#!/usr/bin/env python

from bin.misc import helper
import ConfigParser
    
def preProcessing(helperInstance):
    pass
   # if helperInstance.checkParameter('PreProcessing','program') == 'FastQC':
   #     print 'starte metavelvet'
   # elif helperInstance.checkParameter('Assembly','program') == 'abyss':
   #         print 'starte abyss'
   # elif helperInstance.checkParameter('Assembly','program') == 'metaidba':
   #     print 'starte metaidba'
   # elif helperInstance.checkParameter('Assembly','program') == 'stitch':
   #     print "starte stitch"
   # else:
   #     print 'no assembly program recognized! Please check parameter file!'


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
        
def main():
    helperInstance = helper("parameter.txt")
    
    preProcessing(helperInstance)
    assembly(helperInstance)
    annotate(helperInstance)
    classify(helperInstance)
    
    
main()