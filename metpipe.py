#!/usr/bin/env python

# First imports
import os, sys

# Setting up the paths
RESULT_DIR = '%s%sresult' % (sys.path[0], os.sep)

# hardcode defaults
PARAM_FILE = '%s%sparameter.conf' % (sys.path[0], os.sep)
DEFAULT_KMER = 85
STEPS = {'preprocessing', 'annotate', 'assembly'}

# rest of imports
import time
import argparse
import multiprocessing
from socket import errno
# import own functions and classes 
from src.settings import General, FileSettings
from src.preprocess import *
from src.assembly import *
from src.annotation import *
from src.analysis import *
from src.file_functions import update_reads
from src.log_functions import Logging

# Get the starting time
starting_time = time.time()

# define cli
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = True)
    parser.add_argument('input', nargs = '+', action = 'store', 
                        help = 'single or paired input files in <fastq> format')
    parser.add_argument('--version', action = 'version', version = '%(prog)s 0.5')
    parser.add_argument('-v', dest = 'verbose', action = 'store_true', default = False,
                        help = 'more detailed output (default = False)')
    parser.add_argument('-t', dest = 'threads', type = int, action = 'store', 
                        default = multiprocessing.cpu_count() - 1,
                        help = 'number of threads to use (default = %d)' 
                        % (multiprocessing.cpu_count() - 1))
    parser.add_argument('-p', dest = 'param', action = 'store', default = PARAM_FILE,
                        help = 'use alternative config file (default = parameter.conf)')
    parser.add_argument('-s', dest = 'skip', action = 'store', default = '', 
                        choices = ['Preprocessing', 'Assembly', 'Annotation'],
                        help = 'skip steps in the pipeline (default = None)')
    parser.add_argument('-o', dest = 'output', action = 'store', default = RESULT_DIR,
                        help = 'use alternative output folder')
    parser.add_argument('-a', dest = 'assembler', default = 'MetaVelvet', 
                        choices = ['metavelvet', 'flash','both'],
                        help = 'assembling program to use (default = MetaVelvet)')
    parser.add_argument('-c', dest = 'classify', default = 'both',
                        choices = ['metacv', 'blastn', 'both'],
                        help = 'classifier to use for annotation (default = both)')     
    parser.add_argument('--use_contigs', dest = 'use_contigs', action = 'store_true', 
                        default = 'False',
                        help = 'should MetaCV use assembled Reads or RAW Reads (default = RAW')                                    
    parser.add_argument('--notrimming', dest = 'trim', action = 'store_false', default = True,
                        help = 'trimm and filter input reads? (default = True)')
    parser.add_argument('--noquality', dest = 'quality', action = 'store_false', default = True,
                        help = 'create quality report (default = True)')
    
# create the cli interface
args = parser.parse_args()


# check if input exists
for fname in args.input:
    if not os.path.isfile(fname):
        print ('File:  %s not exists' % (fname))
        sys.exit()
        
# check if output dir exists and create it if not
try:
    os.makedirs(args.output)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

# create the log folder
try:
    os.makedirs(args.output + os.sep + 'log')
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
    
# check if param File existsObjekt orientiert entwickelt 
if not os.path.isfile(args.param):
    print ('param file %s is not readable' % (args.param))
    sys.exit()

parameter_file = args.param
# create the global settings object
settings = General(args.threads, args.verbose, args.skip, starting_time, 
                   args.trim, args.quality, args.use_contigs, args.assembler, args.classify, 1)

files = FileSettings(args.input, os.path.normpath(args.output), parameter_file)
log = Logging()

# Testaufrufe
#preprocess = Preprocess(files, settings, parameter_file)
#assembly = Assembly(files, settings, parameter_file, settings.assembler)
#annotate = Annotation(files, settings, parameter_file, settings.classify)
files.set_blastn_output(update_reads(files.get_blastn_dir(),"blast",'xml'))
analysis = Analysis(files, settings, parameter_file, True)

sys.stdout.write('\nPIPELINE COMPLETE!\n\n')
sys.stdout.write('processed in ' + log.getDHMS(time.time() - settings.get_actual_time())+'\n')
