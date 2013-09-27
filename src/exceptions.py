import sys, os
from src.settings import FileSettings

class ParameterFileNotFound(Exception):
    
    def __init__(self, args):
        self.args = args
        
class NoParameterSection(Exception):
        
    def __init__(self, args):
        self.args = args
        
class NoExecutable(Exception):
    
    def __init__(self, args):
        sys.stdout.write("ERROR 4: No Executable found!\n") 
        sys.stdout.write("Please check path in parameter file: \n%s\n" % (args))
        os._exit(1)

class FileNotFound(Exception):
    pass
