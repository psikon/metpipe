import subprocess
import shlex
import sys, os, time
from src.log_functions import print_step, newline, print_compact, print_verbose, open_logfile, print_running_time
from src.file_functions import create_outputdir, update_reads, parse_parameter
from src.utils import is_executable, to_string, is_fastq
from src.exceptions import FastQException
class Preprocess:
     
    def __init__(self, threads, step_number, verbose, time, input , logdir,
                 fastqc_exe,quality, quality_dir, fastqc_parameter,
                 trim_exe, trim, trim_dir, trim_parameter):
           
        # define general  variables 
        self.threads = threads
        self.step_number = step_number
        self.verbose = verbose
        self.time = time
        self.logdir = logdir
        self.input = input
        
        # define quality report variables
        self.fastqc_exe = fastqc_exe
        self.quality = quality
        self.quality_dir = quality_dir
        self.fastqc_parameter = fastqc_parameter
        
        # define trim variables
        self.trim_exe = trim_exe
        self.trim = trim
        self.trim_dir = trim_dir
        self.trim_parameter = trim_parameter
                
    def __del__(self):
        pass
    
    def manage_preprocessing(self):
        # run the preprocessing functions when the module is initialized
        try:
            is_fastq(self.input)
        except FastQException:
            self.quality = False
            self.trim = False
        
        if self.quality:
            # is executable existing and runnable?
            if is_executable(self.fastqc_exe):
                self.qualityCheck()
                # raise the step number for cmd output
                self.step_number += 1
                #self.files.set_quality_report()
                  
        if self.trim:
            if is_executable(self.trim_exe):
                self.trim_and_filter()
                # update the input to the processed input
                # raise the step number for cmd output
                self.step_number += 1
                
        return [self.step_number, update_reads(self.trim_dir, 'val', 'fq')]
        
        
    def qualityCheck(self):
        
        # create a dir for output
        create_outputdir(self.quality_dir)
        
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Preprocess', 
                   'quality analysis',
                   self.fastqc_parameter)
        newline()
        
        # run FastQC with the given parameter, in seperate threads and extract the output

        p = subprocess.Popen(shlex.split('%s -t %s -o %s --extract %s %s' 
                                         % (self.fastqc_exe,
                                            self.threads,
                                            self.quality_dir, 
                                            self.fastqc_parameter,
                                            to_string(self.input))),
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        # during processing pipe the output and print it on screen
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stderr.readline())
            else:
                print_compact(p.stderr.readline().rstrip('\n'))
        # wait until process is finished
        p.wait()

        # print summary of the process after completion
        print_verbose('Quality check complete for %s\n' % (self.input))
        print_running_time(self.time)
        newline
    
    def trim_and_filter(self):
        
        # create a dir for output
        create_outputdir(self.trim_dir)
        
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Preprocess', 
                   'quality based trimming and filtering',
                   self.trim_parameter)
        newline()
        
        # open the log file
        self.logfile = open_logfile(self.logdir + 'trimming.log')
        
        # start trim_galore with the given parameter and specified output dir
        p = subprocess.Popen(shlex.split('%s %s -o %s %s' % 
                                         (self.trim_exe,
                                          self.trim_parameter,
                                          self.trim_dir,
                                          to_string(self.input))),
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)
        # wait until process is finished
        p.wait()
        # after processing write all generated output to the log file
        for line in p.stderr:
            if self.verbose:
                # in verbose mode additionally print output to stdout 
                print_verbose(line)
                self.logfile.write(line)
            else:
                self.logfile.write(line)

        # print summary of the process after completion
        print_verbose('Trimming and filtering complete \n')
        print_running_time(self.time)
        newline
        
        
        
        
