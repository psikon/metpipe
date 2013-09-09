import os, sys
import shutil
from collections import deque
from datetime import date
from src.settings import TrimGalore_Parameter, Blastn_Parameter, General

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
		elif settings_instance.assembler.lower() == 'flash':
			queue.append(Task(settings_instance, program_instance.flash, 'flash'))
		elif settings_instance.assembler.lower() == 'flash+metavelvet':
			queue.append(Task(settings_instance,program_instance.assembly_with_Preprocessing,'assembly_with_Preprocessing'))
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
	if settings_instance.skip.lower() == 'summary':
		pass
	else:
		queue.append(Task(settings_instance, program_instance.summary,'analysis'))
	return queue

# before start the first run - print all important settings on the cmd
def consoleSummary(settings):
	logging('\nmetpipe - run on %s\n\n'%(date.today()))
	if settings.verbose:
		logging('Verbose Output: ' + 'yes' + '\n')
	else:
		logging('Verbose Output: ' + 'no' + '\n')
	if settings.quality:
		logging('Quality Report: ' + 'yes' + '\n')
	else:
		logging('Quality Report: ' + 'no' + '\n')
	if settings.trim:
		logging('Read Trimming : ' + 'yes' + '\n')
		trim = TrimGalore_Parameter()
		logging(' - trim down to : ' + trim.length + 'bp' + '\n')
		logging(' - min quality  : ' + trim.quality + '\n')
		logging(' - paired reads : ' + str(trim.paired) + '\n')
	else:
		logging('Read Trimming : ' + 'no' + '\n')
	if  settings.skip.lower() == 'assembly':
		logging('Assembly      : skipped \n')
	else:
		logging('Assembly      : ' + settings.assembler + '\n')
	if  settings.skip.lower() == 'annotation':
		logging('Classify      : skipped \n')
	else:
		if settings.classify.lower() == 'blastn':
			logging('Classify      : ' + settings.classify + '\n')
			blastn = Blastn_Parameter()
			if blastn.db == '':
				logging(' - blastn db: nt \n')
			else:
				logging(' - blastn db: ' + blastn.db + '\n')
			if blastn.outfmt == 6:
				logging(' - outfmt   : table \n')
			elif blastn.outfmt == 5:
				logging(' - outfmt   : xml \n')
			else:
				logging(' - outfmt   : ' + blastn.outfmt + '\n') 
			if blastn.evalue:
				logging(' - evalue   : ' + blastn.evalue + '\n')
			if blastn.perc_identity:
				logging(' - perc id  : ' + blastn.perc_identity + '\n')	
		elif settings.classify.lower() == 'metacv':
			logging('Classify      : ' + settings.classify + '\n')
			if settings.use_contigs == True:
				logging(' - input: contigs \n')
			else:
				logging(' - input: RAW \n')
		else: 
			logging('Classify      : ' + settings.classify + '\n')
			blastn = Blastn_Parameter()
			logging('Blastn Parameter: \n')
			if blastn.db == '':
				logging(' - blastn db: nt \n')
			else:
				logging(' - blastn db: ' + blastn.db + '\n')
			if blastn.outfmt == 6:
				logging(' - outfmt   : table \n')
			elif blastn.outfmt == 5:
				logging(' - outfmt   : xml \n')
			else:
				logging(' - outfmt   : ' + blastn.outfmt + '\n') 
			if blastn.evalue:
				logging(' - evalue   : ' + blastn.evalue + '\n')
			if blastn.perc_identity:
				logging(' - perc id  : ' + blastn.perc_identity + '\n')	
			logging('MetaCV Parameter:\n ')
			if settings.use_contigs == True:
				logging(' - input: contigs \n')
			else:
				logging(' - input: RAW \n')
				
	if settings.summary:
		logging('Summary       : yes \n')
	else:
		logging('Summary       : no \n')
		
	# only continue when keyboard command comes
	if settings.automatic:
		return True
	else:
		return raw_input('\nContinue?\n')




			
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
	
	def setOutputDir(self, outputDir):
		self.outputDir = outputDir

	

	

