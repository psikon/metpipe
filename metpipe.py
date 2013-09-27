#!/usr/bin/env python

#@author: Philipp Sehnert
#@contact: philipp.sehnert[a]gmail.com

# import of standard modules
import os, sys, time, multiprocessing
import argparse
# Import of pipeline modules
from src.preprocess import Preprocess
from src.assembly import Assembly
from src.annotation import Annotation
from src.analysis import Analysis
from src.settings import General, FileSettings
from src.utils import file_exists, to_string
from src.log_functions import Logging
from src.file_functions import create_outputdir

# hardcode defaults
RESULT_DIR = '%s%sresult' % (sys.path[0], os.sep)
PARAM_FILE = '%s%sparameter.conf' % (sys.path[0], os.sep)
STEPS = ['preprocessing', 'annotate', 'assembly']

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
                        choices = ['preprocessing', 'assembly', 'annotation','analysis'],
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

# init the Pipeline

PARAM_FILE = args.param if args.param else PARAM_FILE
RESULT_DIR = args.output if args.output else RESULT_DIR

# check if input exists
for fname in args.input:
   file_exists(fname)

# check if param File exists
file_exists(PARAM_FILE)
     
# create outputdir and log folder
create_outputdir(RESULT_DIR)
create_outputdir(RESULT_DIR + os.sep +'log')

# create the global settings object
settings = General(args.threads, args.verbose, args.skip, starting_time, args.trim, 
                   args.quality, args.use_contigs, args.assembler, args.classify, 1)

# setup the input, outputs and important files
files = FileSettings(args.input, os.path.normpath(RESULT_DIR), PARAM_FILE)

# create the Logger interface
log = Logging()

# get the all skipped steps
skip = to_string(settings.get_skip())

# START the modules of Pipeline and wait until completion
if skip in 'preprocessing' and skip:
   log.skip_msg(skip)
else:   
    Preprocess(files, settings, PARAM_FILE)

# if skip in 'assembly' and skip:
#      log.skip_msg(skip)
# else:
#     Assembly(files, settings, PARAM_FILE, settings.assembler)
#      
# if skip in 'annotation'and skip:
#      log.skip_msg(skip)
# else:
#     Annotation(files, settings, PARAM_FILE, settings.classify)
#      
# if skip in 'analysis' and skip:
#      log.skip_msg(skip)
# else:
#     Analysis(files, settings, PARAM_FILE, True)

# print ending message
sys.stdout.write('\nPIPELINE COMPLETE!\n\n')
log.print_running_time(settings.get_actual_time())

