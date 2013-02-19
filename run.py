#!/usr/bin/env python

from bin.misc import Helper
from bin.preprocessing import PreProcessing

# set global variables
helperInstance = Helper()
quiet = helperInstance.parseCommandline().quiet
infile = helperInstance.parseCommandline().input
threads = helperInstance.parseCommandline().threads
skip = helperInstance.parseCommandline().skip
    
def preProcessing(run):
    
    if run == True:
        
        pre = PreProcessing()
        if helperInstance.checkParameter('PreProcessing', 'quality check',"parameter.txt") == 'yes':
            pre.qualityCheck(infile,threads)  
        
        if helperInstance.checkParameter('PreProcessing', 'trimming',"parameter.txt") == 'yes':
            pre.qualityTrimming(infile, threads,"parameter.txt")
            
    else:
        print ("skip Step:", skip)

def assembly(run):

    if run ==True: 
        if helperInstance.checkParameter('Assembly', 'program',"parameter.txt") == 'metavelvet':
            print 'starte metavelvet'
        elif helperInstance.checkParameter('Assembly', 'program',"parameter.txt") == 'abyss':
            print 'starte abyss'
        elif helperInstance.checkParameter('Assembly', 'program',"parameter.txt") == 'metaidba':
            print 'starte metaidba'
        elif helperInstance.checkParameter('Assembly', 'program',"parameter.txt") == 'stitch':
            print "starte stitch"
        else:
            print 'no assembly program recognized! Please check parameter file!'
    else:
        print "skip Step:"+skip

def annotate(run):
    if run ==True: 
        if helperInstance.checkParameter('Annotate', 'program',"parameter.txt") == 'blastn':
            print 'starte blastn'
        elif helperInstance.checkParameter('Annotate', 'program',"parameter.txt") == 'metacv':
            print 'starte metacv'
        else:
            print 'no assembly program recognized! Please check parameter file!'
    else:
        print "skip Step:"+skip
def classify(run):
    if run ==True: 
        
        if helperInstance.checkParameter('Classify', 'program',"parameter.txt") == 'phylosift':
            print 'starte phylosift'
        elif helperInstance.checkParameter('Classify', 'program',"parameter.txt") == '':
            print 'starte metacv'
        else:
            print 'no assembly program recognized! Please check parameter file!'
    else:
        print "skip Step:"+skip
def initPipeline():
    
    preProcessing(helperInstance.skipStep(skip,'PreProcessing'))
    assembly(helperInstance.skipStep(skip,'Assembly'))
    annotate(helperInstance.skipStep(skip,'Annotate'))
    classify(helperInstance.skipStep(skip,'Classify'))
    
    
initPipeline()
