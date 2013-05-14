#!/usr/bin/env python

# First imports
import os, sys

# Setting up the paths
SRC_DIR = "%s%ssrc" % (sys.path[0], os.sep)
PROGRAM_DIR = "%s%sprogram" % (sys.path[0], os.sep)
RESULT_DIR = "%s%sresult" % (sys.path[0], os.sep)

# hardcode defaults
PARAM_FILE = "%s%sparameter.conf" % (sys.path[0], os.sep)
DEFAULT_KMER = 85
STEPS = {'preprocessing', 'annotate', 'assembly'}
PROGRAM_LIST = {'blastn', 'metacv', 'metavelvet', 'concat'}

# rest of imports
import time
import argparse
import multiprocessing
from socket import errno
from collections import deque
# import own functions and classes 
from src.utils import consoleSummary, createTasks
from src.settings import Settings
from src.programs import Programs

# Get the starting time
starting_time = time.time()

# define cli
if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input', nargs='+', action='store', help='single or paired input files in <fastq> format')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False,
                        help='more detailed output (default=False)')
    parser.add_argument('-t', dest='threads', type=int, action='store', default=multiprocessing.cpu_count() - 1,
                        help='number of threads to use (default=%d)' % (multiprocessing.cpu_count() - 1))
    parser.add_argument('-p', dest='param', action='store', default=PARAM_FILE,
                        help='use alternative config file (default=parameter.conf)')
    parser.add_argument('-s', dest='skip', action='store', default='', choices=['Preprocessing', 'Assembly',
                        'Annotation'], help='skip steps in the pipeline (default=None)')
    parser.add_argument('-o', dest='output', action='store', default=RESULT_DIR,
                        help='use alternative output folder')
    parser.add_argument('-a', dest='assembler', default='MetaVelvet', choices=['metavelvet', 'concat'],
                        help='assembling program to use (default= MetaVelvet)')
    parser.add_argument('-k', dest='kmer', type=int, default=DEFAULT_KMER,
                        help='k-mer size to be used (default=' + str(DEFAULT_KMER) + ')')
    parser.add_argument('-c', dest='classify', choices=['metacv', 'blastn', 'both'], default='both',
                        help='classifier to use for annotation (default= both)')                                      
    parser.add_argument('--notrimming', dest='trim', action='store_false', default=True,
                        help='trimm and filter input reads? (default=True)')
    parser.add_argument('--noquality', dest='quality', action='store_false', default=True,
                        help='create quality report (default=True)')
# create the cli interface
args = parser.parse_args()

# check some conditions 

# check if input exists
for fname in args.input:
    if not os.path.isfile(fname):
        print ("File:  %s not exists" % (fname))
        sys.exit()
        
# check if output dir exists and create it if not
try:
    os.makedirs(args.output)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
    
# check if param File exists
if not os.path.isfile(args.param):
    print ('param file %s is not readable' % (args.param))
    sys.exit()

# create the global settings object
settings = Settings(args.kmer, args.threads, PROGRAM_DIR, args.verbose, args.skip, args.input,
                    args.output, args.param, args.trim, args.quality, args.assembler, args.classify)

# fill the pipeline with tasks
queue = deque([])
queue = createTasks(settings,Programs())
# print the summary of the settings
consoleSummary(settings)

# working queue - run until queue is empty or an error occured
while(queue):
    actualElement = queue.popleft()
    if actualElement.getTask()(actualElement.getOutputDir()):
        continue
    else: 
        print "error"
        sys.exit()
        
