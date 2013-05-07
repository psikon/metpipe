import os
import sys
import shutil
import zipfile

def str2bool(string):
		return string.lower() in ("yes", "true", "t", "1")

def bool2Str(string):
		if str(string).lower in ("yes", "t", "1", "y", "True"):
			return "yes"
		else: 
			return "no"

def checkBool(variable):
	if isinstance(variable, bool):
		return True
	else: 
		return False
	
def createOutputDir(path):
		try:
			os.makedirs(path)
		except OSError:
			if not os.path.isdir(path):
				raise

def consoleOutput(step, arguments):
		sys.stdout.write("Step:      " + step + "\n")
		sys.stdout.write("Arguments: " + arguments + "\n")
		sys.stdout.flush()

def moveFiles(src, dst, fileExtension):
	listofFiles = [f for f in os.listdir(src) if f.endswith(fileExtension)]
	for f in listofFiles:
		if os.path.exists(dst + f):
			os.remove(dst + f)
		shutil.move(src + f, dst)

def ParamFileArguments(instance):

	args = ""
	var = vars(instance)
	for name in var:
		if getattr(instance, name):
			if str(getattr(instance, name)).lower() in 'true':
				args += " " + instance.arguments.get(str(name))
			elif str(getattr(instance, name)).lower() in 'false':
				pass
			else: 
				args += " " + instance.arguments.get(str(name)) + getattr(instance, name)
	return args

def autotrim(outputdir):
	
	# get filenames of the quality reports
	fastqc = [f for f in os.listdir(outputdir) if f.endswith(".zip")]
	# unpack only the quality report 
	for file in fastqc:
		with zipfile.ZipFile(outputdir+file) as zip_file:
			for member in zip_file.namelist():
				filename = os.path.basename(member)
				if not filename:
					continue
				if filename.endswith("data.txt"):
					source = zip_file.open(member)
					with source, outputdir+filename:
						shutil.copyfileobj(source, outputdir+filename)
					
				
							
						
	
	sys.exit()
	# --paired -q --phred33 --length 
			
class Task:
	
	def __init__(self, parameter, task, outputDir):
		self.parameter = parameter
		self.task = task
		self.outputDir = outputDir
		
	def __del__(self):
		pass
	
	def getParameter(self):
		return self.parameter

	def setParameter(self, parameter):
		self.parameter = parameter
		
	def getTask(self):
		return self.task
	
	def setTask(self, task):
		self.task = task
		
	def getOutputDir(self):
		return self.outputDir
	
	def setOutputDir(self, dir):
		self.outputDir = dir
