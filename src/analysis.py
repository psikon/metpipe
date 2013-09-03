# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.utils import ParamFileArguments
from src.settings import Settings, Executables, xmlParser, Rannotate, subsetDB
from src.file_functions import create_outputdir, str_input, update_reads, is_exe, is_xml
from src.log_functions import Logging

class Analysis:
    
    blast_out = ''
    metacv_out = ''
    krona = False
    logdir = ''
    
    def __init__(self, blast_out, metacv_out, krona):
        self.log = Logging()
        self.exe = Executables()
        self.blast_out = blast_out
        self.metacv_out = metacv_out
        self.krona = krona
        self.logdir = Settings.logdir
        
        if parse_to_db(self.blast_out):
            annotate_db()
        
    
    def __del__(self):
        pass
    
def parse_to_db(self, outputdir):
    
    if is_xml(outdir):
        p = subprocecss.Popen(shlex.split('%s -o %s %s %s' % (self.exe.PARSER,
                                                              outputdir,
                                                              ParamFileArguments(xmlParser()),
                                                              self.blast_out)),
                              stdout = subprocess.PIPE, stderr = self.log.open_logfile(self.logdir + 'parser.err.log'))
        
        while p.poll() is None:
            if Settings.verbose:
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        p.wait()
        return True
        
    else:
        self.log.print_verbose('blast result is not in xml format. (Needed for parsing!)')
        return False
    
def annotate_db(self, outputdir):
    
    p = subprocess.Popen(shlex.split('%s' % ()))
    