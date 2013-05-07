import subprocess
import os
from src.settings import *
import shlex
from src.utils import createOutputDir, ParamFileArguments

class Programs:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
       
    # do an quality analysis of the input files with FastQC   
    def fastqc(self, settings, outputdir):
    	
    	createOutputDir(Settings.output + os.sep + outputdir)
        # update cli
        consoleOutput("FastQC", ParamFileArguments(FastQC_Parameter()))
        # start FastQC and wait until task complete
        p = subprocess.Popen(shlex.split("%s -t %s -o %s -q --noextract %s %s" % (Settings.FASTQC, Settings.threads, Settings.output + os.sep + outputdir,
                                                                                ParamFileArguments(FastQC_Parameter()),
                                                                                 ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input))))
        p.wait()
        autotrim(Settings.output+os.sep+outputdir+os.sep)
        return True
       
    def trimming(self, settings, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update cli
        consoleOutput("Quality Trimming", ParamFileArguments(TrimGalore_Parameter()))
        # start TrimGalore and wait until task complete
        p = subprocess.Popen(shlex.split("%s %s -o %s %s" % (Settings.TRIMGALORE, ParamFileArguments(TrimGalore_Parameter())
                                                              , (sys.path[0] + os.sep + Settings.output + os.sep + outputdir),
                                                              ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input)))
                             , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        # search for the processed input files and update input files in settings object
        new = [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)]
        Settings.input = [Settings.output + os.sep + outputdir + os.sep + new[1],
						Settings.output + os.sep + outputdir + os.sep + new[0]]
        return True
    
    def assembly(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir + os.sep)
        consoleOutput("Create Hashtables", ParamFileArguments(Velveth_Parameter()))
        # open log file for piping
        log = open(Settings.output + os.sep + outputdir + os.sep + "velveth.log.txt", "w")
        # start velveth and wait for completion
        p = subprocess.Popen(shlex.split("%s %s %s %s -fmtAuto %s " % (Settings.VELVETH,Settings.output + os.sep + outputdir, 
                                                                       Settings.kmer, ParamFileArguments(Velveth_Parameter()) ,
                                                                       ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input))), 
                             stdout=log)
        p.wait()

        consoleOutput("First Assembly Step", ParamFileArguments(Velvetg_Parameter()))
        log = open(Settings.output + os.sep + outputdir + os.sep + "velvetg.log.txt", "w")
        # # Argumente funktionieren im moment noch nicht 
        p = subprocess.Popen(shlex.split("%s %s %s" % (Settings.VELVETG,Settings.output + os.sep + outputdir, 
                                                       ParamFileArguments(Velvetg_Parameter()))), stdout=log)
        p.wait()
        log = open(Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.log.txt", "w")
        consoleOutput("Metagenomic Assembly", ParamFileArguments(MetaVelvet_Parameter()))
        p = subprocess.Popen(shlex.split(Settings.METAVELVET + " " + Settings.output + os.sep + outputdir), stdout=log)
    	#p = subprocess.Popen(shlex.split("%s %s %s" % (Settings.METAVELVET,Settings.output + os.sep + outputdir, 
        #                                               ParamFileArguments(MetaVelvet_Parameter()))),stderr=log)
        p.wait()
        Settings.input = Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.contigs.fa"
        return True
    
    def concat(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        aln = open(Settings.output + os.sep + outputdir + os.sep + "alignments.txt", "w")
        #print all created alignments in extra file
        consoleOutput("Concat", ParamFileArguments(Concat_Parameter()))
        if len(Settings.input) > 1:
            # for paired end files
            p = subprocess.Popen(shlex.split("%s -i %s -j %s -o %s -t %s %s " % (Settings.CONCAT,sys.path[0] + os.sep + str(Settings.input[0]),
                                                                                 sys.path[0] + os.sep + str(Settings.input[1]),
                                                                                 Settings.output + os.sep + outputdir, Settings.threads,
                                                                                 ParamFileArguments(Concat_Parameter()))), 
                                 stdout=aln, stderr=subprocess.STDOUT)
        else:
            # for single end files
            p = subprocess.Popen(shlex.split("%s -i %s -j %s -o %s -t %s %s " % (Settings.CONCAT,sys.path[0] + os.sep + str(Settings.input),
                                                                                 Settings.output + os.sep + outputdir, Settings.threads,
                                                                                 ParamFileArguments(Concat_Parameter()))),
                                 stdout=aln, stderr=subprocess.STDOUT)
        p.wait()
        # move file from the first level to the specified output folder
        moveFiles(Settings.output + os.sep , Settings.output + os.sep + outputdir + os.sep, ".fastq")
        # update the input parameter
        Settings.input = Settings.output + os.sep + outputdir + os.sep + "concat-contigs.fastq"
    
    def blastn(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        # check the input files for filetype
        if Settings.input.endswith(".fq") or Settings.input.endswith(".fastq"):
            consoleOutput("Converting from fastq to fasta", "")
            # convert fastq files to fasta
            p = subprocess.Popen(shlex.split("%s -n -Q33 -i %s -o %s" % (Settings.CONVERTER,Settings.input, 
                                                                         Settings.output + os.sep + outputdir + os.sep + "contigs.fasta")))
            p.wait()
            Settings.input = Settings.output + os.sep + outputdir + os.sep + "contigs.fasta"
        # get all specified blastn parameter
        consoleOutput("Classify with Blastn", ParamFileArguments(Blastn_Parameter()))
        # create argument string
        p = subprocess.Popen(shlex.split("%s -db %s -query %s -out %s -num_threads %s %s " % (Settings.BLASTN,Settings.blastdb_nt, Settings.input,
                                                                      Settings.output + os.sep + outputdir + os.sep + "blastn.tab",
                                                                      Settings.threads, ParamFileArguments(Blastn_Parameter()))))
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
        
        
        
        
        
        
        
        
        
        
        
