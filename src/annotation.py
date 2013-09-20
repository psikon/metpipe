# standard imports
import subprocess
import shlex
import sys, os
import time
# imports of own functions and classes
from src.settings import Executables, Blastn_Parameter, MetaCV_Parameter
from src.file_functions import update_reads, create_outputdir, convert_fastq, merge_files, remove_file, parse_parameter
from src.log_functions import Logging
from src.utils import to_string, is_executable, is_fastq, is_paired, blast_output

class Annotation:
    
    raw = ''
    input = ''
    logdir = ''
    blast_out = ''
    metacv_out = ''
    parameter_file = ''
    
    def __init__(self, files_instance, settings_instance, parameter_file, mode):
        # init all important variables and classes
        self.settings = settings_instance
        self.parameter_file = parameter_file
        self.log = Logging()
        self.exe = Executables(self.parameter_file)
        self.files = files_instance
        self.input = self.files.get_input()
        self.logdir = self.files.get_logdir()
        self.blast_out = self.files.get_blastn_dir()
        self.metacv_out = self.files.get_metacv_dir()
        
        # run the annotation functions when the module is initialized
        if mode.lower() == 'blastn':
            # is executable existing and runnable?
            if is_executable(self.exe.get_Blastn()):
                # start annotation with blastn
                self.blastn(self.blast_out)
                # set the output file for further steps
                self.files.set_blastn_output(update_reads(self.blast_out,'blastn','xml'))
                # raise step_number
                self.settings.set_step_number()
            else:
                pass
        elif mode.lower() == 'metacv':
            # is executable existing and runnable?
            if is_executable(self.exe.get_MetaCV()):
                # start annotation with metacv
                self.metacv(self.metacv_out)
                # set the output file for further steps
                self.files.set_metacv_output(update_reads(self.metacv_out,
                                                          MetaCV_Parameter(self.parameter_file).get_name(),
                                                          'res'))
                # raise step_number
                self.settings.set_step_number()
            else:
                pass
        else: 
            # is executable existing and runnable?
            if is_executable(self.exe.get_Blastn()) and is_executable(self.exe.get_MetaCV()):
                # start annotation with both tools 
                self.blastn(self.blast_out)
                # test for ending and set the right blast output
                self.files.set_blastn_output(update_reads(self.blast_out,
                                                          'blastn',
                                                          blast_output(Blastn_Parameter(self.parameter_file).outfmt).split('.')[1]))
                self.metacv(self.metacv_out)
                self.files.set_metacv_output(update_reads(self.metacv_out,
                                                          MetaCV_Parameter(self.parameter_file).get_name(),
                                                          'res'))
                # raise step_number
                self.settings.set_step_number()
            else:
                pass
            
    def __del__(self):
        pass   
        
            
    def blastn(self, outputdir):
            
        # create a dir for output
        create_outputdir(outputdir)
        
        # blastn can only run with fasta files, so input has to be converted
        if all(is_fastq(i) for i in self.input):
            # print actual informations about the step on stdout
            self.log.print_step(self.settings.get_step_number(), 'Annotation', 'convert fastq files',
                                self.log.cut_path(self.input))
            self.log.newline()
            self.input = convert_fastq(self.input, self.blast_out, self.exe.get_Converter())
        
        # blastn can only annotated one file, so input has to be merged to one file
        if is_paired(self.input):
            # print actual informations about the step on stdout
            self.log.print_step(self.settings.get_step_number(), 'Annotation', 'merging reads to on file',
                                self.log.cut_path(self.input))
            self.log.newline()
            self.input = merge_files(self.input, self.blast_out)
        
        # define the outputformat for the blastn results
        outfile = outputdir + os.sep + blast_output(Blastn_Parameter(self.parameter_file).outfmt)
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Annotation', 'blast sequences against nt database',
                            parse_parameter(Blastn_Parameter(self.parameter_file)))
        self.log.newline()
        # start blastn and wait until completion
        # logfile is not requiered, because blastn has no log function and no output to stdout
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (self.exe.get_Blastn(),
                                          self.exe.get_Blastn_DB(),
                                          to_string(self.input),
                                          outfile,
                                          self.settings.get_threads(), 
                                          parse_parameter(Blastn_Parameter(self.parameter_file)))))
        # wait until process is complete
        p.wait()
        
        # remove the temporary files: converted fastq files and the merged fasta files
        remove_file(outputdir + os.sep, 'converted', 'fasta')
        remove_file(outputdir + os.sep, 'merged', 'fasta')
        # print summary of the process after completion
        self.log.print_verbose('Annotation with blastn complete \n')
        self.log.print_running_time(self.settings.get_actual_time())
        self.log.newline
        
    def metacv(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # create a parameter object for further processing
        parameter = MetaCV_Parameter(self.parameter_file)
        
        # select the input for metacv and convert it in an usable format
        if self.settings.get_use_contigs() is True:
            input = to_string([sys.path[0] + os.sep + i for i in self.files.get_input()])
        else:
            input = to_string([sys.path[0] + os.sep + i for i in self.files.get_raw()])
            
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 
                            'Annotation', 
                            'Annotate bacterial reads with MetaCV',
                            '%s %s %s' % (parameter.get_seq(), 
                                          parameter.get_mode(), 
                                          parameter.get_orf()))
        self.log.newline()
        
        # start MetaCV function and wait until completion
        p = subprocess.Popen(shlex.split('%s classify %s %s %s %s %s %s --threads=%s' % 
                                        (self.exe.get_MetaCV(),
                                         self.exe.get_MetaCV_DB(),
                                         input,
                                         parameter.get_name(),
                                         parameter.get_seq(), 
                                         parameter.get_mode(), 
                                         parameter.get_orf(),
                                         self.settings.get_threads())),
                            stderr = self.log.open_logfile(self.logdir + 'metacv.err.log'), 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.settings.get_verbose():
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished        
        p.wait()

        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 
                            'Annotation', 
                            'Analyse the results of MetaCV',
                            '%s %s %s' % (parameter.get_total_reads(), 
                                          parameter.get_min_qual(), 
                                          parameter.get_taxon()))
        self.log.newline() 
        
        # start MetaCV's res2table function and wait until completion
        p = subprocess.Popen(shlex.split('%s res2table %s %s %s %s %s %s --threads=%s' % 
                                        (self.exe.get_MetaCV(),
                                         self.exe.get_MetaCV_DB(),
                                         to_string(update_reads(outputdir,'metpipe','res')),
                                         parameter.get_name() + '.res2table',
                                         parameter.get_total_reads(), 
                                         parameter.get_min_qual(), 
                                         parameter.get_taxon(),
                                         self.settings.get_threads())),
                            stderr = self.log.open_logfile('metacv.res2table.err.log'), 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.settings.get_verbose():
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished
        p.wait()
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 
                            'Annotation', 
                            'Summarize the results of MetaCV',
                            parameter.get_min_qual())
        self.log.newline()
        
        # start MetaCV's res2sum function and wait until completion
        # the workingdir must be specified to maintain the correct 
        # order of output files
        p = subprocess.Popen(shlex.split('%s res2sum %s %s %s %s' %
                                        (self.exe.get_MetaCV(),
                                        self.exe.get_MetaCV_DB(),
                                        to_string(update_reads(outputdir,'metpipe','res')),
                                        parameter.get_name() + '.res2sum',
                                        parameter.get_min_qual())),
                            stderr = self.log.open_logfile('metacv_res2sum.err.log'), 
                            stdout = subprocess.PIPE,
                            cwd = outputdir + os.sep)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.settings.get_verbose():
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished
        p.wait()
        
        self.log.print_verbose('Annotation with MetaCV complete \n')
        self.log.print_running_time(self.settings.get_actual_time())
        self.log.newline
                
        
        