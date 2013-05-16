import os, sys
import shutil
from collections import deque
from src.settings import TrimGalore_Parameter,Blastn_Parameter

# simple function to create a dir
def createOutputDir(path):
		
		try:
			os.makedirs(path)
		except OSError:
			# if dir exists and is dir go ahead
			if not os.path.isdir(path):
				raise

# function to fill the working queue with tasks based on the cli commands
def createTasks(settings_instance, program_instance):
	queue = deque()
	
	# create Preprocessing steps
	if settings_instance.quality:
		queue.append(Task(settings_instance, program_instance.fastqc, 'RAW'))
	if settings_instance.trim:
		queue.append(Task(settings_instance, program_instance.trimming, 'trimmed'))
		if settings_instance.quality:
			queue.append(Task(settings_instance, program_instance.fastqc, 'trimmed'))
	# Assembly tasks
	if settings_instance.skip.lower() == 'assembly':
		pass
	else:
		if settings_instance.assembler.lower() == 'concat':	
			queue.append(Task(settings_instance, program_instance.concat, 'concat'))
		else:
			queue.append(Task(settings_instance, program_instance.assembly, 'assembly'))
	# Annotation
	if settings_instance.skip.lower() == 'annotation':
		pass
	else:
		if settings_instance.classify.lower() == 'both':
			queue.append(Task(settings_instance, program_instance.blastn, 'blastn'))
			queue.append(Task(settings_instance, program_instance.metaCV, 'metacv'))
		elif settings_instance.classify.lower() == 'metacv':
			queue.append(Task(settings_instance, program_instance.metaCV, 'metacv'))
		else:
			queue.append(Task(settings_instance, program_instance.blastn, 'blastn'))
	return queue

# before start the first run - print all important settings on the cmd
def consoleSummary(settings):
	sys.stdout.write('\nmetpipe - Overview\n\n')
	if settings.verbose:
		sys.stdout.write('Verbose Output: ' + 'yes' + '\n')
	else:
		sys.stdout.write('Verbose Output: ' + 'no' + '\n')
	if settings.quality:
		sys.stdout.write('Quality Report: ' + 'yes' + '\n')
	else:
		sys.stdout.write('Quality Report: ' + 'no' + '\n')
	if settings.trim:
		sys.stdout.write('Read Trimming : ' + 'yes' + '\n')
		trim = TrimGalore_Parameter()
		sys.stdout.write(' - trim down to : ' + trim.length + 'bp' + '\n')
		sys.stdout.write(' - min quality  : ' + trim.quality + '\n')
		sys.stdout.write(' - paired reads : ' + str(trim.paired) + '\n')
	else:
		sys.stdout.write('Read Trimming : ' + 'no' + '\n')
	if  settings.skip.lower() == 'assembly':
		sys.stdout.write('Assembly      : skipped \n')
	else:
		if settings.assembler == 'concat':
			sys.stdout.write('Assembly      : ' + settings.assembler + '\n')
		else:
			sys.stdout.write('Assembly      : ' + settings.assembler + '\n')	
	if  settings.skip.lower() == 'annotation':
		sys.stdout.write('Classify      : skipped \n')
	else:
		if settings.classify.lower() == 'blastn':
			sys.stdout.write('Classify      : ' + settings.classify + '\n')
			blastn = Blastn_Parameter()
			if blastn.db == '':
				sys.stdout.write(' - blastn db: nt \n')
			else:
				sys.stdout.write(' - blastn db: ' + blastn.db + '\n')
			if blastn.outfmt == 6:
				sys.stdout.write(' - outfmt   : table \n')
			elif blastn.outfmt == 5:
				sys.stdout.write(' - outfmt   : xml \n')
			else:
				sys.stdout.write(' - outfmt   : ' + blastn.outfmt + '\n') 
			if blastn.evalue:
				sys.stdout.write(' - evalue   : ' + blastn.evalue + '\n')
			if blastn.perc_identity:
				sys.stdout.write(' - perc id  : ' + blastn.perc_identity + '\n')	
		elif settings.classify.lower() == 'metacv':
			sys.stdout.write('Classify      : ' + settings.classify + '\n')
		else: 
			sys.stdout.write('Classify      : ' + settings.classify + '\n')
			blastn = Blastn_Parameter()
			if blastn.db == '':
				sys.stdout.write(' - blastn db: nt \n')
			else:
				sys.stdout.write(' - blastn db: ' + blastn.db + '\n')
			if blastn.outfmt == 6:
				sys.stdout.write(' - outfmt   : table \n')
			elif blastn.outfmt == 5:
				sys.stdout.write(' - outfmt   : xml \n')
			else:
				sys.stdout.write(' - outfmt   : ' + blastn.outfmt + '\n') 
			if blastn.evalue:
				sys.stdout.write(' - evalue   : ' + blastn.evalue + '\n')
			if blastn.perc_identity:
				sys.stdout.write(' - perc id  : ' + blastn.perc_identity + '\n')	
			
	# only continue when keyboard command comes
	return raw_input('\nContinue?\n')

def getDHMS(seconds):
	
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return "%d days, %d hours, %d minutes, %d seconds" % (days, hours, minutes, seconds)

# copy files into another dir
def moveFiles(src, dst, fileExtension):
	listofFiles = [f for f in os.listdir(src) if f.endswith(fileExtension)]
	print 
	for f in listofFiles:
		if os.path.exists(dst + os.sep + f):
			os.remove(dst + os.sep + f)
		shutil.move(src + f, dst)

# important function to get all used arguments from a settings object and convert it to an argument string
def ParamFileArguments(instance):

	args = ''
	# get all used vars of the instance
	var = vars(instance)
	for name in var:
		# if var is boolean and true only print the name of the var in dict
		if getattr(instance, name):
			if str(getattr(instance, name)).lower() in 'true':
				args += ' ' + instance.arguments.get(str(name))
			# if var is boolean and false discard it
			elif str(getattr(instance, name)).lower() in 'false':
				pass
			# else var has a value - print var from dict + value
			else: 
				args += ' ' + instance.arguments.get(str(name)) + getattr(instance, name)
	return args

# test the input file for etxension of fastq files

def testForFQ(testfile):
	if  testfile.endswith(".fq") or testfile.endswith(".fastq"):
		return True
	else:
		return False
			
# class for manage the attributes of the tasks in the workingQueue
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
