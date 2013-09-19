# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.settings import Executables, blastParser, Rannotate, subsetDB, Krona_Parameter
from src.file_functions import create_outputdir, update_reads, remove_file, parse_parameter, extract_tabular
from src.log_functions import Logging
from src.utils import to_string, is_xml, is_tabular, is_db, is_executable

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
    # misc
    parameter_file = ''
    krona = False
    exitcode = ''
    
    def __init__(self, files_instance, settings_instance, parameter_file, krona):
        # init all important variables and classes
        self.settings = settings_instance
        self.parameter_file = parameter_file
        self.log = Logging()
        self.exe = Executables(self.parameter_file)
        self.files = files_instance
        self.logdir = self.files.get_logdir()
        self.krona = krona
        # set the paths for the output
        self.output = self.files.get_output()
        self.parsed_db_out = self.files.get_parsed_db_dir()
        self.annotated_db_out = self.files.get_annotated_db_dir()
        self.subseted_db_out = self.files.get_subseted_db_dir()
        self.krona_report_out = self.files.get_krona_report_dir()
        # get the input 
        self.blast_output = self.files.get_blastn_output()
        self.metacv_output = self.files.get_metacv_output()
        
        # test for blastrun with outfmt 5 mode
        if is_xml(self.blast_output):
            
            # create a SQLite DB from the xml file
            self.parse_to_db(self.blast_output, self.parsed_db_out)
            # test the exit code, because next script need the output as input
            if self.exitcode is 0:
                # update input 
                self.files.set_parser_output(update_reads(self.parsed_db_out, blastParser(self.parameter_file).get_name(), 'db'))
                # raise step_number
                self.settings.set_step_number()
                # create a new database with taxonomical annotations
                self.annotate_db(self.files.get_parser_output(), self.annotated_db_out)
                # test the exit code, because next script need the output as input
                if self.exitcode is 0:
                    # update input
                    self.files.set_annotated_output(update_reads(self.annotated_db_out, Rannotate(self.parameter_file).get_name(), 'db'))
                    # raise step_number
                    self.settings.set_step_number()
                    # subset the taxonomical database for a better and 
                    # faster analysis after the pipline has finished
                    self.subset_db(self.files.get_annotated_output(), self.subseted_db_out)
                    # raise step_number
                    self.settings.set_step_number()
                else:
                    self.log.print_verbose("ERROR: Annotated Database could not be subseted correctly") 
                # create a pie chart of the blast data with Krona Webtools 
                if krona:
                    self.krona_report(self.blast_output, self.krona_report_out)     
            else: 
                self.log.print_verbose("ERROR: XML file could not be parsed")
        # test for blast tabular output
        elif is_tabular(self.blast_output) and krona is True:
            self.krona_report(self.blast_output, self.krona_report_out)
        else:
            self.log.print_verbose("ERROR: Blast output file is not in xml or tabular format.\n",
                                   "Please use outfmt 5 or 6 for Blast run")
    
    def __del__(self):
        pass

    def parse_to_db(self, input, output):

        # create a dir for output
        create_outputdir(output)
        # generate filename for db
        outfile = output + os.sep + blastParser(self.parameter_file).get_name() + '.db'
        # remove old databases with same name
        if os.path.exists(outfile):
            os.remove(outfile)
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Analysis', 
                            'Parse database from blast results',
                            parse_parameter(blastParser(self.parameter_file)))
        # start the parser and wait until completion
        p = subprocess.Popen(shlex.split('%s -o %s %s %s' % (self.exe.PARSER,
                                                             outfile,
                                                             parse_parameter(blastParser(self.parameter_file)),
                                                             to_string(input))),
                              stdout = subprocess.PIPE,
                              stderr = self.log.open_logfile(self.logdir + 'parser.err.log'))
        
        # print information about the status
        while p.poll() is None:
            if self.settings.get_verbose():
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is complete        
        p.wait()
        # save the exit code for later function calls 
        self.exitcode = p.returncode
        
        # print summary of the process after completion
        self.log.print_verbose('Parsing of blast XML File complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - self.settings.get_actual_time()) 
                               + '\n')
        self.log.newline
        
    def annotate_db(self, input, output):

        # create a dir for output
        create_outputdir(output)
        # generate filename for db
        outfile = output + os.sep + Rannotate(self.parameter_file).get_name() + '.db'
        # open a logfile for annotation process
        logfile = self.log.open_logfile(self.logdir + 'annotation_of_db.log')
        
        # remove old databases with same name
        if os.path.exists(outfile):
            os.remove(outfile)
        
        # print actual informations about the step on stdout    
        self.log.print_step(self.settings.get_step_number(), 'Analysis', 
                            'Annotate taxonomical data to blast database',
                            parse_parameter(Rannotate(self.parameter_file)))
        # start the parser and wait until completion
        p = subprocess.Popen(shlex.split('%s -i %s -o %s %s --taxon %s' 
                                         % (self.exe.ANNOTATE, 
                                            to_string(input), 
                                            outfile, 
                                            parse_parameter(Rannotate(self.parameter_file)),
                                            Rannotate(self.parameter_file).get_taxon_db())),
                             stdout = subprocess.PIPE)
        
        # print information about the status
        while p.poll() is None:
            if self.settings.get_verbose():
                self.log.print_verbose(p.stdout.readline())
                logfile.write(p.stdout.readline())
            else:
                logfile.write(p.stdout.readline())
        # wait until process is complete
        p.wait()
        # save the exit code for later function calls 
        self.exitcode = p.returncode
        
        # print summary of the process after completion
        self.log.print_verbose('Taxonomical annotation of blast database complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - self.settings.get_actual_time()) 
                               + '\n')
        self.log.newline
        
    def subset_db(self, input, output):
        
        # create a dir for output
        create_outputdir(output)
        # create a subset Object to access the classifier and rank lists
        subsetting = subsetDB(self.parameter_file)
        
        # because of multiple possible classifier the database will be subseted in a loop,
        # so that every classifier can be processed
        for i in range(len(subsetting.get_classifier())):
            # print actual informations about the step on stdout    
            self.log.print_step(self.settings.get_step_number(), 
                                'Analysis', 
                                'Subset the database for %s' % (subsetting.get_classifier()[i]),
                                '--bitscore %s --rank %s' % (subsetting.get_bitscore(),
                                                             subsetting.get_rank()[i]))
            
            # generate name for database file
            outfile = '%s%s%s%s' % (output, os.sep, subsetting.get_classifier()[i], '.db') 
            logfile = self.log.open_logfile(self.logdir + subsetting.get_classifier()[i] + '.log')
            
            # remove old databases with the same name
            if os.path.exists(outfile):
                os.remove(outfile)
                
            # start the process with classifier i and the complete output from the annotation step before
            p = subprocess.Popen(shlex.split('%s -i %s -o %s --classifier %s --bitscore %s --rank %s --taxon %s --blast %s' 
                                             % (self.exe.SUBSET, 
                                                to_string(input), 
                                                outfile,
                                                subsetting.get_classifier()[i],
                                                subsetting.get_bitscore(),
                                                subsetting.get_rank()[i],
                                                subsetting.get_taxon_db(),
                                                to_string(self.files.get_parser_output()))),
                                 stdout = subprocess.PIPE)
            
            # during processing print output in verbose mode and update the logfile
            while p.poll() is None:
                if self.settings.get_verbose():
                    self.log.print_verbose(p.stdout.readline())
                    logfile.write(p.stdout.readline())
                else:
                    logfile.write(p.stdout.readline())
            # wait until process is complete
            p.wait()
            
            self.log.newline
            
        # print summary of the process after completion
        self.log.print_verbose('Subsetting of annotated Blast database complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - self.settings.get_actual_time()) 
                               + '\n')
        self.log.newline
       
    def krona_report(self, input, output):
        
        # create a dir for output
        create_outputdir(output)
        # generate path and name for output file
        outfile = output + os.sep + Krona_Parameter(self.parameter_file).get_name() + '.html'
        
        # test type of input file
        if is_tabular(input):
            # print actual informations about the step on stdout    
            self.log.print_step(self.settings.get_step_number(), 
                                'Analysis', 
                                'Create Overview from tabular output',
                                parse_parameter(Krona_Parameter(self.parameter_file)))
            
            # start the Krona import script for Blast tabular output
            # pipe all output for stdout in a logfile
            p = subprocess.Popen(shlex.split('%s -o %s %s %s' % (self.exe.KRONA_BLAST,
                                                                 outfile,
                                                                 parse_parameter(Krona_Parameter(self.parameter_file)),
                                                                 to_string(input))),
                                 stdout = self.log.open_logfile(self.logdir + 'krona.log'),
                                 stderr = self.log.open_logfile(self.logdir + 'krona.err.log'))
            # wait until process is complete
            p.wait()
            
        elif is_xml(input) and is_db(self.files.get_parser_output()):
            self.log.print_step(self.settings.get_step_number(), 
                                'Analysis', 
                                'Create Overview from XML output',
                                parse_parameter(Krona_Parameter(self.parameter_file)))
            # convert the values from database to tabular format
            extract_tabular(to_string(self.files.get_parser_output()),output)
            # set the new input
            input = update_reads(output,'extracted_from_DB','tab')
            
            # start the Krona import script for Blast tabular output
            # pipe all output for stdout in a logfile
            p = subprocess.Popen(shlex.split('%s -o %s %s %s' % (self.exe.KRONA_BLAST,
                                                                 outfile,
                                                                 parse_parameter(Krona_Parameter(self.parameter_file)),
                                                                 to_string(input))),
                                 stdout = self.log.open_logfile(self.logdir + 'krona.log'),
                                 stderr = self.log.open_logfile(self.logdir + 'krona.err.log'))
            
        elif not is_tabular(input) or not is_xml(input):
            self.log.print_verbose('Input must be in Blast table or xml format \n' + 
                                   'change Blast Parameter "outfmt" to 5 or 6')
            errorlog.write('Input must be in Blast table or xml format \n' + 
                               'change Blast Parameter "outfmt" to 5 or 6')
        else:
            self.log.print_verbose('Krona Report could not be generated, because of unknown reasons')
            
        
        
