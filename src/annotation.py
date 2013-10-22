# standard imports
import subprocess
import shlex
import sys, os
import time
# imports of own functions and classes
from src.file_functions import update_reads, create_outputdir, convert_fastq, merge_files, remove_file, parse_parameter
from src.log_functions import print_step, newline, print_compact, print_verbose, open_logfile, print_running_time, remove_empty_logfile, cut_path
from src.utils import to_string, is_executable, is_fastq, is_paired, blast_output
from src.exceptions import BlastnException, MetaCVException, MetaCVSumException

class Annotation:
      
    def __init__(self, threads, step_number, verbose, time, logdir, input, raw, mode, contigs,
                 blastn_exe, blastn_db, converter_exe, blast_dir, outfmt, blast_parameter,
                 metacv_exe, metacv_db, metacv_dir, metacv_seq, metacv_mode, metacv_orf, 
                 metacv_total_reads, metacv_min_qual, metacv_taxon, metacv_name):
                 
        # init general variables
        self.threads = threads
        self.step_number = step_number
        self.verbose = verbose
        self.time = time
        self.logdir = logdir
        self.input = input
        self.raw = raw
        self.mode = mode
        self.contigs = contigs
        
        # blastn specific variables
        self.blastn_exe = blastn_exe
        self.blastn_db = blastn_db
        self.converter_exe = converter_exe
        self.blast_dir = blast_dir
        self.outfmt = outfmt
        self.blast_parameter = blast_parameter

        # metcv specific variables
        self.metacv_exe = metacv_exe
        self.metacv_db = metacv_db
        self.metacv_dir = metacv_dir
        self.metacv_seq = metacv_seq
        self.metacv_mode = metacv_mode
        self.metacv_orf = metacv_orf
        self.metacv_total_reads = metacv_total_reads
        self.metacv_min_qual = metacv_min_qual
        self.metacv_taxon = metacv_taxon
        self.metacv_name = metacv_name
                
    def __del__(self):
        pass   
        
    def manage_annotation(self):
        blastn_out = ''
        metacv_out = ''
        # run the annotation functions when the module is initialized
        if self.mode.lower() == 'blastn':
            # is executable existing and runnable?
            if is_executable(self.blastn_exe):
                # start annotation with blastn
                self.blastn(self.blast_dir)
                # set the output file for further steps
                blastn_out = update_reads(self.blast_dir,
                                         'blastn',
                                         blast_output(self.outfmt).split('.')[1])
                # raise step_number
                self.step_number += 1
                
        elif self.mode.lower() == 'metacv':
            # is executable existing and runnable?
            if is_executable(self.metacv_exe):
                # start annotation with metacv
                self.metacv(self.metacv_dir)
                # set the output file for further steps
                metacv_out = update_reads(self.metacv_dir,
                                          self.metacv_name,
                                          'res')
                # raise step_number
                self.step_number += 1
                
        else: 
            # is executable existing and runnable?
            if is_executable(self.blastn_exe) and is_executable(self.metacv_exe):
                # start annotation with both tools 
                self.blastn(self.blast_dir)
                # test for ending and set the right blast output
                blastn_out = update_reads(self.blast_dir,
                                         'blastn',
                                         blast_output(self.outfmt).split('.')[1])
                self.metacv(self.metacv_dir)
                metacv_out = update_reads(self.metacv_dir,
                                          self.metacv_name,
                                          'res')
                # raise step_number
                self.step_number += 1
        
        return [self.step_number, blastn_out, metacv_out]
    
    def blastn(self, outputdir):
            
        # create a dir for output
        create_outputdir(outputdir)
        
        # blastn can only run with fasta files, so input has to be converted
        if is_fastq(self.input):
            # print actual informations about the step on stdout
            print_step(self.step_number,
                       'Annotation', 
                       'convert fastq files',
                       cut_path(self.input))
            newline()
            self.input = convert_fastq(self.input, self.blast_dir, self.converter_exe)
        
        # blastn can only annotated one file, so input has to be merged to one file
        if is_paired(self.input):
            # print actual informations about the step on stdout
            print_step(self.step_number,
                       'Annotation',
                       'merging reads to on file',
                       cut_path(self.input))
            newline()
            self.input = merge_files(self.input, self.blast_dir, 'merged', 'fasta')
        
        # define the outputformat for the blastn results
        outfile = outputdir + os.sep + blast_output(self.outfmt)
        
        # print actual informations about the step on stdout
        print_step(self.step_number,
                   'Annotation',
                   'blast sequences against nt database',
                   self.blast_parameter)
        newline()
        # start blastn and wait until completion
        # logfile is not requiered, because blastn has no log function and no output to stdout
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (self.blastn_exe,
                                          self.blastn_db,
                                          to_string(self.input),
                                          outfile,
                                          self.threads, 
                                          self.blast_parameter)),
                             stderr = open_logfile(self.logdir + 'blastn.err.log'))
        # wait until process is complete
        p.wait()
        
        if p.returncode:
            raise BlastnException(self.logdir + 'blastn.err.log')
        else:
            # remove the temporary files: converted fastq files and the merged fasta files
            remove_file(outputdir + os.sep, 'converted', 'fasta')
            remove_file(outputdir + os.sep, 'merged', 'fasta')
            # remove unused error logs
            remove_empty_logfile(self.logdir + 'blastn.err.log')
        
            # print summary of the process after completion
            print_verbose('Annotation with blastn complete \n')
            print_running_time(self.time)
            newline()
        
    def metacv(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # select the input for metacv and convert it in an usable format
        if self.contigs is True:
            input = to_string(self.input)
        else:
            input = to_string(self.raw)
            
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Annotation', 
                   'Annotate bacterial reads with MetaCV',
                    '%s %s %s' % (self.metacv_seq,
                                  self.metacv_mode,
                                  self.metacv_orf))
        newline()
        
        # metacv has a maximum thread number of 64
        # parameter has to be adjusted
        if self.threads > 64:
                threads = 64
        else:
                threads = self.threads
        classify = open_logfile(self.logdir + 'metacv.classify.log')
        # start MetaCV function and wait until completion
        p = subprocess.Popen(shlex.split('%s classify %s %s %s %s %s %s --threads=%s' % 
                                        (self.metacv_exe,
                                         self.metacv_db,
                                         input,
                                         self.metacv_name,
                                         self.metacv_seq, 
                                         self.metacv_mode, 
                                         self.metacv_orf,
                                         threads)),
                            stderr = subprocess.PIPE, 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stderr.readline())
                classify.write(p.stderr.readline())
            else:
                print_compact(p.stderr.readline().rstrip('\n'))
                classify.write(p.stderr.readline())
        # wait until process is finished        
        p.wait()
        
        if p.returncode:
            raise MetaCVException(self.logdir + 'metacv.classify.log')
        else:
            # remove unused error logs
            remove_empty_logfile(self.logdir + 'metacv.classify.log')
            
            # print actual informations about the step on stdout
            print_step(self.step_number, 
                       'Annotation', 
                       'Analyse the results of MetaCV',
                       '%s %s %s' % (self.metacv_total_reads, 
                                     self.metacv_min_qual, 
                                     self.metacv_taxon))
            newline() 
            res2table = open_logfile(self.logdir + 'metacv.res2table.log')
            # start MetaCV's res2table function and wait until completion
            p = subprocess.Popen(shlex.split('%s res2table %s %s %s %s %s %s --threads=%s' % 
                                             (self.metacv_exe,
                                              self.metacv_db,
                                              to_string(update_reads(outputdir,'metpipe','res')),
                                              self.metacv_name + '.res2table',
                                              self.metacv_total_reads, 
                                              self.metacv_min_qual, 
                                              self.metacv_taxon,
                                              threads)),
                                 stderr = subprocess.PIPE, 
                                 stdout = subprocess.PIPE,
                                 cwd = outputdir + os.sep)
            # during processing pipe the output and print it on screen
            while p.poll() is None:
                if self.verbose:
                    print_verbose(p.stderr.readline())
                    res2table.write(p.stderr.readline())
                    
                else:
                    print_compact(p.stderr.readline().rstrip('\n'))
                    res2table.write(p.stderr.readline())
            # wait until process is finished
            p.wait()
        
            if p.returncode:
                raise MetaCVSumException(self.logdir + 'metacv.res2table.log')
            else:
                # remove unused error logs
                remove_empty_logfile(self.logdir + 'metacv.res2table.log')
            # print actual informations about the step on stdout
            print_step(self.step_number, 
                       'Annotation', 
                       'Summarize the results of MetaCV',
                       self.metacv_min_qual)
            newline()
            
            res2sum = open_logfile(self.logdir + 'metacv.res2sum.log')
            # start MetaCV's res2sum function and wait until completion
            # the workingdir must be specified to maintain the correct 
            # order of output files
            p = subprocess.Popen(shlex.split('%s res2sum %s %s %s %s' %
                                             (self.metacv_exe,
                                              self.metacv_db,
                                              to_string(update_reads(outputdir,'metpipe','res')),
                                              self.metacv_name + '.res2sum',
                                              self.metacv_min_qual)),
                                 stderr = subprocess.PIPE, 
                                 stdout = subprocess.PIPE,
                                 cwd = outputdir + os.sep)
            # during processing pipe the output and print it on screen
            while p.poll() is None:
                if self.verbose:
                    print_verbose(p.stderr.readline())
                    res2sum.write(p.stderr.readline())
                else:
                    print_compact(p.stderr.readline().rstrip('\n'))
                    res2sum.write(p.stderr.readline())
            # wait until process is finished
            p.wait()
        
            if p.returncode:
                raise MetaCVSumException(self.logdir + 'metacv.res2sum.log')
            else:
                # remove unused error logs
                remove_empty_logfile(self.logdir + 'metacv.res2sum.log')
        
            # print summary of the process after completion
            print_verbose('Annotation with MetaCV complete \n')
            print_running_time(self.time)
            newline()
                
        
        