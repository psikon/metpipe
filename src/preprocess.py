import subprocess
import shlex
import sys, os, time
from src.utils import ParamFileArguments
from src.settings import RunSettings, FastQC_Parameter, TrimGalore_Parameter, Executables, FileSettings
from src.log_functions import Logging
from src.file_functions import create_outputdir, str_input, is_executable, update_reads

class Preprocess:
    
    input = ''
    logfile = ''
    quality_dir = ''
    trim_dir = ''
    
    def __init__(self, quality_dir, trim_dir, files_instance):
        
        # init the important classes and variables
        self.exe = Executables()
        self.log = Logging()
        self.files = files_instance
        self.input = str_input(self.files.get_input())
        # define the dirs for log and processing
        self.quality_dir = RunSettings.output + os.sep + quality_dir
        self.trim_dir = RunSettings.output + os.sep + trim_dir
        self.logfile = RunSettings.logdir + os.sep + 'trimming.log.txt'
        
        # test for fastq noch integrieren
        
        # run the preprocessing functions when the module is initialized
        if RunSettings.quality:
            # is executable existing and runnable?
            if is_executable(self.exe.FASTQC, 'fastqc'):
                self.qualityCheck()
                # raise the step number for cmd output
                RunSettings.step_number = RunSettings.step_number + 1
                #self.files.set_quality_report()
                          
        if RunSettings.trim:
            if is_executable(self.exe.TRIMGALORE, 'trim galore'):
                self.trim_and_filter()
                # update the input to the processed input
                self.files.set_input(update_reads(self.trim_dir, 'val', 'fq'))
                self.files.set_preprocessed_output(update_reads(self.trim_dir, 'val', 'fq'))
                # raise the step number for cmd output
                RunSettings.step_number = RunSettings.step_number + 1
            else:
                pass
                
    def __del__(self):
        pass
    
    def qualityCheck(self):
        
        # create a dir for output
        create_outputdir(self.quality_dir)
        
        # print actual informations about the step on stdout
        self.log.print_step(RunSettings.step_number, 'Preprocess', 'quality analysis',
                            ParamFileArguments(FastQC_Parameter()))
        self.log.newline()
        
        # run FastQC with the given parameter, in seperate threads and extract the output
        p = subprocess.Popen(shlex.split('%s -t %s -o %s --extract %s %s' 
                                         % (self.exe.FASTQC,
                                            RunSettings.threads,
                                            self.quality_dir, 
                                            ParamFileArguments(FastQC_Parameter()),
                                            self.input)),
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        # during processing pipe the output and print it on screen
        # no logfile needed, because FastQC is a log function
        while p.poll() is None:
            if RunSettings.verbose:
                self.log.print_verbose(p.stderr.readline())
            else:
                self.log.print_compact(p.stderr.readline().rstrip('\n'))
        # wait until process is finished
        p.wait()
        # print summary of the process after completion
        self.log.print_verbose('Quality check complete for %s\n' % (self.input))
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - RunSettings.actual_time) 
                               + '\n')
        self.log.newline
    
    def trim_and_filter(self):
        
        # create a dir for output
        create_outputdir(self.trim_dir)
        
        # print actual informations about the step on stdout
        self.log.print_step(RunSettings.step_number, 'Preprocess', 'quality based trimming and filtering',
                            ParamFileArguments(TrimGalore_Parameter()))
        self.log.newline()
        
        # open the log file
        self.logfile = self.log.open_logfile(self.logfile)
        
        # start trim_galore with the given parameter and specified output dir
        p = subprocess.Popen(shlex.split('%s %s -o %s %s' % 
                                         (self.exe.TRIMGALORE,
                                          ParamFileArguments(TrimGalore_Parameter()),
                                          self.trim_dir,
                                          self.input)),
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)
        # wait until process is finished
        p.wait()
        # after processing write all generated output to the log file
        for line in p.stderr:
            if RunSettings.verbose:
                # in verbose mode additionally print output to stdout 
                self.log.print_verbose(line)
                self.logfile.write(line)
            else:
                self.logfile.write(line)

        # print summary of the process after completion
        self.log.print_verbose('Trimming and filtering complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - RunSettings.actual_time) 
                               + '\n')
        self.log.newline
        
        
        
        
