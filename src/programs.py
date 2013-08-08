#  normal imports
import subprocess
import shlex
import sys, os
import shutil
import time
# own imports
from src.utils import  getDHMS, createOutputDir, ParamFileArguments, moveFiles, testForFQ,logging,updateReads, convertInput
from src.settings import Settings, FastQC_Parameter, TrimGalore_Parameter, Concat_Parameter, Velveth_Parameter, Velvetg_Parameter, MetaVelvet_Parameter, Blastn_Parameter, MetaCV_Parameter,\
    FLASH_Parameter


class Programs:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
       
    # handle the program FastQC - an standard tool to determine the quality of short read sequencing files 
    def fastqc(self, outputdir):
    
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        logging('\nStep:       Quality analysis with FastQC \n')
        logging('Arguments: ' + ParamFileArguments(FastQC_Parameter()) + '\n\n')
        if (Settings.input[0].endswith(".fastq")):
            # start FastQC and wait until task complete
            p = subprocess.Popen(shlex.split('%s -t %s -o %s -q --extract %s %s' % (Settings.FASTQC, 
                                                                                    Settings.threads, 
                                                                                    Settings.output + os.sep + outputdir,
                                                                                    ParamFileArguments(FastQC_Parameter()),
                                                                                    convertInput(Settings.input))))
            p.wait()

            # update the Settings.quality_report var for log purposes
            for r, d, f in os.walk(Settings.output + os.sep + outputdir + os.sep):
                for files in f:
                    if files.endswith('_data.txt'):
                        Settings.quality_report.append(os.path.join(r, files))
        else:
            logging("! ERROR: %s not a fastq file! \n"%(' '.join(str(i)for i in Settings.input)))
                        
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        
        
        return True
       
    def trimming(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        logging('\nStep:       Quality trimming and filtering \n')
        logging('Arguments: ' + ParamFileArguments(TrimGalore_Parameter()) + '\n\n')
        
        # start TrimGalore and wait until task complete
        trimlog = open(Settings.logdir + 'trim.log.txt', 'w')
        if Settings.verbose:
            
            p = subprocess.Popen(shlex.split('%s %s -o %s %s' % (Settings.TRIMGALORE, 
                                                                 ParamFileArguments(TrimGalore_Parameter())
                                                                 , (Settings.output + os.sep + outputdir),
                                                                 convertInput(Settings.input))),
                                 stderr=subprocess.PIPE)
            for line in p.stderr:
                logging(line)
                trimlog.write(line)
        else:   
            p = subprocess.Popen(shlex.split('%s %s -o %s %s' % (Settings.TRIMGALORE, 
                                                                 ParamFileArguments(TrimGalore_Parameter()),
                                                                 (Settings.output + os.sep + outputdir),
                                                                 convertInput(Settings.input)))
                                 , stdout=subprocess.PIPE, stderr=trimlog)
        p.wait()
        
        # search for the processed input files and update input files in settings object
    
        if len(Settings.input) > 1:
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][1],
						      Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][0]]
        else:
            Settings.input = [Settings.output + os.sep + outputdir + os.sep + [f for f in os.listdir(Settings.output + os.sep + outputdir) if (f.endswith('.fq') and 'val' in f)][0]]
        
        # print out the processing time of this step
        updateReads(Settings.input[0])
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def assembly(self, outputdir):

        createOutputDir(Settings.output + os.sep + outputdir + os.sep)
        # update information on cmd
        logging('\nStep:       Creating Hastables \n')
        logging('Arguments: ' + ParamFileArguments(Velveth_Parameter()) + '\n\n')
        # start velveth and wait for completion
        velvethlog = open(Settings.logdir + 'velveth.log.txt', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s %s %s %s -fmtAuto %s ' % (Settings.VELVETH, 
                                                                           Settings.output + os.sep + outputdir,
                                                                           Settings.kmer, 
                                                                           ParamFileArguments(Velveth_Parameter()) ,
                                                                           convertInput(Settings.input))),
                                 stdout=subprocess.PIPE, stderr=open(Settings.logdir + 'velveth.err.txt', 'w')) 
            for line in p.stdout:
                logging(line)
                velvethlog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s %s %s %s -fmtAuto %s ' % (Settings.VELVETH, 
                                                                           Settings.output + os.sep + outputdir,
                                                                           Settings.kmer, 
                                                                           ParamFileArguments(Velveth_Parameter()) ,
                                                                           convertInput(Settings.input))),
                                 stdout=velvethlog, stderr=open(Settings.logdir + 'velveth.err.txt', 'w'))
        p.wait()
        
        # update information on cmd
        logging('\nStep:       Create Graph for Assembly \n')
        logging('Arguments: ' + ParamFileArguments(Velvetg_Parameter()) + '\n\n')
        
        # start velvetg to create the graph for the metagenomic assembly
        velvetglog = open(Settings.logdir + 'velvetg.log.txt', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s %s %s' % (Settings.VELVETG, 
                                                           Settings.output + os.sep + outputdir,
                                                           ParamFileArguments(Velvetg_Parameter()))),
                                 stdout=subprocess.PIPE, stderr=open(Settings.logdir + 'velvetg.err.txt', 'w'))
            for line in p.stdout:
                logging(line)
                velvetglog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s %s %s' % (Settings.VELVETG, 
                                                           Settings.output + os.sep + outputdir,
                                                           ParamFileArguments(Velvetg_Parameter()))),
                                 stdout=velvetglog, stderr=open(Settings.logdir + 'velvetg.err.txt', 'w'))
        p.wait()
        
        # update information on cmd
        logging('\nStep:       Search for metagenomic Contigs \n')
        logging('Arguments: ' + ParamFileArguments(MetaVelvet_Parameter()) + '\n')
        metavelvetlog = open(Settings.logdir + 'meta-velvetg.log.txt', 'w')
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s %s %s' % (Settings.METAVELVET, 
                                                           Settings.output + os.sep + outputdir,
                                                           ParamFileArguments(MetaVelvet_Parameter()))),
                                 stdout=subprocess.PIPE, stderr=open(Settings.logdir + 'meta-velvetg.err.txt', 'w'))
            for line in p.stdout:
                logging(line)
                metavelvetlog.write(line)
        else:
            p = subprocess.Popen(shlex.split('%s %s%s' % (Settings.METAVELVET, 
                                                          Settings.output + os.sep + outputdir + os.sep,
                                                          ParamFileArguments(MetaVelvet_Parameter()))),
                                 stdout=metavelvetlog, stderr=open(Settings.logdir + 'meta-velvetg.err.txt', 'w'))
        p.wait()
        
        # update Settings.contigs for further processing
        Settings.contigs = [Settings.output + os.sep + outputdir + os.sep + 'meta-velvetg.contigs.fa']
        updateReads(Settings.contigs[0])
        
        # print out the processing time of this step
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def flash(self, outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        logging('\nStep:       Concatenate the reads with FLASH \n')
        logging('Arguments: ' + ParamFileArguments(FLASH_Parameter()) + '\n')
        flashlog = open(Settings.logdir + 'flash.log.txt', 'w')
            if Settings.verbose:
                p = subprocess.Popen(shlex.split('%s -d %s %s %s' % (Settings.FLASH,
                                                                     Settings.output + os.sep + outputdir,
                                                                     ParamFileArguments(FLASH_Parameter()),
                                                                     convertInput(Settings.input))),
                                     stdout=subprocess.PIPE)
                for line in p.stdout:
                    logging(line)
                    flashlog.write(line)
            else:
                p = subprocess.Popen(shlex.split('%s -d %s %s %s' % (Settings.FLASH,
                                                                     Settings.output + os.sep + outputdir,
                                                                     ParamFileArguments(FLASH_Parameter()),
                                                                     convertInput(Settings.input))),
                                     stdout=flashlog)
        elif len(Settings.input) ==1 and FLASH_Parameter().interleavedInput:
            if Settings.verbose:
                p = subprocess.Popen(shlex.split('%s -d %s %s %s' % (Settings.FLASH,
                                                                     Settings.output + os.sep + outputdir,
                                                                     ParamFileArguments(FLASH_Parameter()),
                                                                     Settings.input[1])),
                                    stdout=subprocess.PIPE)
                for line in p.stdout:
                    logging(line)
                    flashlog.write(line)
            else:
                p = subprocess.Popen(shlex.split('%s -d %s %s %s' % (Settings.FLASH,
                                                                     Settings.output + os.sep + outputdir,
                                                                     ParamFileArguments(FLASH_Parameter()),
                                                                     Settings.input[1])),
                                     stdout=flashlog)
                
        else:
            logging('Nothing to merge - PLease check input')
            return False
        
        Settings.contigs = [Settings.output + os.sep + outputdir + os.sep + 'out.extendedFrags.fastq']
        updateReads(Settings.contigs[0])
        # print out the processing time of this step
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        return True
                
        
        
    def concat(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update information on cmd
        logging('\nStep:       Concatenate the reads with stitch \n')
        logging('Arguments: ' + ParamFileArguments(Concat_Parameter()) + '\n')
        
        concatlog = open(Settings.logdir + 'concat.log.txt', 'w')
        if len(Settings.input) > 1:
            # for paired end files
            
            if Settings.verbose:
                p = subprocess.Popen(shlex.split('%s -i %s -j %s -o %s -t %s %s ' % (Settings.CONCAT, 
                                                                                     str(Settings.input[0]),
                                                                                     str(Settings.input[1]),
                                                                                     Settings.output + os.sep + outputdir, 
                                                                                     Settings.threads,
                                                                                     ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt', 'w'),
                                     stderr=subprocess.PIPE)
                for line in p.stderr:
                    logging(line)
                    concatlog.write(line)
            else:
                p = subprocess.Popen(shlex.split('%s -i %s -j %s -o %s -t %s %s ' % (Settings.CONCAT, 
                                                                                     str(Settings.input[0]),
                                                                                     str(Settings.input[1]),
                                                                                     Settings.output + os.sep + outputdir, 
                                                                                     Settings.threads,
                                                                                     ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt', 'w'),
                                     stderr=concatlog)
        else:
            # for single end files
            if Settings.verbose:
                p = subprocess.Popen(shlex.split('%s -i %s -o %s -t %s %s ' % (Settings.CONCAT, 
                                                                               str(Settings.input),
                                                                               Settings.output + os.sep + outputdir, 
                                                                               Settings.threads,
                                                                               ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt'),
                                     stderr=subprocess.PIPE)
                for line in p.stderr:
                    logging(line)
                    concatlog.write(line)
            else:
                p = subprocess.Popen(shlex.split('%s -i %s -o %s -t %s %s ' % (Settings.CONCAT, 
                                                                               str(Settings.input),
                                                                               Settings.output + os.sep + outputdir, 
                                                                               Settings.threads,
                                                                               ParamFileArguments(Concat_Parameter()))),
                                     stdout=open(Settings.output + os.sep + outputdir + os.sep + 'alignments.txt', 'w'),
                                     stderr=concatlog)
        p.wait()
        
        # move files from the first level to the specified output folder
        moveFiles(Settings.output + os.sep , Settings.output + os.sep + outputdir + os.sep, '.fastq')
        # update the Setings.input var for further processing
        Settings.contigs = [Settings.output + os.sep + outputdir + os.sep + 'concat-contigs.fastq']
        updateReads(Settings.input[0])
        
        # print out the processing time of this step
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def assembly_with_Preprocessing(self,outputdir):
        
        self.flash(outputdir)
        Settings.input = Settings.contigs
        self.assembly(outputdir)
        return True
    
    def convertToFasta(self, outputdir):
        
        logging('\nStep:       Converting Fastq to Fasta \n')
        
        # if the assembly step was skipped --> merge the two paired-end files
        if len(Settings.blast_input) > 1:
            merge = open(Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq', 'wb')
            shutil.copyfileobj(open(Settings.input[0], 'rb'), merge)
            shutil.copyfileobj(open(Settings.input[1], 'rb'), merge)
            merge.close()
            Settings.blast_input = [Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq']   

        # convert fastq files to fasta
        p = subprocess.Popen(shlex.split('%s -n -Q33 -i %s -o %s' % (Settings.CONVERTER, 
                                                                     Settings.blast_input[0],
                                                                     Settings.output + os.sep + outputdir + os.sep + 'contigs.fasta')))
        p.wait()
        
        # remove the intermediary file 
        if os.path.exists(Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq'):
            os.remove(Settings.output + os.sep + outputdir + os.sep + 'merged.reads.fastq')
        # update the Input for blastn
        Settings.blast_input = [Settings.output + os.sep + outputdir + os.sep + 'contigs.fasta']
        
    def blastn(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        
        # if the assembled reads will be used for classifcation
        if Settings.use_contigs == True:
            Settings.blast_input = Settings.contigs
        else:
            Settings.blast_input = Settings.input

        # check the input files for filetype - fastq Files need conversion into fasta for blastn
        if len(Settings.blast_input) > 1: 
            if testForFQ(' '.join(str(i)for i in Settings.blast_input)):
                self.convertToFasta(outputdir)
        else: 
            if testForFQ(Settings.blast_input[0]):
                self.convertToFasta(outputdir)
            
        # update information of cmd
        logging('\nStep:       Classify with Blastn \n')
        logging('Arguments: ' + ParamFileArguments(Blastn_Parameter()) + '\n')
        # create outputfile name
        if Blastn_Parameter().outfmt == 5:
            outfile = 'blastn.xml' 
        else: 
            outfile = 'blastn.tab'
            
        # start blastn and wait until completion
        p = subprocess.Popen(shlex.split('%s -db %s -query %s -out %s -num_threads %s %s ' % 
                                         (Settings.BLASTN,
                                          Settings.blastdb_nt,
                                          Settings.blast_input[0],
                                          Settings.output + os.sep + outputdir + os.sep + outfile,
                                          Settings.threads, ParamFileArguments(Blastn_Parameter()))))
        p.wait()
        
        # save path to the blastn results
        Settings.blast_output = Settings.output + os.sep + outputdir + os.sep + outfile
        
        # print out the processing time of this step
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        
        return True
        
    def metaCV(self, outputdir):
        
        createOutputDir(Settings.output + os.sep + outputdir)
        # update the information of cmd
        logging('\nStep:       Classify with MetaCV \n')
        logging('Arguments: ' + ParamFileArguments(MetaCV_Parameter()) + '\n')
        # start metaCV and wait until completion ATTENTION: need 32GB RAM
        metacvlog = open(Settings.logdir + 'metacv.log', 'w')
        if Settings.verbose:
            if Settings.use_contigs == True:
                p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % 
                                                 (Settings.METACV,
                                                  Settings.metacv_db,
                                                  ' '.join(str(i)for i in Settings.contigs),
                                                  'metpipe',
                                                   ParamFileArguments(MetaCV_Parameter()))),
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            else:
                p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % 
                                                 (Settings.METACV,
                                                  Settings.metacv_db,
                                                  ' '.join(str(i)for i in Settings.input),
                                                  'metpipe',
                                                   ParamFileArguments(MetaCV_Parameter()))),
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE) 
            for line in p.stderr:
                    logging(line)
                    metacvlog.write(line)
        else:
            if Settings.use_contigs == True:
                p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % 
                                                 (Settings.METACV,
                                                  Settings.metacv_db,
                                                  ' '.join(str(i)for i in Settings.contigs),
                                                  'metpipe',
                                                   ParamFileArguments(MetaCV_Parameter()))),
                                 stderr=metacvlog, stdout=subprocess.PIPE)
            else:
                p = subprocess.Popen(shlex.split('%s classify %s %s %s %s' % 
                                                 (Settings.METACV,
                                                  Settings.metacv_db,
                                                  ' '.join(str(i)for i in Settings.input),
                                                  'metpipe',
                                                  ParamFileArguments(MetaCV_Parameter()))),
                                 stderr=metacvlog, stdout=subprocess.PIPE)
        p.wait()
        
        # move all necessary files into metacv output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, '.csv')
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, '.res')
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir, '.faa')    
        # save the path to the metaCV result file 
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, 
                                                                    Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith('.res')][0]))))
        updateReads(Settings.metaCV_output[0])
        
        # update the information of cmd
        logging('\nStep:       Create summary of MetaCV results \n')
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
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, 
                                                                    Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith('.fun_hist') or f.endswith('.tax_hist')][0]))))
        
        # create a list of all found taxa in the metacv result
        if Settings.verbose:
            p = subprocess.Popen(shlex.split('%s res2sum %s %s %s' % (Settings.METACV, 
                                                                      Settings.metacv_db,
                                                                      Settings.metaCV_output[0], 
                                                                      'metpipe.res2sum')))
        else:
            p = subprocess.Popen(shlex.split('%s res2sum %s %s %s' % (Settings.METACV, 
                                                                      Settings.metacv_db,
                                                                      Settings.metaCV_output[0], 
                                                                      'metpipe.res2sum')),
                                stderr=open(Settings.logdir + 'metacv.log', 'w'))
        p.wait()
        
        # move the list to the output folder
        moveFiles(sys.path[0] + os.sep, Settings.output + os.sep + outputdir + os.sep, '.res2sum')
        Settings.metaCV_output.append(os.path.normpath(os.path.join(sys.path[0] + os.sep, 
                                                                    Settings.output + os.sep + outputdir + os.sep,
                                                                    str([f for f in os.listdir(Settings.output + os.sep + outputdir) if f.endswith('.res2sum')][0]))))
        
        # print out the processing time of this step
        logging('processed in: ' + getDHMS(time.time() - Settings.actual_time) + '\n')
        Settings.actual_time = time.time()
        
        return True
    
    def analysis(self, outputdir):
        if Settings.blast_output:
            if Settings.blast_output.endswith(".xml"):
                # parser the Blast xml file to a DB
                print ParamFileArguments(xmlParser())
                p = subprocess.Popen(shlex.split('%s -o %s %s %s %s' % (Settings.PARSER,
                                                                        Settings.output + os.sep + outputdir + os.sep +"metpipe.db", 
                                                                        ParamFileArguments(xmlParser()),
                                                                        Settings.blast_output[0])))
                # R Analyse starten
                #p = subprocess.Popen(shlex.split('R -q -f annotate.R -%s -%s' % ) )
            
            else:
                print 'Tabular einlesen'
                p = subprocess.Popen(shlex.split('%s %s') % (Settings.KRONA_BLAST,
                                                         Settings.blast_output[0]))
            return True
        else:
            print 'no Blast Output found'
            return False
            
            
            
        
        
        
        
        
        
        
        
