import shlex
import os
import sys

def str2bool(string):
		return string.lower() in ("yes","true","t","1")

def bool2Str(object):
		if str(object).lower in  ("yes","true","t","1","y"):
			return "Yes"
		else: 
			return "No"

def createOutputDir(path):
		try:
			os.makedirs(path)
		except OSError:
			if not os.path.isdir(path):
				raise
				
class Utils:
	
	def __inti__(self):
		pass
	
	
	
	
		
	def checkInstallation(self, path):
		return os._exists(path)

	
	
               	
	def skipStep(self, skip, category):
		
		if skip == category: 
			return False
		else:
			return True
		
class Attributes:
	
	#attributes for tasks
	raw_typ = "RAW"
	raw_status = "unprocessed"
	filter_typ = "RAW"
	filter_status = "processed"
	assembly_typ = "contigs"
	assembly_status = "assembled"
	annotate_typ = "annotations"
	annotate_status = "annotated"
	# attributes for syntax
	# boolean = True/False 
	# words = Yes/No
	program_syntax = ["boolean", "words"]
	
	
class FileHandler:

	def __init__(self, typ, status, nextStep, parameter, outputdir, program_syntax):
		self.typ = typ
		self.status = status
		self.nextStep = nextStep
		self.parameter = parameter
		self.outputdir = outputdir
		self.program_syntax = program_syntax
		
	def __del__(self):
		pass
	
	def getTyp(self):
		return self.typ

	def getStatus(self):
		return self.status

	def getNextStep(self):
		return self.nextStep

	def getParameter(self):
		return self.parameter
	
	def getOutputdir(self):
		return self.outputdir
	
	def getProgramSyntax(self):
		return self.program_syntax

	def setTyp(self, typ):
		self.typ = typ

	def setStatus(self, string):
		self.status += string

	def setNextStep(self, destination):
		self.destination = destination

	def setParameter(self, parameter):
		self.parameter = parameter	
	
	def	setOutputdir(self, outputdir):
		self.outputdir = outputdir
		
	def setProgramsyntax(self,program_syntax):
		self.program_syntax = program_syntax


		
