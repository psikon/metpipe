# standard imports
import subprocess
import shlex
import sys, os, time
import shutil
# imports of own functions and classes
from src.file_functions import create_outputdir, update_reads, remove_file, parse_parameter, extract_tabular
from src.log_functions import print_step, newline, print_compact, print_verbose, open_logfile, print_running_time, remove_empty_logfile, cut_path
from src.utils import to_string, is_xml, is_tabular, is_db, is_executable
from src.exceptions import ParserException, AnnotateDBException, SubsetDBException, KronaException, KronaFormatException

class Analysis:
    
    # input 
    blast_output = ''
    metacv_output = ''
    
    # output
    parsed_db_out = ''
    annotated_db_out = ''
    subseted_db_out = ''
    logdir = ''
    # misc
    parameter_file = ''
    krona = False
    exitcode = ''
    
    def __init__(self, threads, step_number, verbose, time, logdir, classify, output, 
                 parsed_db_dir, annotated_db_dir, subseted_db_dir, krona_report_dir, 
                 blast_output, metacv_output,parser_exe, parser_parameter, parser_name,
                 annotate_exe, annotate_parameter, annotate_name, annotate_taxon_db, 
                 subset_exe, subset_bitscore, subset_classifier, subset_rank,
                 subset_taxon_db, krona_exe, krona_parameter, krona_name, krona):
        
        # init general variables
        self.threads = threads
        self.step_number = step_number
        self.verbose = verbose
        self.time = time
        self.logdir = logdir
        self.annotation_mode = classify
        

        self.parsed_db_out = parsed_db_dir
        self.annotated_db_out = annotated_db_dir
        self.subseted_db_out = subseted_db_dir
        self.krona_report_out = krona_report_dir
        # get the input 
        self.blast_output = blast_output
        self.metacv_output = metacv_output
        
        # blastparser variables
        self.parser_exe = parser_exe
        self.parser_parameter = parser_parameter
        self.parser_name = parser_name
        
        # Analysis with R 
        self.R_annotate_exe = annotate_exe
        self.R_annotate_parameter = annotate_parameter
        self.R_annotate_name = annotate_name
        self.R_annotate_taxon_db = annotate_taxon_db
        self.R_subset_exe = subset_exe
        self.R_subset_bitscore = subset_bitscore
        self.R_subset_classifier = subset_classifier
        self.R_subset_rank = subset_rank
        self.R_subset_taxon_db = subset_taxon_db
        
        # init Krona variables
        self.krona_exe = krona_exe
        self.krona_parameter = krona_parameter
        self.krona_name = krona_name
        self.krona = krona
        
        
    def __del__(self):
        pass
    
    def manage_analysis(self):
        
       
        if self.annotation_mode in 'metacv':
            print_verbose("For a detailed analysis blastn with XML output is needed")
        else:
            # test for blastrun with outfmt 5 mode
            if is_xml(self.blast_output):
                # create a SQLite DB from the xml file
                self.parse_to_db(to_string(self.blast_output), self.parsed_db_out)
                # test the exit code, because next script need the output as input
                if self.exitcode is 0:
                    # update input 
                    parser_out = update_reads(self.parsed_db_out, self.parser_name, 'db')
                    # raise step_number
                    self.step_number += 1
                    # create a new database with taxonomical annotations
                    self.annotate_db(parser_out, self.annotated_db_out)
                    # test the exit code, because next script need the output as input
                    if self.exitcode is 0:
                        # update input
                        annotated_output = update_reads(self.annotated_db_out, self.R_annotate_name, 'db')
                        # raise step_number
                        self.step_number += 1
                        # subset the taxonomical database for a better and 
                        # faster analysis after the pipline has finished
                        self.subset_db(annotated_output, self.subseted_db_out, parser_out)
                        # raise step_number
                        self.step_number += 1
                    else:
                        print_verbose("ERROR: Annotated Database could not be subseted correctly") 
                    # create a pie chart of the blast data with Krona Webtools 
                    if self.krona:
                        self.krona_report(self.blast_output, self.krona_report_out, parser_out)
                        
                    return [parser_out, annotated_output]   
                else: 
                    print_verbose("ERROR: XML file could not be parsed")
            # test for blast tabular output
            elif is_tabular(self.blast_output) and self.krona is True:
                self.krona_report(self.blast_output, self.krona_report_out, '')
                return []
            else:
                print_verbose("ERROR: Blast output file is not in xml or tabular format.\n" +
                              "Please use outfmt 5 or 6 for Blast run")
                return []

    def parse_to_db(self, input, output):
        # create a dir for output
        create_outputdir(output)
        # generate filename for db
        outfile = output + os.sep + self.parser_name + '.db'
        # remove old databases with same name
        if os.path.exists(outfile):
            os.remove(outfile)
            
        # print actual informations about the step on stdout
        print_step(self.step_number, 'Analysis', 
                   'Parse database from blast results',
                   self.parser_parameter)
        newline()

        # start the parser and wait until completion
        p = subprocess.Popen(shlex.split('%s -o %s %s %s' % (self.parser_exe,
                                                             outfile,
                                                             self.parser_parameter,
                                                             input)),
                              stdout = subprocess.PIPE,
                              stderr = open_logfile(self.logdir + 'parser.err.log'))
        
        # print information about the status
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stdout.readline())
            else:
                print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is complete        
        p.wait()
        # save the exit code for later function calls 
        self.exitcode = p.returncode
        # raise Exception when an error occurs during processing
        if p.returncode:
            raise ParserException(self.logdir + 'parser.err.log')
        else:
            # remove empty error logs
            remove_empty_logfile(self.logdir + 'parser.err.log')
            # print summary of the process after completion
            print_verbose('Parsing of blast XML File complete \n')
            print_running_time(self.time)
            newline()
        
    def annotate_db(self, input, output):

        # create a dir for output
        create_outputdir(output)
        # generate filename for db
        outfile = output + os.sep + self.R_annotate_name + '.db'
        # open a logfile for annotation process
        logfile = open_logfile(self.logdir + 'annotation_of_db.log')
        
        # remove old databases with same name
        if os.path.exists(outfile):
            os.remove(outfile)
        
        # print actual informations about the step on stdout    
        print_step(self.step_number, 'Analysis', 
                   'Annotate taxonomical data to blast database',
                   self.R_annotate_parameter)
        newline()
        # start the parser and wait until completion
        p = subprocess.Popen(shlex.split('%s -i %s -o %s %s --taxon %s' 
                                         % (self.R_annotate_exe, 
                                            to_string(input), 
                                            outfile, 
                                            self.R_annotate_parameter,
                                            self.R_annotate_taxon_db)),
                             stdout = subprocess.PIPE)
        
        # print information about the status
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stdout.readline())
                logfile.write(p.stdout.readline())
            else:
                logfile.write(p.stdout.readline())
        # wait until process is complete
        p.wait()
        # save the exit code for later function calls 
        self.exitcode = p.returncode
        
        # raise Exception when an error occurs during processing
        if p.returncode:
            raise AnnotateDBException(self.logdir + 'annotation_of_db.log')
        else:
            # print summary of the process after completion
            print_verbose('Taxonomical annotation of blast database complete \n')
            print_running_time(self.time)
            newline()
        
    def subset_db(self, input, output, parser_out):
        
        # create a dir for output
        create_outputdir(output)
        
        # because of multiple possible classifier the database will be subseted in a loop,
        # so that every classifier can be processed
        for i in range(len(self.R_subset_classifier)):
            # print actual informations about the step on stdout    
            print_step(self.step_number, 
                       'Analysis', 
                       'Subset the database for %s' % (self.R_subset_classifier[i]),
                        '--bitscore %s --rank %s' % (self.R_subset_bitscore,
                                                     self.R_subset_rank[i]))
            newline()
            # generate name for database file
            outfile = '%s%s%s%s' % (output, os.sep, self.R_subset_classifier[i], '.db') 
            logfile = open_logfile(self.logdir + self.R_subset_classifier[i] + '.log')
            
            # remove old databases with the same name
            if os.path.exists(outfile):
                os.remove(outfile)
                
            # start the process with classifier i and the complete output from the annotation step before
            p = subprocess.Popen(shlex.split('%s -i %s -o %s --classifier %s --bitscore %s --rank %s --taxon %s --blast %s' 
                                             % (self.R_subset_exe, 
                                                to_string(input), 
                                                outfile,
                                                self.R_subset_classifier[i],
                                                self.R_subset_bitscore,
                                                self.R_subset_rank[i],
                                                self.R_subset_taxon_db,
                                                to_string(parser_out))),
                                 stdout = subprocess.PIPE)
            
            # during processing print output in verbose mode and update the logfile
            while p.poll() is None:
                if self.verbose:
                    print_verbose(p.stdout.readline())
                    logfile.write(p.stdout.readline())
                else:
                    logfile.write(p.stdout.readline())
            # wait until process is complete
            p.wait()
            if p.returncode:
                raise SubsetDBException(self.logdir + self.R_subset_classifier[i] + '.log')
            
        # print summary of the process after completion
        print_verbose('Subsetting of annotated Blast database complete \n')
        print_running_time(self.time)
        newline()
       
    def krona_report(self, input, output, parser_output):
        
        # create a dir for output
        create_outputdir(output)
        # generate path and name for output file
        outfile = output + os.sep + self.krona_name + '.html'
        
        # test type of input file
        if is_tabular(input):
            # print actual informations about the step on stdout    
            print_step(self.step_number, 
                       'Analysis', 
                       'Create Overview from tabular output',
                       self.krona_parameter)
            newline()
            
            # start the Krona import script for Blast tabular output
            # pipe all output for stdout in a logfile
            p = subprocess.Popen(shlex.split('%s -o %s %s %s' 
                                             % (self.krona_exe,
                                                outfile,
                                                self.krona_parameter,
                                                to_string(input))),
                                 stdout = open_logfile(self.logdir + 'krona.log'),
                                 stderr = open_logfile(self.logdir + 'krona.err.log'))
            # wait until process is complete
            p.wait()
            if p.returncode:
                raise KronaException(self.logdir + 'krona.err.log')
            else:
                # remove unused error logs
                remove_empty_logfile(self.logdir + 'krona.err.log')
                # print summary of the process after completion
                print_verbose('Creation of Krona Pie Chart complete \n')
                print_running_time(self.time)
                newline()
            
        elif is_xml(input) and is_db(parser_output):
            print_step(self.step_number, 
                       'Analysis', 
                       'Create Overview from XML output',
                       self.krona_parameter)
            # convert the values from database to tabular format
            extract_tabular(to_string(parser_output), output)
            # set the new input
            input = update_reads(output, 'extracted_from_DB','tab')
            
            # start the Krona import script for Blast tabular output
            # pipe all output for stdout in a logfile
            p = subprocess.Popen(shlex.split('%s -o %s %s %s' 
                                             % (self.krona_exe,
                                                outfile,
                                                self.krona_parameter,
                                                to_string(input))),
                                 stdout = open_logfile(self.logdir + 'krona.log'),
                                 stderr = open_logfile(self.logdir + 'krona.err.log'))
            # wait until process is complete
            p.wait()
            if p.returncode:
                raise KronaException(self.logdir + 'krona.err.log')
            else:
                # remove unused error logs
                remove_empty_logfile(self.logdir + 'krona.err.log')
                # print summary of the process after completion
                print_verbose('Creation of Krona Pie Chart complete \n')
                print_running_time(self.time)
                newline()
            
        elif not is_tabular(input) or not is_xml(input):
            raise KronaFormatException()
        else:
            print_verbose('ERROR 25: Krona Report could not be generated, because of unknown reasons')
            sys.exit(1)
            
        
        
