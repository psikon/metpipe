import subprocess
import shlex
import sys, os
from src.utils import consoleOutput, createOutputDir, ParamFileArguments, moveFiles, testInputFormat
from src.settings import Settings, FastQC_Parameter, TrimGalore_Parameter, Concat_Parameter, Velveth_Parameter, Velvetg_Parameter, MetaVelvet_Parameter, Blastn_Parameter, MetaCV_Parameter

class Programs:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
       
    # handle the program FastQC - an standard tool to determine the quality of short read sequencing files 
    def fastqc(self, outputdir):
    	
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        consoleOutput("FastQC", ParamFileArguments(FastQC_Parameter()))
        # start FastQC and wait until task complete
        p = subprocess.Popen(shlex.split("%s -t %s -o %s -q --extract %s %s" % (Settings.FASTQC, Settings.threads, Settings.output + os.sep + outputdir,
                                                                                ParamFileArguments(FastQC_Parameter()),
                                                                                 ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input))))
        p.wait() 
        # update the Settings.quality_report var for log purposes
        for r, d, f in os.walk(Settings.output + os.sep + outputdir + os.sep):
            for files in f:
                if files.endswith("_data.txt"):
                    Settings.quality_report.append(os.path.join(r, files))
        return True
       
    def trimming(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        consoleOutput("Quality Trimming", ParamFileArguments(TrimGalore_Parameter()))
        # start TrimGalore and wait until task complete
        p = subprocess.Popen(shlex.split("%s %s -o %s %s" % (Settings.TRIMGALORE, ParamFileArguments(TrimGalore_Parameter())
                                                              , (sys.path[0] + os.sep + Settings.output + os.sep + outputdir),
                                                              ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input)))
                             , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        # search for the processed input files and update input files in settings object
        if len(Settings.input) > 1:
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][1],
						      Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][0]]
        else:
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][0]]
        return True
    
    def assembly(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir + os.sep)
        # update information on cmd
        consoleOutput("Create Hashtables with velveth", ParamFileArguments(Velveth_Parameter()))
        # start velveth and wait for completion
        p = subprocess.Popen(shlex.split("%s %s %s %s -fmtAuto %s " % (Settings.VELVETH, Settings.output + os.sep + outputdir,
                                                                       Settings.kmer, ParamFileArguments(Velveth_Parameter()) ,
                                                                       ' '.join(sys.path[0] + os.sep + str(i)for i in Settings.input))),
                             stdout=open(Settings.output + os.sep + outputdir + os.sep + "velveth.log.txt", "w"))
        p.wait()
        # update information on cmd
        consoleOutput("First Assembly Step", ParamFileArguments(Velvetg_Parameter()))

        # start velvetg to create the graph for the metagenomic assembly
        p = subprocess.Popen(shlex.split("%s %s %s" % (Settings.VELVETG, Settings.output + os.sep + outputdir,
                                                       ParamFileArguments(Velvetg_Parameter()))),
                             stdout=open(Settings.output + os.sep + outputdir + os.sep + "velvetg.log.txt", "w"))
        p.wait()
        # update information on cmd
        consoleOutput("Metagenomic Assembly", ParamFileArguments(MetaVelvet_Parameter()))
        p = subprocess.Popen(shlex.split(Settings.METAVELVET + " " + Settings.output + os.sep + outputdir),
                             stdout=open(Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.log.txt", "w"))
    	# p = subprocess.Popen(shlex.split("%s %s %s" % (Settings.METAVELVET,Settings.output + os.sep + outputdir, 
        #                                               ParamFileArguments(MetaVelvet_Parameter()))),
        #                     stderr=open(Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.log.txt", "w"))
        p.wait()
        # update Settings.input for further processing
        Settings.input = Settings.output + os.sep + outputdir + os.sep + "meta-velvetg.contigs.fa"
        return True
    
    def concat(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        consoleOutput("Concat", ParamFileArguments(Concat_Parameter()))
        if len(Settings.input) > 1:
            # for paired end files
            p = subprocess.Popen(shlex.split("%s -i %s -j %s -o %s -t %s %s " % (Settings.CONCAT, sys.path[0] + os.sep + str(Settings.input[0]),
                                                                                 sys.path[0] + os.sep + str(Settings.input[1]),
                                                                                 Settings.output + os.sep + outputdir, Settings.threads,
                                                                                 ParamFileArguments(Concat_Parameter()))),
                                 stdout=open(Settings.output + os.sep + outputdir + os.sep + "alignments.txt", "w"),
                                 stderr=open(Settings.output + os.sep + outputdir + os.sep + "concat.log.txt", "w"))
        else:
            # for single end files
            p = subprocess.Popen(shlex.split("%s -i %s -j %s -o %s -t %s %s " % (Settings.CONCAT, sys.path[0] + os.sep + str(Settings.input),
                                                                                 Settings.output + os.sep + outputdir, Settings.threads,
                                                                                 ParamFileArguments(Concat_Parameter()))),
                                 stdout=open(Settings.output + os.sep + outputdir + os.sep + "alignments.txt", "w"),
                                 stderr=open(Settings.output + os.sep + outputdir + os.sep + "concat.log.txt", "w"))
        p.wait()
        # move files from the first level to the specified output folder
        moveFiles(Settings.output + os.sep , Settings.output + os.sep + outputdir + os.sep, ".fastq")
        # update the Setings.input var for further processing
        Settings.input = Settings.output + os.sep + outputdir + os.sep + "concat-contigs.fastq"
        return True
    
    def convertToFasta(self,outputdir):
        
        # if no assembly was done and the reads are paired-end in 2 files --> create one file from it
        if len(Settings.input) > 1:
            consoleOutput(step, arguments)
            input = open()
            
            
            
            # update information of cmd
            consoleOutput("Converting from fastq to fasta", Settings.input)
            # convert fastq files to fasta
            p = subprocess.Popen(shlex.split("%s -n -Q33 -i %s -o %s" % (Settings.CONVERTER, Settings.input,
                                                                     Settings.output + os.sep + outputdir + os.sep + "contigs.fasta")))
            p.wait()
            # update the Settings.input var
            Settings.input = Settings.output + os.sep + outputdir + os.sep + "contigs.fasta"
        
    def blastn(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # check the input files for filetype - fastq Files need convertion into fasta for blastn
        if testInputFormat(Settings.input):
            # update information of cmd
            consoleOutput("Converting from fastq to fasta", Settings.input)
            # convert fastq files to fasta
            p = subprocess.Popen(shlex.split("%s -n -Q33 -i %s -o %s" % (Settings.CONVERTER, Settings.input,
                                                                         Settings.output + os.sep + outputdir + os.sep + "contigs.fasta")))
            p.wait()
            # update the Settings.input var
            Settings.input = Settings.output + os.sep + outputdir + os.sep + "contigs.fasta"
        # update information of cmd
        consoleOutput("Classify with Blastn", ParamFileArguments(Blastn_Parameter()))
        # create outputfile name
        if Blastn_Parameter().outfmt == 5:
            outfile = "blastn.xml" 
        else: 
            outfile = "blastn.tab"
            
        # start blastn and wait until completion
        p = subprocess.Popen(shlex.split("%s -db %s -query %s -out %s -num_threads %s %s " % (Settings.BLASTN, Settings.blastdb_nt, Settings.input,
                                                                      Settings.output + os.sep + outputdir + os.sep + outfile,
                                                                      Settings.threads, ParamFileArguments(Blastn_Parameter()))))
        p.wait()
        # save path to the blastn results
        Settings.blast_output = Settings.output + os.sep + outputdir + os.sep + outfile
        
        return True
        
    def metaCV(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update the information of cmd
        consoleOutput("MetaCV", ParamFileArguments(MetaCV_Parameter()))
        # start metaCV and wait until completion ATTENTION: need 32GB RAM
        p = subprocess.Popen(shlex.split("%s classify %s %s %s %s" % (Settings.METACV,Settings.metacv_db, 
                                                                      Settings.input, "metpipe", 
                                                                      ParamFileArguments(MetaCV_Parameter()))), 
                             stderr=open(Settings.output + os.sep + outputdir + os.sep + "metacv.log", "w"))
        p.wait()
        # move all necessary files into metacv output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, ".csv")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, ".res")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, ".faa")
        # save the path to the metaCV result file 
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith(".res")][0]))))
        # update the information of cmd
        consoleOutput("Create Summary of annotation", "")
        # create an summary of the metacv run
        p = subprocess.Popen(shlex.split("%s res2table %s %s %s --threads=%s" % (Settings.METACV,Settings.metacv_db, Settings.metaCV_output, "metpipe.res2table", Settings.threads)),
                             stderr=open(Settings.output + os.sep + outputdir + os.sep + "metacv.log", "w"))
        p.wait()
        # move the summary to the output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".res2table")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".fun_hist")
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".tax_hist")
        # save the path to the summary of metacv
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith(".fun_hist") or f.endswith(".tax_hist")][0]))))
        # create a list of all found taxa in the metacv result
        p = subprocess.Popen(shlex.split("%s res2sum %s %s %s" % (Settings.METACV,Settings.metacv_db, Settings.metaCV_output, "metpipe.res2sum")), 
                             stderr=open(Settings.output + os.sep + outputdir + os.sep + "metacv.log", "w"))
        p.wait()
        # move the list to the output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, ".res2sum")
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith(".res2sum")][0]))))
       
        return True
        
    def summary(self):
        f = open("summary.txt","w")
        f.write(Settings.blast_output+"\n")
        for element in Settings.metaCV_output:
            f.write(element+"\n")
        f.write(Settings.quality_report)
        f.close()
        
        
        
        
        
        
        
        
        
        
