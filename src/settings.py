from ConfigParser import SafeConfigParser
import ConfigParser
import sys
import os

# class for general settings of the pipeline and variables needed from every program

class General:

    # general settings
    threads = 8
    verbose = False
    skip = ''
    starting_time = ''
    actual_time = ''
    step_number = 1
    # Program Settings
    trim = True
    quality = True
    use_contigs = False
    assembler = ''
    classify = 'both'
    
    
    def __init__(self, threads = None, verbose = False, skip = None, starting_time = None,
                 trim = None, quality = None, krona = None, use_contigs = None, assembler = None,
                 annotation = None, step_number = None):

        self.threads = threads
        self.verbose = verbose
        self.skip = skip.lower()
        self.starting_time = starting_time
        self.actual_time = starting_time
        self.trim = trim
        self.quality = quality 
        self.krona = krona
        self.use_contigs = use_contigs
        self.assembler = assembler.lower()
        self.annotation = annotation.lower() 
        self.step_number = step_number

    def get_threads(self):
        return self.threads
        
    def get_verbose(self):
        return self.verbose
        
    def get_starting_time(self):
        return self.starting_time
        
    def get_actual_time(self):
        return self.actual_time
    
    def get_parameterfile(self):
        return self.param
    
    def get_quality(self):
        return self.quality
    
    def get_trim(self):
        return self.trim
    
    def get_krona(self):
        return self.krona
    
    def get_assembler(self):
        return self.assembler
    
    def get_annotation(self):
        return self.annotation
    
    def get_skip(self):
        return self.skip.split(',')
    
    def get_use_contigs(self):
        return self.use_contigs
    
    def get_step_number(self):
        return self.step_number
    
    def set_step_number(self, value):
        self.step_number = value
        
        
class Executables:
    
    conf = ConfigParser.SafeConfigParser()
    FASTQC = ''
    TRIMGALORE = ''
    VELVETH = ''
    VELVETG = ''
    METAVELVET = ''
    FLASH = ''
    BLASTN = ''
    BLAST_DB = ''
    METACV_DB = ''
    blastn = ''
    CONVERTER = ''
    PARSER = ''
    ANNOTATE = ''
    SUBSET = ''
    KRONA_BLAST = ''
    KRONA_TEXT = ''
    
    def __init__(self, parameter_file):
        
        self.conf.read(parameter_file)
        self.FASTQC = os.path.normpath(self.conf.get('FastQC', 'path')) + os.sep + 'fastqc' if self.conf.has_option('FastQC', 'path') else ''
        self.TRIMGALORE = os.path.normpath(self.conf.get('TrimGalore', 'path')) + os.sep + 'trim_galore' if self.conf.has_option('TrimGalore', 'path') else ''
        self.FLASH = os.path.normpath(self.conf.get('FLASH', 'path')) + os.sep + 'flash' if self.conf.has_option('FLASH', 'path') else ''
        self.VELVETH = os.path.normpath(self.conf.get('Velvet', 'path')) + os.sep + 'velveth' if self.conf.has_option('Velvet', 'path') else ''
        self.VELVETG = os.path.normpath(self.conf.get('Velvet', 'path')) + os.sep + 'velvetg' if self.conf.has_option('Velvet', 'path') else ''
        self.METAVELVET = os.path.normpath(self.conf.get('MetaVelvet', 'path')) + os.sep + 'meta-velvetg' if self.conf.has_option('MetaVelvet', 'path') else ''
        self.METACV = os.path.normpath(self.conf.get('MetaCV', 'path')) + os.sep + 'metacv' if self.conf.has_option('MetaCV', 'path') else ''
        self.METACV_DB = os.path.normpath(self.conf.get('MetaCV', 'db')) + os.sep + 'cvk6_2059' if self.conf.has_option('MetaCV', 'db') else ''
        self.BLASTN = os.path.normpath(self.conf.get('blastn', 'path')) + os.sep + 'blastn' if self.conf.has_option('blastn', 'path') else ''
        self.BLAST_DB = os.path.normpath(self.conf.get('blastn', 'db')) + os.sep + 'nt' if self.conf.has_option('blastn', 'db') else ''
        self.CONVERTER = os.path.normpath(self.conf.get('FastX', 'path')) + os.sep + 'fastq_to_fasta' if self.conf.has_option('FastX', 'path') else ''
        self.PARSER = os.path.normpath(self.conf.get('blastParser', 'path')) + os.sep + 'bigBlastParser' if self.conf.has_option('blastParser', 'path') else ''
        self.ANNOTATE = sys.path[0] + os.sep + 'src' + os.sep + 'annotate.R' 
        self.SUBSET = sys.path[0] + os.sep + 'src' + os.sep + 'subsetDB.R' 
        self.KRONA_BLAST = os.path.normpath(self.conf.get('Krona Tools', 'path')) + os.sep + 'ktImportBLAST' if self.conf.has_option('Krona Tools', 'path') else ''
        self.KRONA_TEXT = os.path.normpath(self.conf.get('Krona Tools', 'path')) + os.sep + 'ktImportText' if self.conf.has_option('Krona Tools', 'path') else ''
        self.KRONA_CONVERTER = sys.path[0] + os.sep + 'src' + os.sep + 'convert_for_krona.R' 
        
    def get_FastQC(self):
        return self.FASTQC
    
    def get_TrimGalore(self):
        return self.TRIMGALORE
    
    def get_Flash(self):
        return self.FLASH
    
    def get_Velveth(self):
        return self.VELVETH
    
    def get_Velvetg(self):
        return self.VELVETG
    
    def get_MetaVelvet(self):
        return self.METAVELVET
    
    def get_MetaCV(self):
        return self.METACV
    
    def get_MetaCV_DB(self):
        return self.METACV_DB
    
    def get_Blastn(self):
        return self.BLASTN
    
    def get_Blastn_DB(self):
        return self.BLAST_DB
    
    def get_Converter(self):
        return self.CONVERTER
    
    def get_Parser(self):
        return self.PARSER
    
    def get_Annotate(self):
        return self.ANNOTATE
    
    def get_Subset(self):
        return self.SUBSET
    
    def get_Krona_Blast(self):
        return self.KRONA_BLAST
    
    def get_Krona_Text(self):
        return self.KRONA_TEXT  

class FileSettings:
    
    # important dirs for the pipeline
    output = ''
    logdir = ''
    paramfile = ''
    quality_dir = ''
    trim_dir = ''
    concat_dir = ''
    assembly_dir = ''
    blastn_dir = ''
    metacv_dir = ''
    parsed_db_dir = ''
    annotated_db_dir = ''
    subseted_db_dir = ''
    # variables for the input and output of the programs
    raw = []
    input = []
    quality_report = []
    preprocessed_output = []
    concatinated_output = []
    assembled_output = []
    blastn_output = []
    metacv_output = []
    parser_output = []
    annotated_output = []
    subseted_output = []
    
    def __init__(self, raw = None, output = None, parameter_file = None):
        
        self.paramfile = parameter_file
        conf = ConfigParser.SafeConfigParser()
        conf.read(self.paramfile)
        self.raw = raw
        self.input = raw
        self.output = output + os.sep
        self.quality_dir = conf.get('General', 'quality_dir') if conf.has_option('General', 'quality_dir') else ''
        self.trim_dir = conf.get('General', 'trim_dir') if conf.has_option('General', 'trim_dir') else ''
        self.concat_dir = conf.get('General', 'concat_dir') if conf.has_option('General', 'concat_dir') else ''
        self.assembly_dir = conf.get('General', 'assembly_dir') if conf.has_option('General', 'assembly_dir') else ''
        self.blastn_dir = conf.get('General', 'blastn_dir') if conf.has_option('General', 'blastn_dir') else ''
        self.metacv_dir = conf.get('General', 'metacv_dir') if conf.has_option('General', 'metacv_dir') else ''
        self.parsed_db_dir = conf.get('General', 'parsed_db_dir') if conf.has_option('General', 'parsed_db_dir') else ''
        self.annotated_db_dir = conf.get('General', 'annotated_db_dir') if conf.has_option('General', 'annotated_db_dir') else ''
        self.subseted_db_dir = conf.get('General', 'subseted_db_dir') if conf.has_option('General', 'subseted_db_dir') else ''
        self.krona_report_dir = conf.get('General', 'krona_report') if conf.has_option('General', 'krona_report') else ''
        self.logdir = conf.get('General', 'log_dir') if conf.has_option('General', 'quality_dir') else ''

    
    def get_parameter_file(self):
        return self.paramfile
        
    def get_output(self):
        return self.output
    
    def get_logdir(self):
        return self.output + self.logdir + os.sep
        
    def get_quality_dir(self):
        return self.output + self.quality_dir 
        
    def get_trim_dir(self):
        return self.output + self.trim_dir
    
    def get_concat_dir(self):
        return self.output + self.concat_dir
        
    def get_assembly_dir(self):
        return self.output + self.assembly_dir
   
    def get_blastn_dir(self):
        return self.output + self.blastn_dir
       
    def get_metacv_dir(self):
        return self.output + self.metacv_dir
    
    def get_parsed_db_dir(self):
        return self.output + self.parsed_db_dir
    
    def get_annotated_db_dir(self):
        return self.output + self.annotated_db_dir
        
    def get_subseted_db_dir(self):
        return self.output + self.subseted_db_dir
    
    def get_krona_report_dir(self):
        return self.output + self.krona_report_dir
        
    def get_raw(self):
        return self.raw
    
    def set_raw(self, value):
        self.raw = value
    
    def get_input(self):
        return self.input
    
    def set_input(self, value):
        self.input = value
        
    def get_quality_report(self):
        return self.quality_report
    
    def set_quality_report(self, value):
        self.quality_report = value
        
    def get_preprocessed_output(self):
        return self.preprocessed_output
    
    def set_preprocessed_output(self, value):
        self.preprocessed_output = value
        
    def get_concatinated_output(self):
        return self.concatinated_output
    
    def set_concatinated_output(self, value):
        self.concatinated_output = value
        
    def get_assembled_output(self):
        return self.assembled_output
    
    def set_assembled_output(self, value):
        self.assembled_output = value
        
    def get_blastn_output(self):
        return self.blastn_output
    
    def set_blastn_output(self, value):
        self.blastn_output = value
        
    def get_metacv_output(self):
        return self.metacv_output
    
    def set_metacv_output(self, value):
        self.metacv_output = value
        
    def get_parser_output(self):
        return self.parser_output
    
    def set_parser_output(self, value):
        self.parser_output = value
    
    def get_annotated_output(self):
        return self.annotated_output
    
    def set_annotated_output(self, value):
        self.annotated_output = value
        
    def get_subseted_output(self):
        return self.subseted_output
    
    def set_subseted_output(self, value):
        self.subseted_output = value
          
# Parameters for FastQC 
class FastQC_Parameter:

    nogroup = False
    contaminants = '' 
    kmers = ''
    # dict with the arguments string
    arguments = {'nogroup' : '--nogroup ', 'contaminants': '-c ', 'kmers': '-k '}
    
    def __init__(self, parameter_file):
        
        conf = ConfigParser.SafeConfigParser()
        conf.read(parameter_file)
        self.nogroup = conf.getboolean('FastQC', 'nogroup') if conf.has_option('FastQC', 'nogroup') else ''
        self.kmers = conf.get('FastQC', 'kmers') if conf.has_option('FastQC', 'kmers') else ''
        self.contaminants = conf.get('FastQC', 'contaminants') if conf.has_option('FastQC', 'contaminents') else ''

# Parameter for TrimGalore!
class TrimGalore_Parameter:

    quality = 20 
    phred = ''
    adapter = ''
    adapter2 = ''
    stringency = ''
    error_rate = 0.1
    length = 150
    paired = False
    retain_unpaired = False
    length_1 = ''
    length_2 = ''
    trim = False
    # dict with the arguments string
    arguments = {'quality':'-q ', 'phred':'--phred', 'adapter':'-a ', 'adapter2':'-a2 ', 'stringency':'-s ',
                 'error_rate':'-e ', 'length':'--length ', 'paired':'--paired', 'retain_unpaired':'--retain_unpaired',
                 'length1':'-r1 ', 'length2':'-r2 ', 'trim':'-t '}
    
    def __init__(self, parameter_file):
        
        conf = ConfigParser.SafeConfigParser()
        conf.read(parameter_file)
        self.quality = conf.get('TrimGalore', 'quality') if conf.has_option('TrimGalore', 'quality') else ''
        self.phred = conf.get('TrimGalore', 'phred') if conf.has_option('TrimGalore', 'phred') else ''
        self.adapter = conf.get('TrimGalore', 'adapter') if conf.has_option('TrimGalore', 'adapter') else ''
        self.adapter2 = conf.get('TrimGalore', 'adapter2') if conf.has_option('TrimGalore', 'adapter2') else ''
        self.stringency = conf.get('TrimGalore', 'stringency') if conf.has_option('TrimGalore', 'stringency') else ''
        self.error_rate = conf.get('TrimGalore', 'error_rate') if conf.has_option('TrimGalore', 'error_rate') else ''
        self.length = conf.get('TrimGalore', 'length') if conf.has_option('TrimGalore', 'length') else ''
        self.paired = conf.getboolean('TrimGalore', 'paired') if conf.has_option('TrimGalore', 'paired') else ''
        self.retain_unpaired = conf.getboolean('TrimGalore', 'retain_unpaired') if conf.has_option('TrimGalore', 'retain_unpaired') else ''
        self.length_1 = conf.get('TrimGalore', 'length_1') if conf.has_option('TrimGalore', 'length_1') else ''
        self.length_2 = conf.get('TrimGalore', 'length_2') if conf.has_option('TrimGalore', 'length_2') else ''
        self.trim = conf.getboolean('TrimGalore', 'trim1') if conf.has_option('TrimGalore', 'trim1') else ''

class FLASH_Parameter:
    
    minOverlap = 10
    maxOverlap = ''
    maxMismatchDensity = ''
    phred = 33
    readLength = 250
    fragmentLength = 400
    fragmentLengthStddev = 40
    interleavedInput = False
    interleavedOutput = True
    arguments = {'minOverlap' : '-m ', 'maxOverlap' : '-M ', 'maxMismatchDensity': '-x ',
                 'phred' : '-p ', 'readLength' : '-r ', 'fragmentLength' : '-f ',
                 'fragmentLengthStddev' : '-s ', 'interleavedInput' : '--interleaved-input',
                 'interleavedOutput' : '--interleaved-output'}
    def __init__(self, parameter_file):
        
        conf = ConfigParser.ConfigParser()
        conf.read(parameter_file)
        self.minOverlap = conf.get('FLASH', 'min-overlap') if conf.has_option('FLASH', 'min-overlap') else ''
        self.maxOverlap = conf.get('FLASH', 'max-overlap') if conf.has_option('FLASH', 'max-overlap') else ''
        self.maxMismatchDensity = conf.get('FLASH', 'max-mismatch-density') if conf.has_option('FLASH', 'max-mismatch-density') else ''
        self.phred = conf.get('FLASH', 'phred-offset') if conf.has_option('FLASH', 'phred-offset') else ''
        self.readLength = conf.get('FLASH', 'read-len') if conf.has_option('FLASH', 'read-len') else ''
        self.fragmentLength = conf.get('FLASH', 'fragment-len') if conf.has_option('FLASH', 'fragment-len') else ''
        self.fragmentLengthStddev = conf.get('FLASH', 'fragment-len-stddev') if conf.has_option('FLASH', 'fragment-len-stddev') else ''
        self.interleavedInput = conf.getboolean('FLASH', 'interleaved-input') if conf.has_option('FLASH', 'interleaved-input') else ''
        self.interleavedOutput = conf.getboolean('FLASH', 'interleaved-output') if conf.has_option('FLASH', 'interleaved-output') else ''
        
# Parameter for velveth
class Velveth_Parameter:
    
    kmer = 85
    file_layout = ''
    read_type = ''
    strand_specific = False
    reuse_Sequences = False
    noHash = False
    create_binary = False
    # dict with the arguments string
    arguments = {'file_layout' : '-', 'read_type' : '-', 'strand_specific':'-strand_specific',
				'reuse_Sequences':'-reuse_Sequences', 'noHash':'-noHash', 'create_binary':'-createBinary'}
    
    def __init__(self, parameter_file):
        
        conf = ConfigParser.ConfigParser()
        conf.read(parameter_file)
        self.file_layout = conf.get('Velvet', 'file_layout') if conf.has_option('Velvet', 'file_layout') else ''
        self.read_type = conf.get('Velvet', 'read_type') if conf.has_option('Velvet', 'read_type') else ''
        self.strand_specific = conf.getboolean('Velvet', 'strand_specific') if conf.has_option('Velvet', 'strand_specific') else ''
        self.reuse_Sequences = conf.getboolean('Velvet', 'reuse_Sequences') if conf.has_option('Velvet', 'reuse_Sequences') else ''
        self.noHash = conf.getboolean('Velvet', 'noHash') if conf.has_option('Velvet', 'noHash') else ''
        self.create_binary = conf.getboolean('Velvet', 'create_binary') if conf.has_option('Velvet', 'create_binary') else ''
        
    def get_kmer(self, parameter_file):
        conf = ConfigParser.ConfigParser()
        conf.read(parameter_file)
        return conf.get('Velvet', 'kmer') if conf.has_option('Velvet', 'kmer') else ''

# Parameter for velvetg
class Velvetg_Parameter:

    cov_cutoff = ''
    ins_length = ''
    read_trkg = False
    min_contig_lgth = 250
    exp_cov = 'auto'
    long_cov_cutoff = ''
    ins_length_long = ''
    ins_length_sd = ''
    scaffolding = True
    max_branch_length = 100
    max_divergence = 0.2
    max_gap_count = 3
    min_pair_count = 5
    max_coverage = False
    coverage_mask = ''
    long_mult_cutoff = 2
    unused_reads = False
    alignments = False
    exportFiltered = False 
    paired_exp_fraction = 0.1
    shortMatePaired = False
    conserveLong = False
    # dict with the arguments string
    arguments = {'cov_cutoff' : '-cov_cutoff ', 'ins_length' : '-ins_length ',
                 'read_trkg' : '-read_trkg ', 'min_contig_lgth' : '-min_contig_lgth ',
                 'exp_cov' : '-exp_cov ', 'long_cov' : '-long_cov ', 'long_cov_cutoff':'-long_cov_cutoff ',
                 'ins_length_long' : '-ins_length_long ', 'ins_length_sd' : '-ins_length_sd ',
                 'scaffolding':'-scaffolding ', 'max_branch_length':'-max_branch_length ',
                 'max_divergence' : '-max_divergence ', 'max_gap_count' : '-max_gap_count ',
                 'min_pair_count' : '-min_pair_count ', 'max_coverage' : '-max_coverage ',
                 'coverage_mask' : '-coverage_mask ', 'long_mult_cutoff' : '-long_mult_cutoff ',
                 'unused_reads' : '-unused_reads ', 'alignments' : '-alignments ',
                 'exportFiltered' : '-exportFiltered ', 'paired_exp_fraction' : '-paired_exp_fraction ',
                 'shortMatePaired' : '-shortMatePaired ', 'conserveLong' : '-conserveLong '}  
    
    def __init__(self, parameter_file):
        
        conf = ConfigParser.ConfigParser()
        conf.read(parameter_file)
        self.cov_cutoff = conf.get('Velvet', 'cov_cutoff') if conf.has_option('Velvet', 'cov_cutoff') else ''
        self.ins_length = conf.get('Velvet', 'read_trkg') if conf.has_option('Velvet', 'read_trkg') else ''
        self.read_trkg = conf.getboolean('Velvet', 'read_trkg') if conf.has_option('Velvet', 'read_trkg') else ''
        self.min_contig_lgth = conf.get('Velvet', 'min_contig_lgth') if conf.has_option('Velvet', 'min_contig_lgth') else ''
        self.exp_cov = conf.get('Velvet', 'exp_cov') if conf.has_option('Velvet', 'exp_cov') else ''
        self.long_cov_cutoff = conf.get('Velvet', 'long_cov_cutoff') if conf.has_option('Velvet', 'long_cov_cutoff') else ''
        self.ins_length_long = conf.get('Velvet', 'ins_length_long') if conf.has_option('Velvet', 'ins_length_long') else ''
        self.ins_length_sd = conf.get('Velvet', 'ins_length_sd') if conf.has_option('Velvet', 'ins_length_sd') else ''
        self.scaffolding = conf.getboolean('Velvet', 'scaffolding') if conf.has_option('Velvet', 'scaffolding') else ''
        self.max_branch_length = conf.get('Velvet', 'max_branch_length') if conf.has_option('Velvet', 'max_branch_length') else ''
        self.max_divergence = conf.get('Velvet', 'max_divergence') if conf.has_option('Velvet', 'max_divergence') else ''
        self.max_gap_count = conf.get('Velvet', 'max_gap_count') if conf.has_option('Velvet', 'max_gap_count') else ''
        self.min_pair_count = conf.get('Velvet', 'min_pair_count') if conf.has_option('Velvet', 'min_pair_count') else ''
        self.max_coverage = conf.get('Velvet', 'max_coverage') if conf.has_option('Velvet', 'max_coverage') else ''
        self.coverage_mask = conf.get('Velvet', 'coverage_mask') if conf.has_option('Velvet', 'coverage_mask') else ''
        self.long_mult_cutoff = conf.get('Velvet', 'long_mult_cutoff') if conf.has_option('Velvet', 'long_mult_cutoff') else ''
        self.unused_reads = conf.getboolean('Velvet', 'unused_reads') if conf.has_option('Velvet', 'unused_reads') else ''
        self.alignments = conf.getboolean('Velvet', 'alignments') if conf.has_option('Velvet', 'alignments') else ''
        self.exportFiltered = conf.getboolean('Velvet', 'exportFiltered') if conf.has_option('Velvet', 'exportFiltered') else ''
        self.paired_exp_fraction = conf.get('Velvet', 'paired_exp_fraction') if conf.has_option('Velvet', 'paired_exp_fraction') else ''
        self.shortMatePaired = conf.getboolean('Velvet', 'shortMatePaired') if conf.has_option('Velvet', 'shortMatePaired') else ''
        self.conserveLong = conf.getboolean('Velvet', 'conserveLong')  if conf.has_option('Velvet', 'conserveLong') else ''
        
# Parameter for meta-velvetg 
class MetaVelvet_Parameter:

    discard_chimera = False
    max_chimera_rate = '' 
    repeat_cov_sd = '' 
    min_split_length = ''
    valid_connections = '' 
    noise_connections = '' 
    use_connections = True 
    report_split_detail = False
    report_subgraph = False 
    exp_covs_meta = ''  
    min_peak_cov = '' 
    max_peak_cov = ''      
    histo_bin_width = ''  
    histo_sn_ratio = ''
    amos_file = False
    coverage_mask = ''
    unused_reads_meta = False 
    alignments_meta = False
    exportFiltered_meta = False
    paired_exp_fraction_meta = ''
    # dict with the arguments string 
    arguments = {'discard_chimera':'-discard_chimera ', 'max_chimera_rate':'-max_chimera_rate ',
				'repeat_cov_sd':'-repeat_cov_sd ', 'min_split_length':'-min_split_length ',
				'valid_connections':'-valid_connections ', 'noise_connections':'-noise_connections ',
				'use_connections':'-use_connections', 'report_split_detail':'-report_split_detail',
				'report_subgraph':'-report_subgraph' , 'exp_covs_meta':'-exp_cov ',
				'min_peak_cov':'-min_peak_cov ', 'max_peak_cov':'-max_peak_cov ',
				'histo_bin_width':'-histo_bin_width ', 'histo_sn_ratio':'-histo_sn_ratio ', 'amos_file':'-amos_file',
				'coverage_mask':'-coverage_mask ', 'unused_reads_meta':'-unused_reads',
				'alignments_meta':'-alignments', 'exportFiltered_meta':'-exportFiltered',
				'paired_exp_fraction_meta': '-paired_exp_fraction '}  
     
    def __init__(self, parameter_file):
        conf = ConfigParser.ConfigParser()
        conf.read(parameter_file)
        self.discard_chimera = conf.get('MetaVelvet', 'discard_chimera') if conf.has_option('MetaVelvet', 'discard_chimera') else ''
        self.max_chimera_rate = conf.get('MetaVelvet', 'max_chimera_rate') if conf.has_option('MetaVelvet', 'max_chimera_rate') else ''
        self.repeat_cov_sd = conf.get('MetaVelvet', 'repeat_cov_sd') if conf.has_option('MetaVelvet', 'repeat_cov_sd') else ''
        self.min_split_length = conf.get('MetaVelvet', 'min_split_length') if conf.has_option('MetaVelvet', 'min_split_length') else ''
        self.valid_connections = conf.get('MetaVelvet', 'valid_connections') if conf.has_option('MetaVelvet', 'valid_connections') else ''
        self.noise_connections = conf.get('MetaVelvet', 'noise_connections') if conf.has_option('MetaVelvet', 'noise_connections') else ''
        self.use_connections = conf.getboolean('MetaVelvet', 'use_connections') if conf.has_option('MetaVelvet', 'use_connections') else ''
        self.report_split_detail = conf.getboolean('MetaVelvet', 'report_split_detail') if conf.has_option('MetaVelvet', 'report_split_detail') else ''
        self.report_subgraph = conf.getboolean('MetaVelvet', 'report_subgraph') if conf.has_option('MetaVelvet', 'report_subgraph') else ''
        self.exp_covs_meta = conf.get('MetaVelvet', 'exp_covs_meta') if conf.has_option('MetaVelvet', 'exp_covs_meta') else ''
        self.min_peak_cov = conf.get('MetaVelvet', 'min_peak_cov') if conf.has_option('MetaVelvet', 'min_peak_cov') else ''
        self.max_peak_cov = conf.get('MetaVelvet', 'max_peak_cov') if conf.has_option('MetaVelvet', 'max_peak_cov') else ''
        self.histo_bin_width = conf.get('MetaVelvet', 'histo_bin_width') if conf.has_option('MetaVelvet', 'histo_bin_width') else ''
        self.histo_sn_ratio = conf.get('MetaVelvet', 'histo_sn_ratio') if conf.has_option('MetaVelvet', 'histo_sn_ratio') else ''
        self.amos_file = conf.get('MetaVelvet', 'amos_file') if conf.has_option('MetaVelvet', 'amos_file') else ''
        self.coverage_mask = conf.get('MetaVelvet', 'coverage_mask') if conf.has_option('MetaVelvet', 'coverage_mask') else ''
        self.unused_reads_meta = conf.getboolean('MetaVelvet', 'unused_reads_meta') if conf.has_option('MetaVelvet', 'unused_reads_meta') else ''
        self.alignments_meta = conf.getboolean('MetaVelvet', 'alignments_meta') if conf.has_option('MetaVelvet', 'alignments_meta') else ''
        self.exportFiltered_meta = conf.getboolean('MetaVelvet', 'exportFiltered_meta') if conf.has_option('MetaVelvet', 'exportFiltered_meta') else ''
        self.paired_exp_fraction_meta = conf.get('MetaVelvet', 'paired_exp_fraction_meta') if conf.has_option('MetaVelvet', 'paired_exp_fraction_meta') else ''

# Parameter for metacv
class MetaCV_Parameter:

    seq = 'dna'
    mode = 'upgma'
    orf = 'optimal'
    total_reads = '100000'
    min_qual = '20'
    taxon = 'lca'
    name = 'metpipe'
    conf = ConfigParser.SafeConfigParser()
    
    def __init__(self, parameter_file):
        self.conf.read(parameter_file)
    
    def get_seq(self):
        return '--seq=' + self.conf.get('MetaCV', 'seq') if self.conf.has_option('MetaCV', 'seq') else ''
    
    def get_mode(self):
        return '--mode=' + self.conf.get('MetaCV', 'mode') if self.conf.has_option('MetaCV', 'mode') else ''
    
    def get_orf(self):
        return '--orf=' + self.conf.get('MetaCV', 'orf')  if self.conf.has_option('MetaCV', 'orf') else ''
    
    def get_total_reads(self):
        return '--total_reads=' + self.conf.get('MetaCV', 'total_reads') if self.conf.has_option('MetaCV', 'total_reads') else ''
        
    def get_min_qual(self):
        return '--min_qual=' + self.conf.get('MetaCV', 'min_qual') if self.conf.has_option('MetaCV', 'min_qual') else ''
    
    def get_taxon(self):
        return '--taxon=' + self.conf.get('MetaCV', 'taxon') if self.conf.has_option('MetaCV', 'taxon') else ''
    
    def get_name(self):
        return self.conf.get('MetaCV','name') if self.conf.has_option('MetaCV', 'name') else ''
        
# Parameter for blastn        
class Blastn_Parameter:

    import_search_strategy = ''
    dbsize = ''
    gilist = ''
    seqidlist = ''
    negative_gilist = ''
    entrez_query = ''
    db_soft_mask = ''
    db_hard_mask = ''
    evalue = ''
    word_size = ''
    gapopen = ''
    gapextend = ''
    perc_identity = 100.0
    xdrop_ungap = ''
    xdrop_gap = ''
    xdrop_gap_final = ''
    searchsp = ''
    max_hsps_per_subject = ''
    penalty = ''
    reward = ''
    no_greedy = False
    min_raw_gapped_score = ''
    dust = ''
    filtering_db = ''
    window_masker_taxid = ''
    window_masker_db = ''
    soft_masking = ''
    ungapped = False
    culling_limit = ''
    best_hit_overhang = ''
    best_hit_score_edge = ''
    window_size = ''
    off_diagonal_range = ''
    lcase_masking = False
    query_loc = ''
    strand = ''
    parse_deflines = False
    outfmt = 5
    show_gis = False
    num_descriptions = ''
    num_alignments = ''
    html = False
    max_target_seqs = ''
    arguments = {'import_search_strategy' : '-import_search_strategy ', 
                 'dbsize' : '-dbsize ','gilist' : '-gilist ', 
                 'seqidlist' : '-seqidlist ', 'negative_gilist' : '-negative_gilist ',
                 'entrez_query' : '-entrez_query ', 'db_soft_mask' : '-db_soft_mask ', 
                 'evalue' : '-evalue ', 'db_hard_mask' : '-db_hard_mask ',  
                 'word_size' : '-word_size ','gapopen' :  '-gapopen ', 
                 'gapextend' : '-gapextend ', 'perc_identity' : '-perc_identity ', 
                 'xdrop_gap' : '-xdrop_gap ', 'xdrop_ungap' : '-xdrop_ungap ',  
                 'xdrop_gap_final' : '-xdrop_gap_final ', 'penalty' : '-penalty ',
                 'searchsp' : '-searchsp ', 'max_hsps_per_subject' : '-max_hsps_per_subject ', 
                 'reward' : '-reward ', 'no_greedy' : '-no_greedy ',
                 'min_raw_gapped_score' : '-min_raw_gapped_score ', 'dust' : '-dust ', 
                 'filtering_db' : '-filtering_db ','window_masker_taxid' : '-window_masker_taxid ', 
                 'window_masker_db' :  '-window_masker_db ','soft_masking' : '-soft_masking ', 
                 'ungapped' : '-ungapped ', 'culling_limit' : '-culling_limit ',
                 'best_hit_overhang' : '-best_hit_overhang ', 'best_hit_score_edge' : '-best_hit_score_edge ',
                 'window_size' : '-window_size ', 'off_diagonal_range' : '-off_diagonal_range ',
                 'lcase_masking' : '-lcase_masking ', 'query_loc' : '-query_loc ', 
                 'strand' : '-strand ', 'parse_deflines' : '-parse_deflines ', 
                 'outfmt' : '-outfmt ', 'show_gis' : '-show_gis ', 
                 'num_descriptions' : '-num_descriptions ', 'num_alignments' : '-num_alignments ', 
                 'html' : '-html ', 'max_target_seqs' : '-max_target_seqs ' }

    def __init__(self, parameter_file):
        conf = ConfigParser.ConfigParser()
        conf.read(parameter_file)
        self.import_search_strategy = conf.get('blastn', 'import_search_strategy') if conf.has_option('blastn', 'import_search_strategy') else ''
        self.dbsize = conf.get('blastn', 'dbsize') if conf.has_option('MetaCV', 'dbsize') else ''
        self.gilist = conf.get('blastn', 'gilist') if conf.has_option('blastn', 'gilist') else ''
        self.seqidlist = conf.get('blastn', 'seqidlist') if conf.has_option('blastn', 'seqidlist') else ''
        self.negative_gilist = conf.get('blastn', 'negative_gilist') if conf.has_option('blastn', 'negative_gilist') else ''
        self.entrez_query = conf.get('blastn', 'entrez_query') if conf.has_option('blastn', 'entrez_query') else ''
        self.db_soft_mask = conf.get('blastn', 'db_soft_mask') if conf.has_option('blastn', 'db_soft_mask') else ''
        self.db_hard_mask = conf.get('blastn', 'db_hard_mask') if conf.has_option('blastn', 'db_hard_mask') else ''
        self.evalue = conf.get('blastn', 'evalue') if conf.has_option('blastn', 'evalue') else ''
        self.word_size = conf.get('blastn', 'word_size') if conf.has_option('blastn', 'word_size') else ''
        self.gapopen = conf.get('blastn', 'gapopen') if conf.has_option('blastn', 'gapopen') else ''
        self.gapextend = conf.get('blastn', 'gapextend') if conf.has_option('blastn', 'gapextend') else ''
        self.perc_identity = conf.get('blastn', 'perc_identity') if conf.has_option('blastn', 'perc_identity') else ''
        self.xdrop_ungap = conf.get('blastn', 'xdrop_ungap') if conf.has_option('blastn', 'xdrop_ungap') else ''
        self.xdrop_gap = conf.get('blastn', 'xdrop_gap') if conf.has_option('blastn', 'xdrop_gap') else ''
        self.xdrop_gap_final = conf.get('blastn', 'xdrop_gap_final') if conf.has_option('blastn', 'xdrop_gap_final') else ''
        self.searchsp = conf.get('blastn', 'searchsp') if conf.has_option('blastn', 'searchsp') else ''
        self.max_hsps_per_subject = conf.get('blastn', 'max_hsps_per_subject') if conf.has_option('blastn', 'max_hsps_per_subject') else ''
        self.penalty = conf.get('blastn', 'penalty') if conf.has_option('blastn', 'penalty') else ''
        self.reward = conf.get('blastn', 'reward') if conf.has_option('blastn', 'reward') else ''
        self.no_greedy = conf.getboolean('blastn', 'no_greedy')if conf.has_option('blastn', 'no_greedy') else ''
        self.min_raw_gapped_score = conf.get('blastn', 'min_raw_gapped_score') if conf.has_option('blastn', 'min_raw_gapped_score') else ''
        self.dust = conf.get('blastn', 'dust') if conf.has_option('blastn', 'dust') else ''
        self.filtering_db = conf.get('blastn', 'filtering_db') if conf.has_option('blastn', 'filtering_db') else ''
        self.window_masker_taxid = conf.get('blastn', 'window_masker_taxid') if conf.has_option('blastn', 'window_masker_taxid') else ''
        self.window_masker_db = conf.get('blastn', 'window_masker_db') if conf.has_option('blastn', 'window_masker_db') else ''
        self.soft_masking = conf.get('blastn', 'soft_masking') if conf.has_option('blastn', 'soft_masking') else ''
        self.ungapped = conf.getboolean('blastn', 'ungapped') if conf.has_option('blastn', 'ungapped') else ''
        self.culling_limit = conf.get('blastn', 'culling_limit') if conf.has_option('blastn', 'culling_limit') else ''
        self.best_hit_overhang = conf.get('blastn', 'best_hit_overhang') if conf.has_option('blastn', 'best_hit_overhang') else ''
        self.best_hit_score_edge = conf.get('blastn', 'best_hit_score_edge') if conf.has_option('blastn', 'best_hit_score_edge') else ''
        self.window_size = conf.get('blastn', 'window_size') if conf.has_option('blastn', 'window_size') else ''
        self.off_diagonal_range = conf.get('blastn', 'off_diagonal_range') if conf.has_option('blastn', 'off_diagonal_range') else ''
        self.lcase_maskingm = conf.getboolean('blastn', 'lcase_maskingm')  if conf.has_option('blastn', 'lcase_maskingm') else ''
        self.query_loc = conf.get('blastn', 'query_loc')  if conf.has_option('blastn', 'query_loc') else ''
        self.strand = conf.get('blastn', 'strand')  if conf.has_option('blastn', 'strand') else ''
        self.parse_deflines = conf.getboolean('blastn', 'parse_deflines')  if conf.has_option('blastn', 'parse_deflines') else ''
        self.outfmt = conf.get('blastn', 'outfmt')  if conf.has_option('blastn', 'outfmt') else ''
        self.show_gis = conf.getboolean('blastn', 'show_gis')  if conf.has_option('blastn', 'show_gis') else ''
        self.num_descriptions = conf.get('blastn', 'num_descriptions')  if conf.has_option('blastn', 'num_descriptions') else ''
        self.num_alignments = conf.get('blastn', 'num_alignments')  if conf.has_option('blastn', 'num_alignments') else ''
        self.html = conf.getboolean('blastn', 'html')  if conf.has_option('blastn', 'html') else ''
        self.max_target_seqs = conf.get('blastn', 'max_target_seqs')  if conf.has_option('blastn', 'max_target_seqs') else ''

class blastParser_Parameter:
    # Parser settings
    maxHit = 20
    maxHSP = 20
    reset_at = 1000
    arguments = {'maxHit' : '--max_hit ', 'maxHSP' : '--max_hsp ', 'reset_at' : '--reset_at '}
    conf = ConfigParser.ConfigParser()
    
    def __init__(self, parameter_file):
        self.conf.read(parameter_file)
        self.maxHit = self.conf.get('blastParser', 'max_hit') if self.conf.has_option('blastParser', 'max_hit') else ''
        self.maxHSP = self.conf.get('blastParser', 'max_hit') if self.conf.has_option('blastParser', 'max_hit') else ''
        self.reset_at = self.conf.get('blastParser', 'reset_at') if self.conf.has_option('blastParser', 'reset_at') else ''
    
    def get_name(self):
        return self.conf.get('blastParser', 'name') if self.conf.has_option('blastParser', 'name') else ''
    
class Rannotate_Parameter:
    # settings for annotation of the db with R
    coverage = 0.5
    bitscore = 0.98
    arguments = {'coverage' : ' --coverage ', 'bitscore' : '--bitscore '}
    conf = ConfigParser.SafeConfigParser()
    
    def __init__(self, parameter_file): 
        self.conf.read(parameter_file)
        self.coverage = self.conf.get('Taxonomical Annotation', 'coverage') if self.conf.has_option('Taxonomical Annotation', 'coverage') else ''
        self.bitscore = self.conf.get('Taxonomical Annotation', 'bitscore') if self.conf.has_option('Taxonomical Annotation', 'bitscore') else ''
        
    def get_name(self):
        return self.conf.get('Taxonomical Annotation', 'name') if self.conf.has_option('Taxonomical Annotation', 'name') else ''
    
    def get_taxon_db(self):
        return os.path.normpath(self.conf.get('Taxonomical Annotation', 'taxon_db') if self.conf.has_option('Taxonomical Annotation', 'taxon_db') else '')
        
class subsetDB_Parameter:
    classifier = ''
    bitscore = 0.98
    rank = ''
    conf = ConfigParser.SafeConfigParser()
    
    def __init__(self, parameter_file):
        self.conf.read(parameter_file)
        
    def get_bitscore(self):
        return self.conf.get('Subsetting of Database', 'bitscore') if self.conf.has_option('Subsetting of Database', 'bitscore') else ''
    
    def get_classifier(self):
       return [x.strip(' ') for x in (self.conf.get('Subsetting of Database', 'classifier') if self.conf.has_option('Subsetting of Database', 'classifier') else '').split(',')]
    
    def get_rank(self):
        return [x.strip(' ') for x in (self.conf.get('Subsetting of Database', 'rank') if self.conf.has_option('Subsetting of Database', 'rank') else '').split(',')]
    
    def get_taxon_db(self):
        return os.path.normpath(self.conf.get('Subsetting of Database', 'taxon_db') if self.conf.has_option('Subsetting of Database', 'taxon_db') else '')
    
class Krona_Parameter:
    
    highest_level = 'root'
    no_hits_wedge = ''
    best_hit_random = False
    use_perc_ident = False
    use_bitscore = False
    max_depth = ''
    allow_no_rank = False
    bad_scores = 0
    good_scores = 120
    local = False
    krona_res = ''
    query_url = ''
    e_value = ''
    conf = ConfigParser.ConfigParser()
    arguments = {'highest_level' : '-n ', 'no_hits_wedge': ' -i ', 'best_hit_random' : '-r',
                 'use_perc_ident' : '-p', 'use_bitscore' : '-b', 'max_depth' : '-d ',
                 'allow_no_rank' : '-k', 'bad_scores' : '-x ', 'good_scores' : '-y ',
                 'local' : '-l', 'krona_res' : '-u ', 'query_url' : '-qp ', 'e_value' : '-e '}
    
    def __init__(self, parameter_file):
        self.conf.read(parameter_file)
        self.highest_level = self.conf.get('Krona Tools', 'highest_level') if self.conf.has_option('Krona Tools', 'highest_level') else ''
        self.no_hits_wedge = self.conf.get('Krona Tools', 'no_hits_wedge') if self.conf.has_option('Krona Tools', 'no_hits_wedge') else ''
        self.best_hit_random = self.conf.getboolean('Krona Tools', 'best_hit_random') if self.conf.has_option('Krona Tools', 'best_hit_random') else ''
        self.use_perc_ident = self.conf.getboolean('Krona Tools', 'use_perc_ident') if self.conf.has_option('Krona Tools', 'use_perc_ident') else ''
        self.use_bitscore = self.conf.getboolean('Krona Tools', 'use_bitscore') if self.conf.has_option('Krona Tools', 'use_bitscore') else ''
        self.max_depth = self.conf.get('Krona Tools', 'max_depth') if self.conf.has_option('Krona Tools', 'max_depth') else ''
        self.allow_no_rank = self.conf.getboolean('Krona Tools', 'allow_no_rank') if self.conf.has_option('Krona Tools', 'allow_no_rank') else ''
        self.bad_scores = self.conf.get('Krona Tools', 'bad_scores') if self.conf.has_option('Krona Tools', 'bad_scores') else ''
        self.good_scores = self.conf.get('Krona Tools', 'good_scores') if self.conf.has_option('Krona Tools', 'good_scores') else ''
        self.local = self.conf.getboolean('Krona Tools', 'local') if self.conf.has_option('Krona Tools', 'local') else ''
        self.krona_res = self.conf.get('Krona Tools', 'krona_res') if self.conf.has_option('Krona Tools', 'krona_res') else ''
        self.query_url = self.conf.get('Krona Tools', 'query_url') if self.conf.has_option('Krona Tools', 'query_url') else ''
        self.e_value = self.conf.get('Krona Tools', 'e_value') if self.conf.has_option('Krona Tools', 'e_value') else ''
        
    def get_name(self):
        return self.conf.get('Krona Tools', 'filename') if self.conf.has_option('Krona Tools', 'filename') else ''
        
        
    
