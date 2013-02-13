import subprocess

class PreProcessing:

	
	def __init__(self):
		pass

	def __del__(self):
		pass

	def qualityCheck(self,sequenceFile):
		if len(sequenceFile) > 1:
			for i in sequenceFile:
				p = subprocess.Popen([r"program/fastqc/fastqc",i])
				p.wait()

