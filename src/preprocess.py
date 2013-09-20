import subprocess
import shlex
import sys, os, time
from src.settings import FastQC_Parameter, TrimGalore_Parameter, Executables, FileSettings
from src.log_functions import Logging
from src.file_functions import create_outputdir, update_reads, parse_parameter
from src.utils import is_executable, to_string

class Preprocess:
    
    input = ''
    logdir = ''
    quality_dir = ''
    trim_dir = ''
    parameter_file = ''
    
    def __init__(self, files_instance, settings_instance, parameter_file):
        
        # init the important classes and variables
        self.settings = settings_instance
        self.parameter_file = parameter_file
        self.exe = Executables(self.parameter_file)
        self.log = Logging()
        self.files = files_instance
        self.input = to_string(self.files.get_input())
        # define the dirs for log and processing
        self.quality_dir = self.files.get_quality_dir()
        self.trim_dir = self.files.get_trim_dir()
        self.logdir = self.files.get_logdir()
        # test for fastq noch integrieren
        
        # run the preprocessing functions when the module is initialized
        if self.settings.get_quality():
            # is executable existing and runnable?
            if is_executable(self.exe.get_FastQC()):
                self.qualityCheck()
                # raise the step number for cmd output
                self.settings.set_step_number()
                #self.files.set_quality_report()
                          
        if self.settings.get_trim():
            if is_executable(self.exe.get_TrimGalore()):
                self.trim_and_filter()
                # update the input to the processed input
                self.files.set_input(update_reads(self.trim_dir, 'val', 'fq'))
                self.files.set_preprocessed_output(update_reads(self.trim_dir, 'val', 'fq'))
                # raise the step number for cmd output
                self.settings.set_step_number()
            else:
                pass
                
    def __del__(self):
        pass
    
    def qualityCheck(self):
        
        # create a dir for output
        create_outputdir(self.quality_dir)
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Preprocess', 'quality analysis',
                            parse_parameter(FastQC_Parameter(self.parameter_file)))
        self.log.newline()
        
        # run FastQC with the given parameter, in seperate threads and extract the output
        try:
            p = subprocess.Popen(shlex.split('%s -t %s -o %s --extract %s %s' 
                                             % (self.exe.get_FastQC(),
                                                self.settings.get_threads(),
                                                self.quality_dir, 
                                                parse_parameter(FastQC_Parameter(self.parameter_file)),
                                                self.input)),
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE)
        # during processing pipe the output and print it on screen
            while p.poll() is None:
                if self.settings.get_verbose():
                    self.log.print_verbose(p.stderr.readline())
                else:
                    self.log.print_compact(p.stderr.readline().rstrip('\n'))
            # wait until process is finished
            p.wait()
        except:
            pass
        # print summary of the process after completion
        self.log.print_verbose('Quality check complete for %s\n' % (self.input))
        self.log.print_running_time(self.settings.get_actual_time())
        self.log.newline
    
    def trim_and_filter(self):
        
        # create a dir for output
        create_outputdir(self.trim_dir)
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Preprocess', 'quality based trimming and filtering',
                            parse_parameter(TrimGalore_Parameter(self.parameter_file)))
        self.log.newline()
        
        # open the log file
        self.logfile = self.log.open_logfile(self.logdir + 'trimming.log')
        
        # start trim_galore with the given parameter and specified output dir
        p = subprocess.Popen(shlex.split('%s %s -o %s %s' % 
                                         (self.exe.get_TrimGalore(),
                                          parse_parameter(TrimGalore_Parameter(self.parameter_file)),
                                          self.trim_dir,
                                          self.input)),
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)
        # wait until process is finished
        p.wait()
        # after processing write all generated output to the log file
        for line in p.stderr:
            if self.settings.get_verbose():
                # in verbose mode additionally print output to stdout 
                self.log.print_verbose(line)
                self.logfile.write(line)
            else:
                self.logfile.write(line)

        # print summary of the process after completion
        self.log.print_verbose('Trimming and filtering complete \n')
        self.log.print_running_time(self.settings.get_actual_time())
        self.log.newline
        
        
        
        
