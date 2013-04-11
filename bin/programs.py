import subprocess
import os
from bin.misc import Misc
from bin.fileHandler import fileHandler
import errno

class Programs:
    
    def __init__(self,output,quiet,threads):
        self.fileObject = fileHandler("","","","","","","")
        self.output = output
        self.quiet = quiet
        self.threads=threads
        self.helper = Misc()
        
    def __del__(self):
        pass
    
    
    def setfileHandler(self,fileHandler):
        self.fileObject = fileHandler
    
    def getfileHandler(self):
        return self.fileObject
        
    def fastqc(self):
        # fastqc specific arguments
        fastqc_out = "-o " + self.output + "qualityCheck/"
        extract = "--extract"
        threads = "-t " + self.threads
        if (self.quiet):
            quiet ="-q"
        else:
            quiet=""
        self.helper.createOutputDir(self.output+"qualityCheck")  
        
            
        os.system("fastqc %s %s %s %s" %(fastqc_out,extract, threads, ' '.join(str(i) for i in self.fileObject.getPath())))
        #os.system(self.helper.createProgramString())
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