#!/usr/bin/env python

from bin.misc import Helper
from bin.preprocessing import PreProcessing
import ConfigParser
    
def preProcessing(helperInstance):

    if helperInstance.checkParameter('PreProcessing','quality check') == 'yes':
		pre = PreProcessing()
		pre.qualityCheck()
	
    elif helperInstance.checkParameter('PreProcessing','trimming') == 'yes':
            print 'starte Trim Galore!'
    else:
        print 'no PreProcessing Steps chosen.'


def assembly(helperInstance):

    if helperInstance.checkParameter('Assembly','program') == 'metavelvet':
        print 'starte metavelvet'
    elif helperInstance.checkParameter('Assembly','program') == 'abyss':
            print 'starte abyss'
    elif helperInstance.checkParameter('Assembly','program') == 'metaidba':
        print 'starte metaidba'
    elif helperInstance.checkParameter('Assembly','program') == 'stitch':
        print "starte stitch"
    else:
        print 'no assembly program recognized! Please check parameter file!'

def annotate(helperInstance):

    if helperInstance.checkParameter('Annotate','program') == 'blastn':
        print 'starte blastn'
    elif helperInstance.checkParameter('Annotate','program') == 'metacv':
        print 'starte metacv'
    else:
        print 'no assembly program recognized! Please check parameter file!'
        
def classify(helperInstance):
    
    if helperInstance.checkParameter('Classify','program') == 'phylosift':
        print 'starte phylosift'
    elif helperInstance.checkParameter('Classify','program') == '':
            print 'starte metacv'
    else:
        print 'no assembly program recognized! Please check parameter file!'
        
def initPipeline():
    helperInstance = Helper("parameter.txt")
    
    preProcessing(helperInstance)
    assembly(helperInstance)
    annotate(helperInstance)
    classify(helperInstance)
    
    
initPipeline()
