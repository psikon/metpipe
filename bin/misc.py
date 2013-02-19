import ConfigParser
import argparse
import shlex


class Helper:
	
	def __init__(self):
		pass
	
	def __del__(self):
		pass

	def checkParameter(self,item, value, paramsFile):

		x = ConfigParser.ConfigParser()
		x.read(paramsFile)
		return x.get(item,value)
	
	def parseCommandline(self):

		parser = argparse.ArgumentParser(description="run script for the pipeline metpipe")
		parser.add_argument("input",metavar='N', type=str, nargs='+',
						help="single-end or paired-end input files in <fastq>")
		parser.add_argument("-q","--quiet",help="print no status messages to stdout",action="store_true")
		parser.add_argument("-t","--threads",help="specify number of threads to be used",type=int)
		parser.add_argument("--skip",help="skip steps in pipeline",type=str)
		return parser.parse_args()
	
	def createArgs(self,params):
		return shlex.split(params)
	
	def skipStep(self,skip,category):
		
		if skip == category: 
			return False
		else:
			return True
		