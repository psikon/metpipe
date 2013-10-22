#!/usr/bin/env python

#@author: Philipp Sehnert
#@contact: philipp.sehnert[a]gmail.com

# import of standard modules
import os, sys, time, multiprocessing
import argparse
import traceback
# Import of pipeline modules
from src.preprocess import Preprocess
from src.assembly import Assembly
from src.annotation import Annotation
from src.analysis import Analysis
from src.settings import *
from src.utils import file_exists, to_string
from src.log_functions import skip_msg, print_verbose, print_running_time
from src.file_functions import create_outputdir, parse_parameter, absolute_path
from src.exceptions import InputNotFound, ParamFileNotFound

# hardcode defaults
RESULT_DIR = '%s%sresult' % (sys.path[0], os.sep)
PARAM_FILE = '%s%sparameter.conf' % (sys.path[0], os.sep)
STEPS = ['preprocessing', 'annotate', 'assembly', 'analysis']

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
    parser.add_argument('-c', dest = 'annotation', default = 'both',
                        choices = ['metacv', 'blastn', 'both'],
                        help = 'classifier to use for annotation (default = both)')     
    parser.add_argument('--use_contigs', dest = 'use_contigs', action = 'store_true', 
                        default = 'False',
                        help = 'should MetaCV use assembled Reads or RAW Reads (default = RAW')                                    
    parser.add_argument('--notrimming', dest = 'trim', action = 'store_false', default = True,
                        help = 'trim and filter input reads? (default = True)')
    parser.add_argument('--noquality', dest = 'quality', action = 'store_false', default = True,
                        help = 'create no quality report (default = True)')
    parser.add_argument('--noreport', dest = 'krona', action = 'store_false', default = True,
                        help = 'create no pie chart with the annotated taxonomical data (default = True)')
    parser.add_argument('--merge', dest = 'merge_uncombined', action = 'store_true', default = False,
                        help = 'merge concatinated reads with not concatinated (default = False)')
    
# create the cli interface
args = parser.parse_args()

# init the Pipeline
RESULT_DIR = args.output if args.output else RESULT_DIR
# check if param File exists
if os.path.isfile(args.param):
    PARAM_FILE = args.param
else:
    if os.path.isfile(PARAM_FILE):
        sys.stderr.write('ERROR 3: Parameter File could not be found!\n')
        sys.stderr.write('Use standard Parameter File:\n%s\n\n' % (PARAM_FILE))
    else:
        raise ParamFileNotFound(args.param)
    
# check if input exists
if not all(os.path.isfile(file) for file in args.input):
    raise InputNotFound(to_string(args.input))


     
# create outputdir and log folder
create_outputdir(RESULT_DIR)
create_outputdir(RESULT_DIR + os.sep +'log')

# create the global settings object
settings = General(args.threads, args.verbose, args.skip, starting_time, args.trim, 
                   args.quality, args.krona, args.use_contigs, args.merge_uncombined, args.assembler, 
                   args.annotation, 1)

# setup the input, outputs and important files
files = FileSettings(absolute_path(args.input), os.path.normpath(RESULT_DIR), PARAM_FILE)

exe = Executables(PARAM_FILE)
# get the all skipped steps
skip = to_string(settings.get_skip())

try:
    # START the modules of Pipeline and wait until completion
    if skip in 'preprocessing' and skip:
        skip_msg(skip)
    else:
        # init the preprocessing module
        pre = Preprocess(settings.get_threads(), 
                         settings.get_step_number(),
                         settings.get_verbose(),
                         settings.get_actual_time(),
                         files.get_input(),
                         files.get_logdir(),
                         exe.get_FastQC(),
                         settings.get_quality(),
                         files.get_quality_dir(),
                         parse_parameter(FastQC_Parameter(PARAM_FILE)),
                         exe.get_TrimGalore(),
                         settings.get_trim(),
                         files.get_trim_dir(), 
                         parse_parameter(TrimGalore_Parameter(PARAM_FILE)))
        # run preprocessing functions
        results = pre.manage_preprocessing()
        # update pipeline variables with results
        settings.set_step_number(results[0])
        files.set_input(absolute_path(results[1]))
        files.set_preprocessed_output(absolute_path(results[1]))

    if skip in 'assembly' and skip:
        skip_msg(skip)
    else:
        # init the assembly module 
        assembly = Assembly(settings.get_threads(), 
                            settings.get_step_number(),
                            settings.get_verbose(),
                            settings.get_actual_time(),
                            files.get_logdir(),
                            files.get_input(),
                            settings.get_assembler(),
                            exe.get_Flash(),
                            files.get_concat_dir(),
                            parse_parameter(FLASH_Parameter(PARAM_FILE)),
                            settings.get_merge_uncombined(),
                            exe.get_Velveth(),
                            exe.get_Velvetg(),
                            exe.get_MetaVelvet(),
                            files.get_assembly_dir(),
                            Velveth_Parameter(PARAM_FILE).get_kmer(PARAM_FILE),
                            parse_parameter(Velveth_Parameter(PARAM_FILE)),
                            parse_parameter(Velvetg_Parameter(PARAM_FILE)),
                            parse_parameter(MetaVelvet_Parameter(PARAM_FILE)))
        # run assembly functions
        results = assembly.manage_assembly()
        # update pipeline variables with results
        settings.set_step_number(results[0])
        files.set_input(absolute_path(results[1]))
        files.set_concatinated_output(absolute_path(results[2]))
        files.set_assembled_output(absolute_path(results[3]))
  
    if skip in 'annotation'and skip:
        skip_msg(skip)
    else:
        # init the annotation module
        anno = Annotation(settings.get_threads(), 
                          settings.get_step_number(),
                          settings.get_verbose(),
                          settings.get_actual_time(),
                          files.get_logdir(),
                          files.get_input(),
                          files.get_raw(),
                          settings.get_annotation(),
                          settings.get_use_contigs(),
                          exe.get_Blastn(),
                          exe.get_Blastn_DB(),
                          exe.get_Converter(),
                          files.get_blastn_dir(),
                          Blastn_Parameter(PARAM_FILE).outfmt,
                          parse_parameter(Blastn_Parameter(PARAM_FILE)),
                          exe.get_MetaCV(),
                          exe.get_MetaCV_DB(),
                          files.get_metacv_dir(),
                          MetaCV_Parameter(PARAM_FILE).get_seq(),
                          MetaCV_Parameter(PARAM_FILE).get_mode(),
                          MetaCV_Parameter(PARAM_FILE).get_orf(),
                          MetaCV_Parameter(PARAM_FILE).get_total_reads(),
                          MetaCV_Parameter(PARAM_FILE).get_min_qual(),
                          MetaCV_Parameter(PARAM_FILE).get_taxon(),
                          MetaCV_Parameter(PARAM_FILE).get_name())
        # run the annotation functions
        results = anno.manage_annotation()
        settings.set_step_number(results[0])
        files.set_blastn_output(absolute_path(results[1]))
        files.set_metacv_output(absolute_path(results[2]))
      
    if skip in 'analysis' and skip:
        skip_msg(skip)
    else:
        # init the analysis module
        analysis = Analysis(settings.get_threads(),
                            settings.get_step_number(),
                            settings.get_verbose(),
                            settings.get_actual_time(),
                            files.get_logdir(),
                            settings.get_annotation(),
                            files.get_output(),
                            files.get_parsed_db_dir(),
                            files.get_annotated_db_dir(),
                            files.get_subseted_db_dir(),
                            files.get_krona_report_dir(),
                            files.get_blastn_output(),
                            files.get_metacv_output(),
                            exe.get_Parser(), 
                            parse_parameter(blastParser_Parameter(PARAM_FILE)),
                            blastParser_Parameter(PARAM_FILE).get_name(),
                            exe.get_Annotate(),
                            parse_parameter(Rannotate_Parameter(PARAM_FILE)),
                            Rannotate_Parameter(PARAM_FILE).get_name(),
                            Rannotate_Parameter(PARAM_FILE).get_taxon_db(),
                            exe.get_Subset(),
                            subsetDB_Parameter(PARAM_FILE).get_bitscore(),
                            subsetDB_Parameter(PARAM_FILE).get_classifier(),
                            subsetDB_Parameter(PARAM_FILE).get_rank(),
                            subsetDB_Parameter(PARAM_FILE).get_taxon_db(),
                            exe.get_Krona_Blast(),
                            parse_parameter(Krona_Parameter(PARAM_FILE)),
                            Krona_Parameter(PARAM_FILE).get_name(),
                            settings.get_krona(),
                            exe.get_Perl_lib())
        # run the analysis function
        results = analysis.manage_analysis()
        files.set_parser_output(absolute_path(results[0]))
        files.set_annotated_output(absolute_path(results[1]))    
        
except KeyboardInterrupt:
    sys.stdout.write('\nERROR 1 : Operation cancelled by User!\n')
    sys.exit(1)

# print ending message
print_verbose('\nPIPELINE COMPLETE!\n\n')
print_running_time(settings.get_actual_time())
