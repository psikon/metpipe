#!/usr/bin/env python

#import necessary packages
from bin.fileHandler import fileHandler
from bin.parser import parser

#define global variables
parser = parser()
input = parser.getInput()
threads = parser.getThreads()

conf = parser.getAllfromSection("Assembly")
print "Global: ", input, threads
print conf
#fileHandler = fileHandler("RAW","unprocessed","RAW","qualityCheck",parser.getInput(),"fastq",parser.getParamsFile())
#if parser.getParamsFile() == True:
#    parser.setPath(parser.getArgs().get("--param"))
#    print parser.getParamsFile()
    
 



