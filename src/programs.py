import subprocess
import os
from src.settings import *
import shlex

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
    	
    	params = ParamFileArguments(Velveth_Parameter())
    	velveth_args = "%s %s %s" % (Settings.output + os.sep + outputdir, Settings.kmer, params)
    	print "Velveth: " + velveth_args
    	params = ParamFileArguments(Velvetg_Parameter())
    	velvetg_args = "%s %s" % (Settings.output + os.sep + outputdir, params)
    	print "Velvetg: " + velvetg_args
    	params = ParamFileArguments(MetaVelvet_Parameter())
    	metavelvet_args = "%s" % (params)
    	print "meta-velvetg: " + metavelvet_args

    
    def concat(self, settings, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        params = ParamFileArguments(Concat_Parameter())
        if len(Settings.input) > 1:
        	arguments = "-i %s -j %s -o %s -t %s %s " % (sys.path[0] + os.sep + str(Settings.input[0]),
												  		 sys.path[0] + os.sep + str(Settings.input[1]),
												  		 Settings.output + os.sep + outputdir, Settings.threads,
												  		 params)
        else:
        	arguments = "-i %s -o %s -t %s %s " % (sys.path[0] + os.sep + str(Settings.input),
												  		 Settings.output + os.sep + outputdir, Settings.threads,
												  		 params)
        consoleOutput("Concat", params)
        aln = open(Settings.output + os.sep + outputdir + os.sep + "alignments.txt", "w")
        p = subprocess.Popen(shlex.split(Settings.CONCAT + " " + arguments), stdout=aln, stderr=subprocess.STDOUT)
        p.wait()
        moveFiles(Settings.output + os.sep , Settings.output + os.sep + outputdir + os.sep)
    
    def blastn(self, settings, outputdir):
        params = ParamFileArguments(Blastn_Parameter())
        print "Blastn: "+params
    
    def metaCV(self,settings,outputdir):
        params = ParamFileArguments(MetaCV_Parameter())
        print "MetaCV: "+params
