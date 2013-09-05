# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.utils import ParamFileArguments
from src.settings import RunSettings, Executables, blastParser, Rannotate, subsetDB
from src.file_functions import create_outputdir, str_input, update_reads, is_xml, remove_file
from src.log_functions import Logging

class Analysis:
    
    # input 
    blast_output = ''
    metacv_output = ''
    
    # output
    output = ''
    parsed_db_out = ''
    annotated_db_out = ''
    subseted_db_out = ''
    logdir = ''
    
    krona = False
   
    
    def __init__(self, files_instance, krona):
        self.log = Logging()
        self.exe = Executables()
        self.files = files_instance
        self.output = self.files.get_output()
        self.parsed_db_out = self.files.get_parsed_db_dir()
        self.annotated_db_out = self.files.get_annotated_db_dir()
        self.subseted_db_out = self.files.get_subseted_db_dir()
        self.blast_output = self.files.get_blastn_output()
        self.metacv_output = self.files.get_metacv_output()
        self.logdir = self.files.get_logdir()
        self.krona = krona
        
        #self.parse_to_db(self.blast_output, self.parsed_db_out)
        self.files.set_parser_output(update_reads(self.parsed_db_out, blastParser().get_name(), 'db'))
        self.annotate_db(self.files.get_parser_output(), self.annotated_db_out)
        
        #if parse_to_db(self.blast_out, self.parsed_db_out):
        #    annotate_db()
        
    
    def __del__(self):
        pass

    def parse_to_db(self, input, output):
        
        # create a dir for output
        create_outputdir(output)
        # generate filename for db
        outfile = output + os.sep + blastParser().get_name() + '.db'
        # remove old databases with same name
        if os.path.exists(outfile):
            os.remove(outfile)
        # print actual informations about the step on stdout
        self.log.print_step(RunSettings.step_number, 'Analysis', 'Parse database from blast results',
                            ParamFileArguments(blastParser()))
        # start the parser and wait until completion
        p = subprocess.Popen(shlex.split('%s -o %s %s %s' % (self.exe.PARSER,
                                                             outfile,
                                                             ParamFileArguments(blastParser()),
                                                             input)),
                              stdout = subprocess.PIPE,
                              stderr = self.log.open_logfile(self.logdir + 'parser.err.log'))
        # print information about the status
        while p.poll() is None:
            if RunSettings.verbose:
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is complete        
        p.wait()
        
    def annotate_db(self, input, output):
        
        create_outputdir(output)
        
        outfile = output + os.sep + Rannotate().get_name() + '.db'
        print outfile
        
        if os.path.exists(outfile):
            os.remove(outfile)

        p = subprocess.Popen(shlex.split('%s -i %s -o %s' % (self.exe., input, outfile)))
    