# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.utils import ParamFileArguments
from src.settings import RunSettings, Executables, Blastn_Parameter, MetaCV_Parameter
from src.file_functions import *
from src.log_functions import Logging

class Annotation:
    
    raw = ''
    input = ''
    logdir = ''
    blast_out = ''
    metacv_out = ''
    
    def __init__(self, files_instance, mode):
        # init all important variables and classes
        self.log = Logging()
        self.exe = Executables()
        self.files = files_instance
        self.input = self.files.get_input()
        self.raw = self.files.get_raw()
        self.logdir = self.files.get_logdir()
        self.blast_out = self.files.get_blastn_dir()
        self.metacv_out = self.files.get_metacv_dir()
        
        # run the annotation functions when the module is initialized
        if mode.lower() == 'blastn':
            # is executable existing and runnable?
            if is_executable(self.exe.BLASTN, 'blastn'):
                # start annotation with blastn
                self.blastn(self.blast_out)
                # verbessern
                self.files.set_blastn_output(update_reads(self.blast_out,'blastn','xml'))
                RunSettings.step_number = RunSettings.step_number + 1
            else:
                pass
        elif mode.lower() == 'metacv':
            # is executable existing and runnable?
            if is_executable(self.exe.METACV, 'metacv'):
                # start annotation with metacv
                self.metacv(self.metacv_out)
                RunSettings.step_number = RunSettings.step_number + 1
            else:
                pass
        else: 
            # is executable existing and runnable?
            if is_executable(self.exe.BLASTN, 'blastn') and is_executable(self.exe.METACV, 'metacv'):
                # start annotation with both tools 
                self.blastn(self.blast_out)
                self.metacv(self.metacv_out)
                RunSettings.step_number = RunSettings.step_number + 1
            else:
                pass
            
    def __del__(self):
        pass   
        
            
    def blastn(self, outputdir):
            
        # create a dir for output
        create_outputdir(outputdir)
        
        # blastn can only run with dfasta files, so input has to be converted
        if all(is_fastq(i) for i in self.input):
            # print actual informations about the step on stdout
            self.log.print_step(RunSettings.step_number, 'Assembly', 'convert fastq files',
                                self.log.cut_path(self.input))
            self.input = convert_fastq(self.input, self.blast_out)
        
        # blastn can only annotated one file, so input has to be merged to one file
        if is_paired(self.input):
            # print actual informations about the step on stdout
            self.log.print_step(RunSettings.step_number, 'Annotation', 'merging reads to on file',
                                self.log.cut_path(self.input))
            self.input = merge_files(self.input, self.blast_out)
        
        # define the outputformat for the blastn results
        outfile = outputdir + os.sep + blast_output(Blastn_Parameter().outfmt)
        
        # print actual informations about the step on stdout
        self.log.print_step(RunSettings.step_number, 'Annotation', 'blast sequences against nt database',
                            ParamFileArguments(Blastn_Parameter()))
        
        # start blastn and wait until completion
        # logfile is not requiered, because blastn has no log function and no output to stdout
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (self.exe.BLASTN,
                                          RunSettings.blastdb_nt,
                                          str_input(self.input),
                                          outfile,
                                          RunSettings.threads, 
                                          ParamFileArguments(Blastn_Parameter()))))
        # wait until process is complete
        p.wait()
        
        # remove the temporary files: converted fastq files and the merged fasta files
        remove_file(outputdir + os.sep, 'converted', 'fasta')
        remove_file(outputdir + os.sep, 'merged', 'fasta')
        # print summary of the process after completion
        self.log.print_verbose('Annotation with blastn complete \n')
        self.log.print_verbose('processed in: ' + 
                               self.log.getDHMS(time.time() - RunSettings.actual_time) 
                               + '\n')
        self.log.newline
        
    def metacv(self,outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        #if RunSettings.use_contigs:
        #    self.raw = str_input(self.input)
        #else:
        #    pass
        # print actual informations about the step on stdout
        self.log.print_step(RunSettings.step_number, 'Annotation', 'annotate bacterial reads with MetaCV',
                            ParamFileArguments(MetaCV_Parameter()))
        
        print self.raw
        print shlex.split('%s classify %s %s %s ' % (self.exe.METACV,
                                        RunSettings.metacv_db,
                                        ' '.join(str(i)for i in self.raw),
                                        'metpipe'))
        print self.exe.METACV
        p = subprocess.Popen(shlex.split('%s -h' % (self.exe.METACV)))
#        p = subprocess.Popen(shlex.split('%s classify %s %s %s ' % 
#                                        (self.exe.METACV,
#                                         RunSettings.metacv_db,
#                                         str_input(self.raw),
#                                         'metpipe')),
#                                         #ParamFileArguments(MetaCV_Parameter()))),
#                                 stderr = self.log.open_logfile('metacv.err.log'), 
#                                 stdout = subprocess.PIPE)
        while p.poll() is None:
            if RunSettings.verbose:
                self.log.print_verbose(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
        # wait until process is finished        
        p.wait()
        