"""metpipe

Usage: 
    metpipe [options] <THREADS> <INPUT> ... 

Arguments
    THREADS    number of cores for processing
    INPUT      Input files (single|paired) in <fastq> format
    
Options:
-h                show this help message and exit
--version         show version and exit
-q                print no status messsages to stdout.
--skip            skip steps in the pipeline.
--params=<FILE>   use alternate parameter file [default: parameter.conf].

"""
from bin.docopt import docopt
import ConfigParser

class parser:
    
# Construrctor section    
    def __init__(self):
        #create CLI
        self.arguments= docopt(__doc__,help=True,version="metpipe 0.1 alpha",options_first=False)
        
        if self.getValue('--params') == True:
            self.path = self.getValue("--params")
        else:
            self.path = "parameter.conf"
        
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.path)
       
            
    
    def __del__(self):
        pass

 
# CLI functions
      
    def getArgs(self):
        return self.arguments
    
    def getValue(self,identifier):
        return self.arguments.get(identifier)
    
    def getThreads(self):
        return self.arguments.get('<THREADS>')
    
    def getInput(self):
        return self.arguments.get('<INPUT>')
    
# Params File functions   
        
    def getPath(self):
        return self.path
    
    def setPath(self, path):
        self.path = path
        
    def getSection(self):
        return self.conf.sections()
    
    def getOptions(self,section):
        return self.conf.options(section)
    
    def getAllfromSection(self,section):
        args = {}
        option = self.conf.options(section)
        for option in option:
            try:
                args[option] = self.conf.get(section,option)
                if args[option] == -1:
                        print("skip: %s" % option)
            except:
                args[option] = None
        return args
        