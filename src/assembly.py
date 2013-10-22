# standard imports
import subprocess
import shlex
import sys, os
import time
# imports of own functions and classes
from src.file_functions import create_outputdir, update_reads, parse_parameter, merge_files
from src.log_functions import print_step, newline, print_compact, print_verbose, open_logfile, print_running_time, remove_empty_logfile
from src.utils import to_string, is_fastq, is_paired, is_executable
from src.exceptions import FlashException, VelvetHException, VelvetGException, MetaVelvetException



class Assembly:
    
    def __init__(self, threads, step_number, verbose, time, logdir, input, mode,
                 flash_exe, concat_dir, concat_parameter, merge_uncombined, 
                 velveth_exe, velvetg_exe, metavelvet_exe, assembly_out, kmer, 
                 velveth_parameter, velvetg_parameter, metavelvet_parameter):
        
        # init general variables
        self.threads = threads
        self.step_number = step_number
        self.verbose = verbose
        self.time = time
        self.logdir = logdir
        self.input = to_string(input)
        self.mode = mode
         
        # init flash specific variables
        self.flash_exe = flash_exe
        self.concat_out = concat_dir 
        self.concat_parameter = concat_parameter
        self.merge_uncombined = merge_uncombined
        
        # init metavelvet specific variables
        self.velveth_exe = velveth_exe
        self.velvetg_exe = velvetg_exe
        self.metavelvet_exe = metavelvet_exe
        self.assembly_out = assembly_out
        self.kmer = kmer
        self.velveth_parameter = velveth_parameter
        self.velvetg_parameter = velvetg_parameter
        self.metavelvet_parameter = metavelvet_parameter
          
    def __del__(self):
       pass
    
    def manage_assembly(self):
        
        concatinated = ''
        assembled = ''
        # run the assembling functions when the module is initialized
        if self.mode.lower() == 'flash':
            # is executable existing and runnable?
            if is_executable(self.flash_exe):
                # start concatination and update the input for next step
                self.concatinate(self.concat_out)
                self.step_number += 1
                # merge the concatinated reads with non concatinated rest
                if (self.merge_uncombined):
                    self.input = merge_files([to_string(update_reads(self.concat_out, 'extendedFrags', 'fastq')),
                                             to_string(update_reads(self.concat_out, 'out.notCombined', 'fastq'))],
                                             self.concat_out,
                                             'merged_concat','fastq')
                else:
                    concatinated = update_reads(self.concat_out, 'extendedFrags', 'fastq')
                    self.input = concatinated
                

        if self.mode.lower() == 'metavelvet':
            # is executable existing and runnable?
            if is_executable(self.velveth_exe) and is_executable(self.velveth_exe) and is_executable(self.metavelvet_exe):
                # start assembly and update the input for next step
                self.assemble_reads(self.assembly_out)
                assembled = update_reads(self.assembly_out, 'meta-velvetg', 'fa')
                self.input = assembled
                self.step_number += 1
                
        if self.mode.lower() == 'both':
            #TODO: not working because of auto mode --> see logs
            
            # is executable existing and runnable?
            if is_executable(self.flash_exe) and is_executable(self.velveth_exe) and is_executable(self.velveth_exe) and is_executable(self.metavelvet_exe):
                # start processing and update the input for next step
                self.concatinate(self.concat_out)
                concatinated = update_reads(self.out, 'extendedFrags', 'fastq')
                self.input = concatinated
                self.assemble_reads(self.assembly_out)
                assembled = update_reads(self.assembly_out, 'meta-velvetg', 'fa')
                self.step_number += 1
                self.input = assembled
        return [self.step_number, self.input, concatinated, assembled]
        
    def concatinate(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Assembly', 
                   'Concatinate Reads',
                   self.concat_parameter)
        newline()
        
        # open the logfile
        logfile = open_logfile(self.logdir + 'concatination.log')
        
        # start the program Flash with parameter from the conf file a
        # errors will be piped to extra error logfile
        p = subprocess.Popen(shlex.split('%s -t %d -d %s %s %s' % (self.flash_exe,
                                                                   self.threads,
                                                                   outputdir,
                                                                   self.concat_parameter,
                                                                   self.input)),
                            stdout = subprocess.PIPE, 
                            stderr = open_logfile(self.logdir + 'flash.err.log'))
        
        # during processing print Flash output in verbose mode and update the logfile
        while p.poll() is None:
            if self.verbose:
                print_verbose(p.stdout.readline())
                logfile.write(p.stdout.readline())
            else:
                print_compact(p.stdout.readline().rstrip('\n'))
                logfile.write(p.stdout.readline())
        # wait until process is finished        
        p.wait()
        
        if p.returncode:
           raise FlashException(self.logdir + 'flash.err.log')
        else:
            # remove empty error logs
            remove_empty_logfile(self.logdir + 'flash.err.log')
            # print summary of the process after completion
            newline()
            print_verbose('Concatination complete \n')
            print_running_time(self.time)
        
    def assemble_reads(self, outputdir):
        
        # create a dir for output
        create_outputdir(outputdir)
        
        # print actual informations about the step on stdout
        print_step(self.step_number, 
                   'Assembly', 
                   'Creating Hashmaps',
                   self.velveth_parameter)
        newline()
        
        # open the first logfile
        velveth_log = open_logfile(self.logdir + 'velveth.log')
        
        # start the program velveth with parameter from the conf file and automatic detection
        # of the input file format
        # errors will be piped to extra error logfile
        p = subprocess.Popen(shlex.split('%s %s %s %s -fmtAuto %s' % (self.velveth_exe, 
                                                                      outputdir,
                                                                      self.kmer, 
                                                                      self.velveth_parameter,
                                                                      self.input)),
                            stdout = subprocess.PIPE, 
                            stderr = open_logfile(self.logdir + 'velveth.err.log')) 
        # during processing print velveth output in verbose mode and update the logfile
        while p.poll() is None:
           if self.verbose:
               print_verbose(p.stdout.readline())
               velveth_log.write(p.stdout.readline())
           else:
               #self.log.print_compact(p.stdout.readline())                         
               velveth_log.write(p.stdout.readline())
        # wait until process is finished
        p.wait()
        
        if p.returncode:
           raise VelvetHException(self.logdir + 'velveth.err.log')
        else:
            # remove empty error logs
            remove_empty_logfile(self.logdir + 'velveth.err.log')
            
            # print actual informations about the step on stdout
            print_step(self.step_number, 
                       'Assembly', 
                       'Creating Graph',
                       self.velvetg_parameter)
            newline()
        
            # open the second logfile
            velvetg_log = open_logfile(self.logdir + 'velvetg.log')
        
            # start the program velvetg in the dir of velveth, with the parameter of the conf file
            # errors will be piped to extra error logfile
            p = subprocess.Popen(shlex.split('%s %s %s' % (self.velvetg_exe, 
                                                           outputdir,
                                                           self.velvetg_parameter)),
                                 stdout = subprocess.PIPE,
                                 stderr = open_logfile(self.logdir + 'velvetg.err.log'))
            # during processing print velveth output in verbose mode and update the logfile
            while p.poll() is None:
                if self.verbose:
                    print_verbose(p.stdout.readline())
                    velvetg_log.write(p.stdout.readline())
                else:
                    #self.log.print_compact(p.stdout.readline())
                    velvetg_log.write(p.stdout.readline())
            # wait until process is finished
            p.wait()
        
            if p.returncode:
                raise VelvetGException(self.logdir + 'velvetg.err.log')
            else:
                # remove empty error logs
                remove_empty_logfile(self.logdir + 'velvetg.err.log')
        
                # print actual informations about the step on stdout
                print_step(self.step_number, 
                           'Assembly', 
                           'Metagenomic Assembly',
                           self.metavelvet_parameter)
                newline()
               
                # open the third logfile
                meta_log = open_logfile(self.logdir + 'metavelvet.log')
        
                # start the program meta-velvetg in the dir of velveth and velvetg, 
                # with the parameter of the conf file
                # errors will be piped to extra error logfile
                p = subprocess.Popen(shlex.split('%s %s %s' % (self.metavelvet_exe, 
                                                               outputdir,
                                                               self.metavelvet_parameter)),
                                     stdout = subprocess.PIPE, 
                                     stderr = open_logfile(self.logdir + 'metavelvet.err.log'))
                # during processing print velveth output in verbose mode and update the logfile                         
                while p.poll() is None:
                    if self.verbose:
                        print_verbose(p.stdout.readline())
                        meta_log.write(p.stdout.readline())
                    else:
                        #self.log.print_compact(p.stdout.readline())
                        meta_log.write(p.stdout.readline())
                # wait until process is finished
                p.wait()
                
                if p.returncode:
                    raise MetaVelvetException(self.logdir + 'metavelvet.err.log')
                else:
                    # remove empty error logs
                    remove_empty_logfile(self.logdir + 'metavelvet.err.log')
                    newline()
                    # print summary of the process after completion
                    print_verbose('Assembly complete \n')
                    print_running_time(self.time)
                    newline()

        