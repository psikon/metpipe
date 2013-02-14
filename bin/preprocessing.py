import subprocess
from bin.misc import Helper

class PreProcessing:

	
	def __init__(self):
		self.helper = Helper()

	def __del__(self):
		pass

	def qualityCheck(self, sequenceFile, threads):
		p = subprocess.Popen(self.helper.createArgs('program/fastqc/fastqc -o result/qualityCheck -t %i %s' % (threads, ' '.join(str(i) for i in (sequenceFile)))))
		p.wait()
		
	def analyseQuality(self, qualityFiles, threads):
		pass
	
	def qualityTrimming(self, sequenceFile, threads, paramsFile):
		# init the parameter for trim_galore
		min_length = self.helper.checkParameter("PreProcessing", "min_length", paramsFile)
		quality = self.helper.checkParameter("PreProcessing", "quality", paramsFile)
		if self.helper.checkParameter("PreProcessing", "paired", paramsFile) == "yes":
			paired ='--paired'
		else: paired=''
		if self.helper.checkParameter("PreProcessing", "save single-end", paramsFile) == "yes":
			retain ='--retain_unpaired'
		else:
			retain=''
		phred = '--phred'+self.helper.checkParameter("PreProcessing", "phred Score", paramsFile)
		args = 'program/trim_galore/trim_galore -o result -q %s --length %s %s %s %s %s' % (quality,min_length,paired,retain,phred,' '.join(str(i) for i in (sequenceFile))))
		p =subprocess.Popen(args)
		p.wait()
		
		
		

		
