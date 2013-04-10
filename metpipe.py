#!/usr/bin/env python

"""metpipe

Usage: 
    metpipe [options] <THREADS> <INPUT> ... 

Arguments
    THREADS    number of cores for processing
    INPUT      Input files (single|paired) in <fastq> format
    
Options:
-h                show this help message and exit
--version         show version and exit
-q                print no status messsages to stdout.
--skip            skip steps in the pipeline.
--params=<FILE>   use alternate parameter file [default: parameter.conf].

"""
# global imports
import time, os, sys, datetime, string, shutil
from bin.docopt import docopt

# import own Classes
from bin.fileHandler import fileHandler
from bin.parser import parser
from bin.programs import Programs

# init 

# get commandline arguments
cli = docopt(__doc__, help=True, version="metpipe 0.1 alpha", options_first=False)
# init global variables
quiet = cli.get("-q")
threads = cli.get('<THREADS>')
skip = cli.get("--skip")
config = parser(cli.get("--params"))
workingStack = []
program = Programs()


#if skip != "PreProcessing":
workingStack.append(fileHandler("RAW","RAW","RAW",program.fastqc,cli.get('<INPUT>'),
                                    "fastq",config.getAllfromSection("PreProcessing")))

while(workingStack): 
    actualElement = workingStack.pop()
    program.setfileHandler(actualElement)
    nextElement = actualElement.getDestination()()
    if nextElement != None:
        workingStack.append(nextElement)

print "workingStack leer"



