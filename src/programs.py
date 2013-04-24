import subprocess
import os
import errno
from src.settings import *
from src.utils import *
from docutils.io import FileOutput

class Programs:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
    
    
    def setfileHandler(self,fileHandler):
        self.fileObject = fileHandler
    
    def getfileHandler(self):
        return self.fileObject
    
    def generateArguments(self,settings):
        pass
        
    def fastqc(self,program,settings):
    	createOutputDir(Settings.output+os.sep+self.fileObject.getOutputdir())
        arguments = ("%s -t %s -o %s -q --extract %s")%(' '.join(sys.path[0] + os.sep + 
														str(i)for i in Settings.input),Settings.threads,
														Settings.output+os.sep+self.fileObject.getOutputdir(),
														FastQC_Parameter().checkUsedArguments())
        print "FastQC: "+arguments
        #p = subprocess.Popen(shlex.split(Settings.FASTQC + " " + arguments))
        #p.wait()
        return FileHandler(Attributes.raw_typ, Attributes.raw_status, program.trimming, 
						   settings,"trimmed",Attributes.program_syntax[0])
       
       	
    def trimming(self,program, settings):
        createOutputDir(Settings.output+os.sep+self.fileObject.getOutputdir())
        arguments = ("%s %s")%(TrimGalore_Parameter().checkUsedArguments(),
							' '.join(sys.path[0]+os.sep+str(i)for i in Settings.input))
        print "Trim: "+arguments
        #p = subprocess.Popen(shlex.split(Settings.TRIMGALORE + " " + arguments))
        #p.wait()
        Settings.input = [Settings.output + os.sep + self.fileObject.getOutputdir() + os.sep + "forward.fastq",
						  Settings.output + os.sep + self.fileObject.getOutputdir() + os.sep + "reverse.fastq"]
        return FileHandler(Attributes.filter_typ,Attributes.filter_status,program.concat,settings,"concat",
						Attributes.program_syntax[0])
        
    def assembly(self,program,settings):
    	velveth_args = "%s %s %s"%(Settings.output + os.sep + self.fileObject.getOutputdir(),Settings.kmer,
								Velveth_Parameter().checkUsedArguments())
    	print "Velveth: "+velveth_args
    	velvetg_args = "%s %s"%(Settings.output + os.sep + self.fileObject.getOutputdir(),
								Velvetg_Parameter().checkUsedArguments())
        pass
    
    def concat(self,program,settings):
        createOutputDir(Settings.output+os.sep+self.fileObject.getOutputdir())
        if len(Settings.input) > 1:
        	arguments = "-i %s -j %s -o %s -t %s %s " % (sys.path[0]+os.sep+Settings.input[0],
												  		 sys.path[0]+os.sep+Settings.input[1],
												  		 Settings.output+os.sep+self.fileObject.getOutputdir(), 
												  		 Settings.threads,
												  		 Concat_Parameter().checkUsedArguments())
        else:
        	arguments = "-i %s -o %s -t %s %s " % (sys.path[0]+os.sep+Settings.input,
												  		 Settings.output+os.sep+self.fileObject.getOutputdir(), 
												  		 Settings.threads,
												  		 Concat_Parameter().checkUsedArguments())
        print "Stitch: "+arguments
        return FileHandler(Attributes.filter_typ,Attributes.filter_status,program.assembly,settings,"assembly",
						Attributes.program_syntax[0])
    
    def blastn(self):
        pass
    
    def metaCV(self):
        pass