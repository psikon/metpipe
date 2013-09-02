# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.utils import ParamFileArguments
from src.settings import Settings, Executables, Blastn_Parameter, MetaCV_Parameter
from src.file_functions import *
from src.log_functions import Logging

class Annotation:
    
    input = ''
    blast_out = ''
    metacv_out = ''
    
    def __init__(self, input, blast_out, metacv_out, mode):
        # init all important variables and classes
        self.log = Logging()
        self.logdir = Settings.logdir
        self.exe = Executables()
        self.input = input
        self.blast_out = Settings.output + os.sep + blast_out
        self.metacv_out = Settings.output + os.sep + metacv_out
        
        # run the annotation functions when the module is initialized
        if mode.lower() == 'blastn':
            # is executable existing and runnable?
            if is_executable(self.exe.BLASTN, 'blastn'):
                # start annotation with blastn
                self.blastn(self.blast_out)
                Settings.step_number = Settings.step_number + 1
            else:
                pass
        elif mode.lower() == 'metacv':
            # is executable existing and runnable?
            if is_executable(self.exe.METACV, 'metacv'):
                # start annotation with metacv
                self.metacv(self.metacv_out)
                Settings.step_number = Settings.step_number + 1
            else:
                pass
        else: 
            # is executable existing and runnable?
            if is_executable(self.exe.BLASTN, 'blastn') and is_executable(self.exe.METACV, 'metacv'):
                # start annotation with both tools 
                self.blastn(self.blast_out)
                self.metacv(self.metacv_out)
                Settings.step_number = Settings.step_number + 1
            else:
                pass
            
    def __del__(self):
        pass   
        
            
    def blastn(self,outputdir):
            
        # create a dir for output
        create_outputdir(outputdir)
        
        # blastn can only run with dfasta files, so input has to be converted
        if all(is_fastq(i) for i in Settings.input):
            # print actual informations about the step on stdout
            self.log.print_step(Settings.step_number, 'Assembly', 'convert fastq files',
                                self.log.cut_path(self.input))
            self.input = convert_fastq(self.input, self.blast_out)
        
        # blastn can only annotated one file, so input has to be merged to one file
        if is_paired(self.input):
            # print actual informations about the step on stdout
            self.log.print_step(Settings.step_number, 'Assembly', 'merging reads to on file',
                                self.log.cut_path(self.input))
            self.input = merge_files(self.input, self.blast_out)
        
        # define the outputformat for the blastn results
        outfile = blast_output(Blastn_Parameter().outfmt)
        
        # print actual informations about the step on stdout
        self.log.print_step(Settings.step_number, 'Assembly', 'blast sequences against nt database',
                            ParamFileArguments(Blastn_Parameter()))
        
        # start blastn and wait until completion
        # logfile is not requiered, because blastn has no log function and no output to stdout
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (self.exe.BLASTN,
                                          Settings.blastdb_nt,
                                          str_input(self.input),
                                          outputdir + os.sep + outfile,
                                          Settings.threads, ParamFileArguments(Blastn_Parameter()))))
        # wait until process is complete
        p.wait()
        
        # remove the temporary files: converted fastq files and the merged fasta files
        remove_file(outputdir + os.sep, 'converted', 'fasta')
        remove_file(outputdir + os.sep, 'merged', 'fasta')
        # print summary of the process after completion
        self.log.print_verbose('Annotation with blastn complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - Settings.actual_time) 
                               + '\n')
        self.log.newline
        
    def metacv(self,outputdir):
        pass