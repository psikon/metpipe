# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.settings import Executables, Blastn_Parameter, MetaCV_Parameter
from src.file_functions import *
from src.log_functions import Logging

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
                # verbessern
                self.files.set_blastn_output(update_reads(self.blast_out,'blastn','xml'))
                self.settings.set_step_number()
            else:
                pass
        elif mode.lower() == 'metacv':
            # is executable existing and runnable?
            if is_executable(self.exe.get_MetaCV()):
                # start annotation with metacv
                self.metacv(self.metacv_out)
                self.settings.set_step_number()
            else:
                pass
        else: 
            # is executable existing and runnable?
            if is_executable(self.exe.get_Blastn()) and is_executable(self.exe.get_MetaCV()):
                # start annotation with both tools 
                self.blastn(self.blast_out)
                self.metacv(self.metacv_out)
                self.settings.set_step_number()
            else:
                pass
            
    def __del__(self):
        pass   
        
            
    def blastn(self, outputdir):
            
        # create a dir for output
        create_outputdir(outputdir)
        
        # blastn can only run with dfasta files, so input has to be converted
        if all(is_fastq(i) for i in self.input):
            # print actual informations about the step on stdout
            self.log.print_step(self.settings.get_step_number(), 'Annotation', 'convert fastq files',
                                self.log.cut_path(self.input))
            self.input = convert_fastq(self.input, self.blast_out, self.exe.get_Converter())
        
        # blastn can only annotated one file, so input has to be merged to one file
        if is_paired(self.input):
            # print actual informations about the step on stdout
            self.log.print_step(self.settings.get_step_number(), 'Annotation', 'merging reads to on file',
                                self.log.cut_path(self.input))
            self.input = merge_files(self.input, self.blast_out)
        
        # define the outputformat for the blastn results
        outfile = outputdir + os.sep + blast_output(Blastn_Parameter(self.parameter_file).outfmt)
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Annotation', 'blast sequences against nt database',
                            parse_parameter(Blastn_Parameter(self.parameter_file)))
        
        # start blastn and wait until completion
        # logfile is not requiered, because blastn has no log function and no output to stdout
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (self.exe.get_Blastn(),
                                          self.exe.get_Blastn_DB(),
                                          str_input(self.input),
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
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - self.settings.get_actual_time()) 
                               + '\n')
        self.log.newline
        
    def metacv(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # select the input for metacv 
        if self.settings.get_use_contigs() is True:
            input = self.files.get_input() 
        else:
            input = self.files.get_raw()
            
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Annotation', 'annotate bacterial reads with MetaCV',
                            parse_parameter(MetaCV_Parameter(self.parameter_file)))
        try:
            p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % 
                                             (self.exe.get_MetaCV(),
                                              self.exe.get_MetaCV_DB(),
                                              str_input(input),
                                              'metpipe',
                                              parse_parameter(MetaCV_Parameter(self.parameter_file)))))
                                              #stderr = self.log.open_logfile(self.logdir + 'metacv.err.log'), 
                                              #stdout = subprocess.PIPE)
            while p.poll() is None:
                if self.settings.get_verbose():
                    self.log.print_verbose(p.stdout.readline())
                else:
                    self.log.print_compact(p.stdout.readline().rstrip('\n'))
        except:
            pass
        
#        p = subprocess.Popen(shlex.split('%s res2table %s %s %s %s' % 
#                                        (self.exe.get_MetaCV(),
#                                         self.exe.get_MetaCV_DB(),
#                                         str_input(input),
#                                         'metpipe',
#                                         parse_parameter(MetaCV_Parameter(self.parameter_file)))),
#                                 stderr = self.log.open_logfile('metacv.err.log'), 
#                                 stdout = subprocess.PIPE)
#        while p.poll() is None:
#            if self.settings.get_verbose():
#                self.log.print_verbose(p.stdout.readline())
#            else:
#                self.log.print_compact(p.stdout.readline().rstrip('\n'))

        # wait until process is finished        
        p.wait()
        