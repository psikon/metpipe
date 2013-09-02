# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.utils import ParamFileArguments
from src.settings import Settings, Executables, Blastn_Parameter, MetaCV_Parameter
from src.file_functions import create_outputdir, str_input, is_paired, is_fastq, update_reads, is_executable, convert_fastq, merge_files
from src.log_functions import Logging

class Annotation:
    
    input = ''
    blast_out = ''
    metacv_out = ''
    
    def __init__(self, input, blast_out, metacv_out, mode):
        self.log = Logging()
        self.logdir = Settings.logdir
        self.exe = Executables()
        self.input = input
        self.blast_out = Settings.output + os.sep + blast_out
        self.metacv_out = Settings.output + os.sep + metacv_out
        
        if mode.lower() == 'blastn':
            if is_executable(self.exe.BLASTN, 'blastn'):
                self.blastn(self.blast_out)
                Settings.step_number = Settings.step_number + 1
            else:
                pass
        elif mode.lower() == 'metacv':
            if is_executable(self.exe.METACV, 'metacv'):
                self.metacv(self.metacv_out)
                Settings.step_number = Settings.step_number + 1
            else:
                pass
        else: 
            if is_executable(self.exe.BLASTN, 'blastn') and is_executable(self.exe.METACV, 'metacv'):
                self.blastn(self.blast_out)
                self.metacv(self.metacv_out)
                Settings.step_number = Settings.step_number + 1
            else:
                pass
            
    def __del__(self):
        pass   
        
            
    def blastn(self,outputdir):
            
        create_outputdir(outputdir)
        
        ##TODO: Path aufhuebschen
        if all(is_fastq(i) for i in Settings.input):
            self.log.print_step(Settings.step_number, 'Assembly', 'convert fastq files',
                                str_input(self.input))
            self.input = convert_fastq(self.input, self.blast_out)
        
        # funktioniert das?
        if is_paired(self.input):
            self.log.print_step(Settings.step_number, 'Assembly', 'merging reads to on file',
                                str_input(self.input))
            self.input = merge_files(self.input, self.blast_out)
        
        # funktioniert nicht
        if Blastn_Parameter().outfmt == 5:
            outfile = 'blastn.xml' 
        else: 
            outfile = 'blastn.tab'
        
        self.log.print_step(Settings.step_number, 'Assembly', 'blast sequences against nt database',
                            ParamFileArguments(Blastn_Parameter()))
        # start blastn and wait until completion
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (self.exe.BLASTN,
                                          Settings.blastdb_nt,
                                          str_input(self.input),
                                          outputdir + os.sep + outfile,
                                          Settings.threads, ParamFileArguments(Blastn_Parameter()))))
        p.wait()
        
        # print summary of the process after completion
        self.log.print_verbose('Annotation with blastn complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - Settings.actual_time) 
                               + '\n')
        self.log.newline
        
    def metacv(self,outputdir):
        pass