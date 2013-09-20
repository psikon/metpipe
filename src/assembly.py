# standard imports
import subprocess
import shlex
import sys, os
import time
# imports of own functions and classes
from src.settings import Executables, FLASH_Parameter, Velveth_Parameter, Velvetg_Parameter, MetaVelvet_Parameter
from src.file_functions import create_outputdir, update_reads, parse_parameter
from src.log_functions import Logging
from src.utils import to_string, is_fastq, is_paired, is_executable



class Assembly:
    
    
    input = ''
    interleaved = False
    concat_out = ''
    assembly_out = ''
    logdir = ''
    parameter_file = ''
    
    def __init__(self, files_instance, settings_instance, parameter_file, mode):
        
        # init all important variables and classes
        self.settings = settings_instance
        self.parameter_file = parameter_file
        self.log = Logging()
        self.exe = Executables(self.parameter_file)
        self.files = files_instance
        self.logdir = self.files.get_logdir()
        self.concat_out = self.files.get_concat_dir()
        self.assembly_out = self.files.get_assembly_dir()
        self.input = to_string(self.files.get_input())
        
        # run the assembling functions when the module is initialized
        if mode.lower() == 'flash':
            # is executable existing and runnable?
            if is_executable(self.exe.get_Flash()):
                # start concatination and update the input for next step
                self.concatinate(self.concat_out)
                self.files.set_input(update_reads(self.concat_out, 'extendedFrags', 'fastq'))
                self.files.set_concatinated_output(update_reads(self.concat_out, 'extendedFrags', 'fastq'))
                self.settings.set_step_number()

        if mode.lower() == 'metavelvet':
            # is executable existing and runnable?
            if is_executable(self.exe.get_Velveth()) and is_executable(self.exe.get_Velvetg()) and is_executable(self.exe.get_MetaVelvet()):
                # start assembly and update the input for next step
                self.assemble_reads(self.assembly_out)
                self.files.set_input(update_reads(self.assembly_out, 'meta-velvetg', 'fa'))
                self.files.set_assembled_output(update_reads(self.assembly_out, 'meta-velvetg', 'fa'))
                self.settings.set_step_number()
            else:
                pass
        
        if mode.lower() == 'both':
            #TODO: not working because of auto mode --> see logs
            
            # is executable existing and runnable?
            if is_executable(self.exe.get_Flash()) and is_executable(self.exe.get_Velveth()) and is_executable(self.exe.get_Velvetg()) and is_executable(self.exe.get_MetaVelvet()):
                # start processing and update the input for next step
                self.concatinate(self.concat_out)
                self.input = update_reads(self.out, 'extendedFrags', 'fastq')
                
                self.assemble_reads(self.assembly_out)
                
                self.files.set_input(update_reads(self.assembly_out, 'meta-velvetg', 'fa'))
                self.files.set_assembled_output(update_reads(self.assembly_out, 'meta-velvetg', 'fa'))
                self.settings.set_step_number()
            else:
                pass
            
    def __del__(self):
       pass
    
    def concatinate(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Assembly', 'Concatinate Reads',
                            parse_parameter(FLASH_Parameter(self.parameter_file)))
        self.log.newline()
        
        # open the logfile
        logfile = self.log.open_logfile(self.logdir + 'concatination.log')
        
        # start the program Flash with parameter from the conf file a
        # errors will be piped to extra error logfile
        p = subprocess.Popen(shlex.split('%s -t %d -d %s %s %s' % (self.exe.get_Flash(),
                                                                   self.settings.get_threads(),
                                                                   outputdir,
                                                                   parse_parameter(FLASH_Parameter(self.parameter_file)),
                                                                   self.input)),
                            stdout = subprocess.PIPE, 
                            stderr = self.log.open_logfile(self.logdir + 'flash.err.log'))
        # during processing print Flash output in verbose mode and update the logfile
        while p.poll() is None:
            if self.settings.get_verbose():
                self.log.print_verbose(p.stdout.readline())
                logfile.write(p.stdout.readline())
            else:
                self.log.print_compact(p.stdout.readline().rstrip('\n'))
                logfile.write(p.stdout.readline())
        # wait until process is finished        
        p.wait()
        
        # remove empty error logs
        self.log.remove_empty_logfile(self.logdir + 'flash.err.log')
        
        # print summary of the process after completion
        self.log.print_verbose('Concatination complete \n')
        self.log.print_running_time(self.settings.get_actual_time())
        
    def assemble_reads(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Assembly', 'Creating Hashmaps',
                           parse_parameter(Velveth_Parameter(self.parameter_file)))
        self.log.newline()
        
        # open the first logfile
        velveth_log = self.log.open_logfile(self.logdir + 'velveth.log')
        
        # start the program velveth with parameter from the conf file and automatic detection
        # of the input file format
        # errors will be piped to extra error logfile
        p = subprocess.Popen(shlex.split('%s %s %s %s -fmtAuto %s ' % (self.exe.get_Velveth(), 
                                                                       outputdir,
                                                                       Velveth_Parameter(self.parameter_file).get_kmer(self.parameter_file), 
                                                                       parse_parameter(Velveth_Parameter(self.parameter_file)),
                                                                       self.input)),
                            stdout = subprocess.PIPE, 
                            stderr = self.log.open_logfile(self.logdir + 'velveth.err.log')) 
        # during processing print velveth output in verbose mode and update the logfile
        while p.poll() is None:
           if self.settings.get_verbose():
               self.log.print_verbose(p.stdout.readline())
               velveth_log.write(p.stdout.readline())
           else:
               #self.log.print_compact(p.stdout.readline())                         
               velveth_log.write(p.stdout.readline())
        # wait until process is finished
        p.wait()
        
        # remove empty error logs
        self.log.remove_empty_logfile(self.logdir + 'velveth.err.log')
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Assembly', 'Creating Graph',
                           parse_parameter(Velvetg_Parameter(self.parameter_file)))
        self.log.newline()
        
        # open the second logfile
        velvetg_log = self.log.open_logfile(self.logdir + 'velvetg.log')
        
        # start the program velvetg in the dir of velveth, with the parameter of the conf file
        # errors will be piped to extra error logfile
        p = subprocess.Popen(shlex.split('%s %s %s' % (self.exe.get_Velvetg(), 
                                                       outputdir,
                                                       parse_parameter(Velvetg_Parameter(self.parameter_file)))),
                             stdout = subprocess.PIPE,
                             stderr = self.log.open_logfile(self.logdir + 'velvetg.err.log'))
        # during processing print velveth output in verbose mode and update the logfile
        while p.poll() is None:
           if self.settings.get_verbose():
               self.log.print_verbose(p.stdout.readline())
               velvetg_log.write(p.stdout.readline())
           else:
               #self.log.print_compact(p.stdout.readline())
               velvetg_log.write(p.stdout.readline())
        # wait until process is finished
        p.wait()
        
        # remove empty error logs
        self.log.remove_empty_logfile(self.logdir + 'velvetg.err.log')
        
        # print actual informations about the step on stdout
        self.log.print_step(self.settings.get_step_number(), 'Assembly', 'Metagenomic Assembly',
                           parse_parameter(MetaVelvet_Parameter(self.parameter_file)))
        self.log.newline()
        
        # open the third logfile
        meta_log = self.log.open_logfile(self.logdir + 'metavelvet.log')
        
        # start the program meta-velvetg in the dir of velveth and velvetg, 
        # with the parameter of the conf file
        # errors will be piped to extra error logfile
        p = subprocess.Popen(shlex.split('%s %s %s' % (self.exe.get_MetaVelvet(), 
                                                       outputdir,
                                                       parse_parameter(MetaVelvet_Parameter(self.parameter_file)))),
                                stdout = subprocess.PIPE, 
                                stderr = self.log.open_logfile(self.logdir + 'metavelvet.err.log'))
        # during processing print velveth output in verbose mode and update the logfile                         
        while p.poll() is None:
            if self.settings.get_verbose():
               self.log.print_verbose(p.stdout.readline())
               meta_log.write(p.stdout.readline())
            else:
                #self.log.print_compact(p.stdout.readline())
                meta_log.write(p.stdout.readline())
        # wait until process is finished
        p.wait()
        
        # remove empty error logs
        self.log.remove_empty_logfile(self.logdir + 'metavelvet.err.log')
        
        # print summary of the process after completion
        self.log.print_verbose('Assembly complete \n')
        self.log.print_running_time(self.settings.get_actual_time())
        self.log.newline()

        