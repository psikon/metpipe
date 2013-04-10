##neuschreiben

import ConfigParser

class parser:
    
# Construrctor section    
    def __init__(self,paramFile):
        self.conf = ConfigParser.ConfigParser()
        if (not paramFile):
            self.conf.read("parameter.conf")
        else:
            self.conf.read(paramFile)
       
    def __del__(self):
        pass

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
        