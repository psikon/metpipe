import subprocess
import os
from src.settings import *
import shlex
from src.utils import createOutputDir

class Programs:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
       
    # do an quality analysis of the input files with FastQC   
    def fastqc(self, settings, outputdir):
    	
    	createOutputDir(Settings.output + os.sep + outputdir)
    	# get all specified arguments from the parameter file
    	params = ParamFileArguments(FastQC_Parameter())
    	# create the argument string for usage
        arguments = (" -t %s -o %s -q --extract %s %s") % (Settings.threads,
														Settings.output + os.sep + outputdir,
														params, ' '.join(sys.path[0] + os.sep + 
														str(i)for i in Settings.input))
        # update cli
        consoleOutput("FastQC", params)
        # start FastQC and wait until task complete
        p = subprocess.Popen(shlex.split(Settings.FASTQC + " " + arguments))
        p.wait()
        return True
       
    def trimming(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        params = ParamFileArguments(TrimGalore_Parameter())
        # create the arguments string for TrimGalore
        arguments = ("%s -o %s %s") % (params, (sys.path[0] + os.sep + Settings.output + os.sep + outputdir),
                                    ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input))
        # update cli
        consoleOutput("Quality Trimming", params)
        # start TrimGalore and wait until task complete
        p = subprocess.Popen(shlex.split(Settings.TRIMGALORE + " " + arguments), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        # search for the processed input files and update input files in settings object
        new = [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)]
        Settings.input = [Settings.output + os.sep + outputdir + os.sep + new[1],
						Settings.output + os.sep + outputdir + os.sep + new[0]]
        return True
        
    def assembly(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir + os.sep)
        # parse all velveth specific arguments from parameter file
    	params = ParamFileArguments(Velveth_Parameter())
        # create arguments string for velveth
    	velveth_args = "%s %s %s -fmtAuto %s " % (Settings.output + os.sep + outputdir, Settings.kmer, params ,
                                         ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input))
        consoleOutput("Create Hashtables", params)
        # open log file for piping
        log = open(Settings.output + os.sep + outputdir + os.sep + "velveth.log.txt", "w")
        # start velveth and wait for completion
        p = subprocess.Popen(shlex.split(Settings.VELVETH + " " + velveth_args), stdout=log)
        p.wait()
        # parse alle velvetg specific aruments from parameter file
    	params = ParamFileArguments(Velvetg_Parameter())
    	velvetg_args = "%s %s" % (Settings.output + os.sep + outputdir, params)
        consoleOutput("First Assembly Step", params)
        log = open(Settings.output + os.sep + outputdir + os.sep + "velvetg.log.txt", "w")
        # # Argumente funktionieren im moment noch nicht 
        p = subprocess.Popen(shlex.split(Settings.VELVETG + " " + velvetg_args), stdout=log)
        p.wait()
    	params = ParamFileArguments(MetaVelvet_Parameter())
        log = open(Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.log.txt", "w")
        metavelvet_args = "%s %s" % (Settings.output + os.sep + outputdir, params)  
        consoleOutput("Metagenomic Assembly", params)
        p = subprocess.Popen(shlex.split(Settings.METAVELVET + " " + Settings.output + os.sep + outputdir), stdout=log)
    	# p = subprocess.Popen(shlex.split(Settings.METAVELVET + " " + metavelvet_args))
        p.wait()
        Settings.input = Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.contigs.fa"
        return True
    
    def concat(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        # get all specified parameter from parameter file 
        params = ParamFileArguments(Concat_Parameter())
        # create argument string
        if len(Settings.input) > 1:
            # for paired end files
        	arguments = "-i %s -j %s -o %s -t %s %s " % (sys.path[0] + os.sep + str(Settings.input[0]),
												  		 sys.path[0] + os.sep + str(Settings.input[1]),
												  		 Settings.output + os.sep + outputdir, Settings.threads,
												  		 params)
        else:
            # for single end files
        	arguments = "-i %s -o %s -t %s %s " % (sys.path[0] + os.sep + str(Settings.input),
												  		 Settings.output + os.sep + outputdir, Settings.threads,
												  		 params)
        consoleOutput("Concat", params)
        # print all created alignments in extra file
        aln = open(Settings.output + os.sep + outputdir + os.sep + "alignments.txt", "w")
        p = subprocess.Popen(shlex.split(Settings.CONCAT + " " + arguments), stdout=aln, stderr=subprocess.STDOUT)
        p.wait()
        # move file from the first level to the specified output folder
        moveFiles(Settings.output + os.sep , Settings.output + os.sep + outputdir + os.sep,".fastq")
        # update the input parameter
        Settings.input = Settings.output + os.sep + outputdir + os.sep + "concat-contigs.fastq"
    
    def blastn(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        # check the input files for filetype
        if Settings.input.endswith(".fq") or Settings.input.endswith(".fastq"):
            consoleOutput("Converting from fastq to fasta", "")
            # convert fastq files to fasta
            converter_args = "-n -Q33 -i %s -o %s" % (Settings.input,Settings.output + os.sep + outputdir + os.sep + "contigs.fasta")
            p = subprocess.Popen(shlex.split(Settings.CONVERTER + " " + converter_args))
            p.wait()
            Settings.input = Settings.output + os.sep + outputdir + os.sep + "contigs.fasta"
        # get all specified blastn parameter
        params = ParamFileArguments(Blastn_Parameter())
        consoleOutput("Classify with Blastn", params)
        #create argument string
        arguments = "-db %s -query %s -out %s -num_threads %s %s " % (Settings.blastdb_nt, Settings.input,
                                                                      Settings.output + os.sep + outputdir + os.sep + "blastn.tab",
                                                                      Settings.threads, params)  
        p = subprocess.Popen(shlex.split(Settings.BLASTN + " " + arguments))
        p.wait()
        
    def metaCV(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        params = ParamFileArguments(MetaCV_Parameter())
        consoleOutput("Annotation ", params)
        arguments = "classify %s %s %s %s" % (Settings.metacv_db, Settings.input, "metpipe", params)
        consoleOutput("MetaCV", params)
        log = open(Settings.output + os.sep + outputdir + os.sep + "metacv.log", "w")
        p = subprocess.Popen(shlex.split(Settings.METACV + " " + arguments), stderr=log)
        p.wait()
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, ".csv")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, ".res")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, ".faa")
        result = [sys.path[0] + os.sep + Settings.output + os.sep + outputdir + os.sep + f for f in os.listdir(sys.path[0] + os.sep + Settings.output + os.sep + outputdir) if f.endswith(".res")]
        consoleOutput("Create Summary of annotation", "")
        arguments = "res2table %s %s %s --threads=%s" % (Settings.metacv_db, result[0], "metpipe.res2table", Settings.threads)
        log = open(Settings.output + os.sep + outputdir + os.sep + "metacv.log", "w")
        p = subprocess.Popen(shlex.split(Settings.METACV + " " + arguments), stderr=log)
        p.wait()
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".res2table")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".fun_hist")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".tax_hist")
        arguments = "res2sum %s %s %s" % (Settings.metacv_db, result[0], "metpipe.res2sum")
        log = open(Settings.output + os.sep + outputdir + os.sep + "metacv.log", "w")
        p = subprocess.Popen(shlex.split(Settings.METACV + " " + arguments), stderr=log)
        p.wait()
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".res2sum")
        
        
        
        
        
        
        
        
        
        
        
