#  normal imports
import subprocess
import shlex
import sys, os
import shutil
import time
# own imports
from src.utils import  getDHMS, createOutputDir, ParamFileArguments, moveFiles, testForFQ
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
        sys.stdout.write('\nStep:       Quality analysis with FastQC \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(FastQC_Parameter()) + '\n\n')
        
        # start FastQC and wait until task complete
        p = subprocess.Popen(shlex.split('%s -t %s -o %s -q --extract %s %s' % (Settings.FASTQC, Settings.threads, Settings.output + os.sep + outputdir,
                                                                                ParamFileArguments(FastQC_Parameter()),
                                                                                 ' '.join(str(i)for i in Settings.input))))
        p.wait()

        # update the Settings.quality_report var for log purposes
        for r, d, f in os.walk(Settings.output + os.sep + outputdir + os.sep):
            for files in f:
                if files.endswith('_data.txt'):
                    Settings.quality_report.append(os.path.join(r, files))
        # print out the processing time of this step
        sys.stdout.write('processed in: ' + getDHMS(time.time()-Settings.actual_time)  + '\n')
        Settings.actual_time = time.time()
         
        return True
       
    def trimming(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        sys.stdout.write('\nStep:       Quality trimming and filtering \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(TrimGalore_Parameter()) + '\n\n')
        
        # start TrimGalore and wait until task complete
        trimlog = open(Settings.logdir + 'trim.log.txt', 'w')
        if Settings.verbose:
            
            p = subprocess.Popen(shlex.split('%s %s -o %s %s' % (Settings.TRIMGALORE, ParamFileArguments(TrimGalore_Parameter())
                                                                 , (Settings.output + os.sep + outputdir),
                                                                 ' '.join(str(i)for i in Settings.input))),
                                 stderr=subprocess.PIPE)
            for line in p.stderr:
                sys.stdout.write(line)
                trimlog.write(line)
        else:   
            p = subprocess.Popen(shlex.split('%s %s -o %s %s' % (Settings.TRIMGALORE, ParamFileArguments(TrimGalore_Parameter())
                                                                 , (Settings.output + os.sep + outputdir),
                                                                 ' '.join(str(i)for i in Settings.input)))
                                 , stdout=subprocess.PIPE, stderr=trimlog)
        p.wait()
        
        # search for the processed input files and update input files in settings object
    
        if len(Settings.input) > 1:
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][1],
						      Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][0]]
        else:
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][0]]
        
        # print out the processing time of this step
        sys.stdout.write('processed in: ' + getDHMS(time.time()-Settings.actual_time)  + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def assembly(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir + os.sep)
        # update information on cmd
        sys.stdout.write('\nStep:       Creating Hastables \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(Velveth_Parameter()) + '\n\n')
        # start velveth and wait for completion
        velvethlog = open(Settings.logdir + 'velveth.log.txt', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s %s %s %s -fmtAuto %s ' % (Settings.VELVETH, Settings.output + os.sep + outputdir,
                                                                           Settings.kmer, ParamFileArguments(Velveth_Parameter()) ,
                                                                           ' '.join(str(i)for i in Settings.input))),
                                 stdout=subprocess.PIPE,stderr=open(Settings.logdir + 'velveth.err.txt','w')) 
            for line in p.stdout:
                sys.stdout.write(line)
                velvethlog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s %s %s %s -fmtAuto %s ' % (Settings.VELVETH, Settings.output + os.sep + outputdir,
                                                                           Settings.kmer, ParamFileArguments(Velveth_Parameter()) ,
                                                                           ' '.join(str(i)for i in Settings.input))),
                                 stdout=velvethlog,stderr=open(Settings.logdir + 'velveth.err.txt','w'))
        p.wait()
        
        # update information on cmd
        sys.stdout.write('\nStep:       Create Graph for Assembly \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(Velvetg_Parameter()) + '\n\n')

        # start velvetg to create the graph for the metagenomic assembly
        velvetglog = open(Settings.logdir + 'velvetg.log.txt', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s %s %s' % (Settings.VELVETG, Settings.output + os.sep + outputdir,
                                                           ParamFileArguments(Velvetg_Parameter()))),
                                 stdout=subprocess.PIPE,stderr=open(Settings.logdir + 'velvetg.err.txt','w'))
            for line in p.stdout:
                sys.stdout.write(line)
                velvetglog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s %s %s' % (Settings.VELVETG, Settings.output + os.sep + outputdir,
                                                           ParamFileArguments(Velvetg_Parameter()))),
                                 stdout=velvetglog,stderr=open(Settings.logdir + 'velvetg.err.txt','w'))
        p.wait()
        
        # update information on cmd
        sys.stdout.write('\nStep:       Search for metagenomic Contigs \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(MetaVelvet_Parameter()) + '\n')
        metavelvetlog = open(Settings.logdir + 'meta-velvetg.log.txt', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s %s %s' % (Settings.METAVELVET,Settings.output + os.sep + outputdir, 
                                                          ParamFileArguments(MetaVelvet_Parameter()))),
                                 stdout=subprocess.PIPE,stderr=open(Settings.logdir + 'meta-velvetg.err.txt','w'))
            for line in p.stdout:
                sys.stdout.write(line)
                metavelvetlog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s %s%s' % (Settings.METAVELVET,Settings.output + os.sep + outputdir+os.sep, 
                                                           ParamFileArguments(MetaVelvet_Parameter()))),
                                 stdout=metavelvetlog,stderr=open(Settings.logdir + 'meta-velvetg.err.txt','w'))
        p.wait()
        
        # update Settings.input for further processing
        Settings.input = [Settings.output + os.sep + outputdir + os.sep + 'meta-velvetg.contigs.fa']
        
        # print out the processing time of this step
        sys.stdout.write('processed in: ' + getDHMS(time.time()-Settings.actual_time)  + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def concat(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        sys.stdout.write('\nStep:       Concatenate the reads \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(Concat_Parameter()) + '\n')
        
        concatlog = open(Settings.logdir + 'concat.log.txt', 'w')
        if len(Settings.input) > 1:
            # for paired end files
            
            if Settings.verbose:
                p = subprocess.Popen(shlex.split('%s -i %s -j %s -o %s -t %s %s ' % (Settings.CONCAT, str(Settings.input[0]),
                                                                                     str(Settings.input[1]),
                                                                                     Settings.output + os.sep + outputdir, Settings.threads,
                                                                                     ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt', 'w'),
                                     stderr=subprocess.PIPE)
                for line in p.stderr:
                    sys.stdout.write(line)
                    concatlog.write(line)
            else:
                p = subprocess.Popen(shlex.split('%s -i %s -j %s -o %s -t %s %s ' % (Settings.CONCAT, str(Settings.input[0]),
                                                                                     str(Settings.input[1]),
                                                                                     Settings.output + os.sep + outputdir, Settings.threads,
                                                                                     ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt', 'w'),
                                     stderr=concatlog)
        else:
            # for single end files
            if Settings.verbose:
                p = subprocess.Popen(shlex.split('%s -i %s -o %s -t %s %s ' % (Settings.CONCAT, str(Settings.input),
                                                                               Settings.output + os.sep + outputdir, Settings.threads,
                                                                               ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt'),
                                     stderr=subprocess.PIPE)
                for line in p.stderr:
                    sys.stdout.write(line)
                    concatlog.write(line)
            else:
                p = subprocess.Popen(shlex.split('%s -i %s -o %s -t %s %s ' % (Settings.CONCAT, str(Settings.input),
                                                                               Settings.output + os.sep + outputdir, Settings.threads,
                                                                               ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt', 'w'),
                                     stderr=concatlog)
        p.wait()
        
        # move files from the first level to the specified output folder
        moveFiles(Settings.output + os.sep , Settings.output + os.sep + outputdir + os.sep, '.fastq')
        # update the Setings.input var for further processing
        Settings.input = [Settings.output + os.sep + outputdir + os.sep + 'concat-contigs.fastq']
        
        # print out the processing time of this step
        sys.stdout.write('processed in: ' + getDHMS(time.time()-Settings.actual_time)  + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def convertToFasta(self, outputdir):
        
        sys.stdout.write('\nStep:       Converting Fastq to Fasta \n')
        
        # if the assembly step was skipped --> merge the two paired-end files
        if len(Settings.input) > 1:
            merge = open(Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq', 'wb')
            shutil.copyfileobj(open(Settings.input[0], 'rb'), merge)
            shutil.copyfileobj(open(Settings.input[1], 'rb'), merge)
            merge.close()
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq']   
        
        # convert fastq files to fasta
        p = subprocess.Popen(shlex.split('%s -n -Q33 -i %s -o %s' % (Settings.CONVERTER, Settings.input[0],
                                                                     Settings.output + os.sep + outputdir + os.sep + 'contigs.fasta')))
        p.wait()
        
        # remove the intermediary file 
        if os.path.exists(Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq'):
            os.remove(Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq')
        # update the Settings.input var
        Settings.input = [Settings.output + os.sep + outputdir + os.sep + 'contigs.fasta']
        
    def blastn(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        
        # check the input files for filetype - fastq Files need conversion into fasta for blastn
        if len(Settings.input) > 1: 
            if testForFQ(' '.join(str(i)for i in Settings.input)):
                self.convertToFasta(outputdir)
        else: 
            if testForFQ(Settings.input[0]):
                self.convertToFasta(outputdir)
            
        # update information of cmd
        sys.stdout.write('\nStep:       Classify with Blastn \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(Blastn_Parameter()) + '\n')
        # create outputfile name
        if Blastn_Parameter().outfmt == 5:
            outfile = 'blastn.xml' 
        else: 
            outfile = 'blastn.tab'
            
        # start blastn and wait until completion
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % (Settings.BLASTN, Settings.blastdb_nt, Settings.input[0],
                                                                      Settings.output + os.sep + outputdir + os.sep + outfile,
                                                                      Settings.threads, ParamFileArguments(Blastn_Parameter()))))
        p.wait()
        
        # save path to the blastn results
        Settings.blast_output = Settings.output + os.sep + outputdir + os.sep + outfile
        
        # print out the processing time of this step
        sys.stdout.write('processed in: ' + getDHMS(time.time()-Settings.actual_time)  + '\n')
        Settings.actual_time = time.time()
        
        return True
        
    def metaCV(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update the information of cmd
        sys.stdout.write('\nStep:       Classify with MetaCV \n')
        sys.stdout.write('Arguments: ' + ParamFileArguments(MetaCV_Parameter()) + '\n')
        # start metaCV and wait until completion ATTENTION: need 32GB RAM
        metacvlog=open(Settings.logdir + 'metacv.log', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % (Settings.METACV, Settings.metacv_db,
                                                                          ' '.join(str(i)for i in Settings.input), 'metpipe',
                                                                          ParamFileArguments(MetaCV_Parameter()))),
                                 stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            for line in p.stderr:
                    sys.stdout.write(line)
                    metacvlog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % (Settings.METACV, Settings.metacv_db,
                                                                          ' '.join(str(i)for i in Settings.input), 'metpipe',
                                                                          ParamFileArguments(MetaCV_Parameter()))),
                                 stderr=metacvlog,stdout=subprocess.PIPE)
        p.wait()
        
        # move all necessary files into metacv output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, '.csv')
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, '.res')
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, '.faa')    
        # save the path to the metaCV result file 
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith('.res')][0]))))
        
        # update the information of cmd
        sys.stdout.write('\nStep:       Create summary of MetaCV results \n')
        # create an summary of the metacv run
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s res2table %s %s %s --threads=%s' % (Settings.METACV, 
                                                                                     Settings.metacv_db, 
                                                                                     Settings.metaCV_output[0], 
                                                                                     'metpipe.res2table', 
                                                                                     Settings.threads)))
        else:
            p = subprocess.Popen(shlex.split('%s res2table %s %s %s --threads=%s' % (Settings.METACV, 
                                                                                     Settings.metacv_db, 
                                                                                     Settings.metaCV_output[0], 
                                                                                     'metpipe.res2table', 
                                                                                     Settings.threads)),
                                 stderr=open(Settings.logdir + 'metacv.log', 'w'))
        p.wait()
        
        # move the summary to the output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, '.res2table')
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, '.fun_hist')
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, '.tax_hist')
        # save the path to the summary of metacv
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith('.fun_hist') or f.endswith('.tax_hist')][0]))))
        
        # create a list of all found taxa in the metacv result
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s res2sum %s %s %s' % (Settings.METACV, Settings.metacv_db, 
                                                                      Settings.metaCV_output[0], 'metpipe.res2sum')))
        else:
            p = subprocess.Popen(shlex.split('%s res2sum %s %s %s' % (Settings.METACV, Settings.metacv_db, 
                                                                      Settings.metaCV_output[0], 'metpipe.res2sum')),
                                stderr=open(Settings.logdir + 'metacv.log', 'w'))
        p.wait()
        
        # move the list to the output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, '.res2sum')
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith('.res2sum')][0]))))
        
        # print out the processing time of this step
        sys.stdout.write('processed in: ' + getDHMS(time.time()-Settings.actual_time)  + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def summary(self):
        pass
        
        
        
        
        
        
