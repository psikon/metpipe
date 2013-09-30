# standard imports
import subprocess
import shlex
import sys, os
import time
# imports of own functions and classes
from src.file_functions import update_reads, create_outputdir, convert_fastq, merge_files, remove_file, parse_parameter
from src.log_functions import print_step, newline, print_compact, print_verbose, open_logfile, print_running_time, remove_empty_logfile, cut_path
from src.utils import to_string, is_executable, is_fastq, is_paired, blast_output

class Annotation:
      
    def __init__(self, threads, step_number, verbose, time, logdir, input, raw, mode, contigs,
                 blastn_exe, blastn_db, converter_exe, blast_dir, outfmt, blast_parameter,
                 metacv_exe, metacv_db, metacv_dir, metacv_name, metacv_instance):
                 
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
        self.metacv_name = metacv_name
        self.metacv_instance = metacv_instance
                
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
                blast_out = update_reads(self.blast_dir,
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
                blast_out = update_reads(self.blast_dir,
                                         'blastn',
                                         blast_output(self.outfmt).split('.')[1])
                self.metacv(self.metacv_dir)
                metacv_out = update_reads(self.metacv_dir,
                                          self.metacv_name,
                                          'res')
                # raise step_number
                self.step_number += 1
        
        return [self.step_number, blast_out, metacv_out]
    
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
            self.input = merge_files(self.input, self.blast_dir)
        
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
                                          self.blast_parameter)))
        # wait until process is complete
        p.wait()
        
        # remove the temporary files: converted fastq files and the merged fasta files
        remove_file(outputdir + os.sep, 'converted', 'fasta')
        remove_file(outputdir + os.sep, 'merged', 'fasta')
        
        # print summary of the process after completion
        print_verbose('Annotation with blastn complete \n')
        print_running_time(self.time)
        newline()
        
    def metacv(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        parameter = self.metacv_instance
        # select the input for metacv and convert it in an usable format
        if self.contigs is True:
            input = to_string([sys.path[0] + os.sep + i for i in self.input])
        else:
            input = to_string([sys.path[0] + os.sep + i for i in self.raw])
            
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Annotation', 
                   'Annotate bacterial reads with MetaCV',
                    '%s %s %s' % (parameter.get_seq(), 
                                  parameter.get_mode(), 
                                  parameter.get_orf()))
        newline()
        
        # start MetaCV function and wait until completion
        p = subprocess.Popen(shlex.split('%s classify %s %s %s %s %s %s --threads=%s' % 
                                        (self.metacv_exe,
                                         self.metacv_db,
                                         input,
                                         parameter.get_name(),
                                         parameter.get_seq(), 
                                         parameter.get_mode(), 
                                         parameter.get_orf(),
                                         self.threads)),
                            stderr = open_logfile(self.logdir + 'metacv.err.log'), 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stdout.readline())
            else:
                print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished        
        p.wait()

        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Annotation', 
                   'Analyse the results of MetaCV',
                   '%s %s %s' % (parameter.get_total_reads(), 
                                 parameter.get_min_qual(), 
                                 parameter.get_taxon()))
        newline() 
        
        # start MetaCV's res2table function and wait until completion
        p = subprocess.Popen(shlex.split('%s res2table %s %s %s %s %s %s --threads=%s' % 
                                        (self.metacv_exe,
                                         self.metacv_db,
                                         to_string(update_reads(outputdir,'metpipe','res')),
                                         parameter.get_name() + '.res2table',
                                         parameter.get_total_reads(), 
                                         parameter.get_min_qual(), 
                                         parameter.get_taxon(),
                                         self.threads)),
                            stderr = open_logfile('metacv.res2table.err.log'), 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stdout.readline())
            else:
                print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished
        p.wait()
        
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Annotation', 
                   'Summarize the results of MetaCV',
                   parameter.get_min_qual())
        newline()
        
        # start MetaCV's res2sum function and wait until completion
        # the workingdir must be specified to maintain the correct 
        # order of output files
        p = subprocess.Popen(shlex.split('%s res2sum %s %s %s %s' %
                                        (self.metacv_exe,
                                         self.metacv_db,
                                         to_string(update_reads(outputdir,'metpipe','res')),
                                         parameter.get_name() + '.res2sum',
                                         parameter.get_min_qual())),
                            stderr = open_logfile('metacv_res2sum.err.log'), 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stdout.readline())
            else:
                print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished
        p.wait()
        
        # print summary of the process after completion
        print_verbose('Annotation with MetaCV complete \n')
        print_running_time(self.time)
        newline()
                
        
        