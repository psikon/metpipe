import os, sys
import shutil
from collections import deque
from src.settings import TrimGalore_Parameter,Blastn_Parameter

def createOutputDir(path):
		try:
			os.makedirs(path)
		except OSError:
			if not os.path.isdir(path):
				raise
			
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

def consoleSummary(settings):
	sys.stdout.write('\nmetpipe - Overview\n\n')
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
			
	return raw_input('\nContinue?\n')

	
	
def consoleOutput(step, arguments):
		sys.stdout.write('Step:      ' + step + '\n')
		sys.stdout.write('Arguments: ' + arguments + '\n')
		sys.stdout.flush()

def moveFiles(src, dst, fileExtension):
	listofFiles = [f for f in os.listdir(src) if f.endswith(fileExtension)]
	for f in listofFiles:
		if os.path.exists(dst + f):
			os.remove(dst + f)
		shutil.move(src + f, dst)

def ParamFileArguments(instance):

	args = ''
	var = vars(instance)
	for name in var:
		if getattr(instance, name):
			if str(getattr(instance, name)).lower() in 'true':
				args += ' ' + instance.arguments.get(str(name))
			elif str(getattr(instance, name)).lower() in 'false':
				pass
			else: 
				args += ' ' + instance.arguments.get(str(name)) + getattr(instance, name)
	return args
			
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
