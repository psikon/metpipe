import subprocess
import shlex
import sys, os
import shutil
import time
from src.utils import createOutputDir, ParamFileArguments, convertInput
from src.settings import Settings, FastQC_Parameter, TrimGalore_Parameter, Executables
from src.log_functions import *

class Preprocess:
    
    paired_end = True
    verbose = False
    input = ''
    quality = True
    trimming = True
    logdir = ''
    
    def __init__(self):
        self.exe = Executables()
        self.log = Logging()
        
    def __del__(self):
        pass
    
    def qualityCheck(self,outputdir):
        # checke ob exe exitiert ansonsten mach felhlerbereicht
        createOutputDir(Settings.output + os.sep + outputdir)
        self.log.printStep(1,'quality analysis',ParamFileArguments(FastQC_Parameter()))
        p = subprocess.Popen(shlex.split('%s -t %s -o %s --extract %s %s' % (self.exe.FASTQC, 
                                                                                Settings.threads, 
                                                                                Settings.output + os.sep + outputdir,
                                                                                ParamFileArguments(FastQC_Parameter()),
                                                                                convertInput(Settings.input))),
                             stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    
        while p.poll() is None:
            self.log.updateCMD(p.stderr.readline().rstrip('\n'))
        p.wait()
    
    def trim_and_filter(self,outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        p = subprocess.Popen(shlex.split('%s %s -o %s %s' % (Settings.TRIMGALORE, 
                                                                 ParamFileArguments(TrimGalore_Parameter())
                                                                 , (Settings.output + os.sep + outputdir),
                                                                 convertInput(Settings.input))),
                                 )
        
        
        p.wait