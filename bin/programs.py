import subprocess
from bin.misc import Misc
from bin.fileHandler import fileHandler

class Programs:
    
    
    def __init__(self):
        self.fileObject = fileHandler("","","","","","","")
        
    def __del__(self):
        pass
    
    
    def setfileHandler(self,fileHandler):
        self.fileObject = fileHandler
    
    def getfileHandler(self):
        return self.fileObject
        
    def fastqc(self):
        
        return fileHandler("RAW",self.fileObject.setStatus("quality checked"),self.fastqc.__name__,
                        self.trimming,self.fileObject.getPath(),"fastq",self.fileObject.getParameter())
        
        
    def trimming(self):
        pass
        
    def assembly(self):
        pass
    
    def concat(self):
        pass
    
    def blastn(self):
        pass
    
    def metaCV(self):
        pass