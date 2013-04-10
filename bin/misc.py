import shlex
import os


class Misc:
	
	def __init__(self):
		pass
	
	def __del__(self):
		pass

	def checkInstallation(self,path):
		return os._exists(path)
	
	def createProgramString(self, params):
		return shlex.split(params)
		
	def createArgs(self, params):
		return shlex.split(params)
	
	def startProcess(self, program, params):
		os.system(program + " " + params)
		return os.getpid()
		
	def skipStep(self, skip, category):
		
		if skip == category: 
			return False
		else:
			return True
		
