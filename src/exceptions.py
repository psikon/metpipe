import sys, os
from src.settings import FileSettings

# General Exceptions

class NoExecutable(Exception):
    
    def __init__(self, args):
        sys.stdout.write('ERROR 4: No Executable found!') 
        sys.stdout.write('Please check path in parameter file:\n%s\n'
                         % (args))
        os._exit(1)

class FileNotFound(Exception):
    pass

# Preprocess Exceptions

class FastQException(Exception):
    
    def __init__(self, args):
        sys.stdout.write('ERROR 112: Input File not in FASTQ Format!:\n%s\n'
                         % (args))
        sys.stdout.write('Quality Information is needed for Preprocessing!\n\n')
        
        



        

