import ConfigParser
import sys
import os
from src.utils import *
from twisted.python.rebuild import __getattr__
import types

class Settings:
    
    # general settings
    kmer = 85
    threads = 8
    verbose = False
    skip = ""
    # File settings
    input = ""
    output = ""
    param = ""
    # EXECUTABLES 
    program_dir = ""
    FASTQC = ""
    TRIMGALORE = ""
    VELVETH = ""
    VELVETG = ""
    METAVELVET = ""
    CONCAT = ""
    BLASTN = ""
    METACV = ""
    # Program Settings
    filter = ""
    quality = ""
    assembler = ""
    classify = ""
    
    def __init__(self, kmer=None, threads=None, program_dir=None, verbose=False, skip=None, input=None, output=None,
                param=None, filter=None, quality=None, assembler=None, classify=None):
        
        conf = ConfigParser.ConfigParser()
        conf.read(param)
        Settings.kmer = kmer
        Settings.threads = threads
        Settings.verbose = verbose
        Settings.skip = skip.lower()
        Settings.input = input
        Settings.output = output
        Settings.param = param
        Settings.filter = filter
        Settings.quality = quality 
        Settings.assembler = assembler.lower()
        Settings.classify = classify.lower()
        
        
        # Annotate Options
        
        
        # define program paths
        Settings.FASTQC = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'quality')
        Settings.TRIMGALORE = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'filter')
        Settings.VELVETH = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'velveth')
        Settings.VELVETG = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'velvetg')
        Settings.CONCAT = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'concat')
        Settings.METAVELVET = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'metavelvetg')
        Settings.BLASTN = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'blastn')
        Settings.METACV = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'metacv')
        
class FastQC_Parameter:
    
    nogroup = False
    contaminants = "" 
    kmers = ""
    arguments = {"nogroup" : "--nogroup ", "contaminants": "-c ", "kmers": "-k "}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.nogroup = str2bool(conf.get('FastQC', 'nogroup'))
        self.kmers = conf.get('FastQC', 'kmers')
        self.contaminants = conf.get('FastQC', 'contaminants')
    
class TrimGalore_Parameter:
    
    quality = 20 
    phred = ""
    adapter = ""
    adapter2 = ""
    stringency = ""
    error_rate = 0.1
    length = 150
    paired = False
    retain_unpaired = False
    length_1 = ""
    length_2 = ""
    trim = False
    arguments = {"quality":"-q ", "phred":"--phred", "adapter":"-a ", "adapter2":"-a2 ", "stringency":"-s ",
                 "error_rate":"-e ", "length":"--length ", "paired":"--paired", "retain_unpaired":"--retain_unpaired",
                 "length1":"-r1 ", "length2":"-r2 ", "trim":"-t "}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.quality = conf.get('TrimGalore', 'quality')
        self.phred = conf.get('TrimGalore', 'phred')
        self.adapter = conf.get('TrimGalore', 'adapter')
        self.adapter2 = conf.get('TrimGalore', 'adapter2')
        self.stringency = conf.get('TrimGalore', 'stringency')
        self.error_rate = conf.get('TrimGalore', 'error_rate')
        self.length = conf.get('TrimGalore', 'length')
        self.paired = conf.getboolean('TrimGalore', 'paired')
        self.retain_unpaired = conf.get('TrimGalore', 'retain_unpaired')
        self.length_1 = conf.get('TrimGalore', 'length_1')
        self.length_2 = conf.get('TrimGalore', 'length_2')
        self.trim = conf.get('TrimGalore', 'trim1')
    
class Concat_Parameter:
     
    pretty_out = False
    score = 20
    arguments = {"pretty_out" : "-p", "score" : "-s "}
       
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.pretty_out = conf.get('concat', 'pretty_output')
        self.score = conf.get('concat', 'score')

class Velveth_Parameter:
    
    file_layout = ""
    read_type = ""
    strand_specific = False
    reuse_Sequences = False
    noHash = False
    create_binary = False
    arguments = {"file_layout" : "-", "read_type" : "-", "strand_specific":"-strand_specific",
				"reuse_Sequences":"-reuse_Sequences", "noHash":"-noHash", "create_binary":"-createBinary"}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.file_layout = conf.get('MetaVelvet', 'file_layout')
        self.read_type = conf.get('MetaVelvet', 'read_type')
        self.strand_specific = conf.get('MetaVelvet', 'strand_specific')
        self.reuse_Sequences = conf.get('MetaVelvet', 'reuse_Sequences')
        self.noHash = conf.get('MetaVelvet', 'noHash')
        self.create_binary = conf.get('MetaVelvet', 'create_binary')

class Velvetg_Parameter:
    
    cov_cutoff = ""
    ins_length = ""
    read_trkg = False
    min_contig_lgth = 250
    exp_cov = "auto"
    long_cov_cutoff = ""
    ins_length_long = ""
    ins_length_sd = ""
    scaffolding = True
    max_branch_length = 100
    max_divergence = 0.2
    max_gap_count = 3
    min_pair_count = 5
    max_coverage = False
    coverage_mask = ""
    long_mult_cutoff = 2
    unused_reads = False
    alignments = False
    exportFiltered = False 
    clean = False 
    very_clean = False
    paired_exp_fraction = 0.1
    shortMatePaired = False
    conserveLong = False  
    arguments = {"cov_cutoff" : "-cov_cutoff ", "ins_length" : "-ins_length ",
                     "read_trkg" : "-read_trkg ", "min_contig_lgth" : "-min_contig_lgth ",
                     "exp_cov" : "-exp_cov ", "long_cov" : "-long_cov ", "long_cov_cutoff":"-long_cov_cutoff ",
                     "ins_length_long" : "-ins_length_long ", "ins_length_sd" : "-ins_length_sd ",
                     "scaffolding":"-scaffolding ", "max_branch_length":"-max_branch_length ",
                     "max_divergence" : "-max_divergence ", "max_gap_count" : "-max_gap_count ",
                     "min_pair_count" : "-min_pair_count ", "max_coverage" : "-max_coverage ",
                     "coverage_mask" : "-coverage_mask ", "long_mult_cutoff" : "-long_mult_cutoff ",
                     "unused_reads" : "-unused_reads ", "alignments" : "-alignments ",
                     "exportFiltered" : "-exportFiltered ", "clean" : "-clean ", "very_clean" : "-very_clean ",
                     "paired_exp_fraction" : "-paired_exp_fraction ", "shortMatePaired" : "-shortMatePaired ",
                     "conserveLong" : "-conserveLong "}  
    
    def __init__(self):
        
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.cov_cutoff = conf.get('MetaVelvet', 'cov_cutoff')
        self.ins_length = conf.get('MetaVelvet', 'ins_length')
        self.read_trkg = conf.get('MetaVelvet', 'read_trkg')
        self.min_contig_lgth = conf.get('MetaVelvet', 'min_contig_lgth')
        self.exp_cov = conf.get('MetaVelvet', 'exp_cov')
        self.long_cov_cutoff = conf.get('MetaVelvet', 'long_cov_cutoff')
        self.ins_length_long = conf.get('MetaVelvet', 'ins_length_long')
        self.ins_length_sd = conf.get('MetaVelvet', 'ins_length_sd')
        self.scaffolding = conf.get('MetaVelvet', 'scaffolding')
        self.max_branch_length = conf.get('MetaVelvet', 'max_branch_length')
        self.max_divergence = conf.get('MetaVelvet', 'max_divergence')
        self.max_gap_count = conf.get('MetaVelvet', 'max_gap_count')
        self.min_pair_count = conf.get('MetaVelvet', 'min_pair_count')
        self.max_coverage = conf.get('MetaVelvet', 'max_coverage')
        self.coverage_mask = conf.get('MetaVelvet', 'coverage_mask')
        self.long_mult_cutoff = conf.get('MetaVelvet', 'long_mult_cutoff')
        self.unused_reads = conf.get('MetaVelvet', 'unused_reads')
        self.alignments = conf.get('MetaVelvet', 'alignments')
        self.exportFiltered = conf.get('MetaVelvet', 'exportFiltered')
        self.clean = conf.get('MetaVelvet', 'clean')
        self.very_clean = conf.get('MetaVelvet', 'very_clean')
        self.paired_exp_fraction = conf.get('MetaVelvet', 'paired_exp_fraction')
        self.shortMatePaired = conf.get('MetaVelvet', 'shortMatePaired')
        self.conserveLong = conf.get('MetaVelvet', 'conserveLong') 
        
       
    
       
class MetaVelvet_Parameter:
    
    discard_chimera = False
    max_chimera_rate = 0.0 
    repeat_cov_sd = 0.1 
    min_split_length = 0
    valid_connections = 1 
    noise_connections = 0 
    use_connections = True 
    report_split_detail = False
    report_subgraph = False 
    exp_covs_meta = "auto"  
    min_peak_cov = 0 
    max_peak_cov = 500        
    histo_bin_width = 1  
    histo_sn_ratio = 10
    amos_file = False
    coverage_mask = 1
    unused_reads_meta = False 
    alignments_meta = False
    exportFiltered_meta = False
    paired_exp_fraction_meta = ""   
    arguments = {"discard_chimera":"-discard_chimera ", "max_chimera_rate":"-max_chimera_rate ",
				"repeat_cov_sd":"-repeat_cov_sd ", "min_split_length":"-min_split_length ",
				"valid_connections":"-valid_connections ", "noise_connections":"-noise_connections ",
				"use_connections":"-use_connections ", "report_split_detail":"-report_split_detail ",
				"report_subgraph":"-report_subgraph " , "exp_covs_meta":"-exp_covs ",
				"min_peak_cov":"-min_peak_cov ", "max_peak_cov":"-max_peak_cov ",
				"histo_bin_width":"-histo_bin_width ", "histo_sn_ratio":"-histo_sn_ratio ", "amos_file":"-amos_file",
				"coverage_mask":"-coverage_mask ", "unused_reads_meta":"-unused_reads ",
				"alignments_meta":"-alignments", "exportFiltered_meta":"-exportFiltered ",
				"paired_exp_fraction_meta": "-paired_exp_fraction "}  
     
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)   
        self.discard_chimera = conf.get('MetaVelvet', 'discard_chimera')
        self.max_chimera_rate = conf.get('MetaVelvet', 'max_chimera_rate')
        self.repeat_cov_sd = conf.get('MetaVelvet', 'repeat_cov_sd')
        self.min_split_length = conf.get('MetaVelvet', 'min_split_length')
        self.valid_connections = conf.get('MetaVelvet', 'valid_connections')
        self.noise_connections = conf.get('MetaVelvet', 'noise_connections')
        self.use_connections = conf.get('MetaVelvet', 'use_connections')
        self.report_split_detail = conf.get('MetaVelvet', 'report_split_detail')
        self.report_subgraph = conf.get('MetaVelvet', 'report_subgraph')
        self.exp_covs_meta = conf.get('MetaVelvet', 'exp_covs_meta')
        self.min_peak_cov = conf.get('MetaVelvet', 'min_peak_cov')
        self.max_peak_cov = conf.get('MetaVelvet', 'max_peak_cov')
        self.histo_bin_width = conf.get('MetaVelvet', 'histo_bin_width')
        self.histo_sn_ratio = conf.get('MetaVelvet', 'histo_sn_ratio')
        self.amos_file = conf.get('MetaVelvet', 'amos_file')
        self.coverage_mask = conf.get('MetaVelvet', 'coverage_mask')
        self.unused_reads_meta = conf.get('MetaVelvet', 'unused_reads_meta')
        self.alignments_meta = conf.get('MetaVelvet', 'alignments_meta')
        self.exportFiltered_meta = conf.get('MetaVelvet', 'exportFiltered_meta')
        self.paired_exp_fraction_meta = conf.get('MetaVelvet', 'paired_exp_fraction_meta')   

class MetaCV_Parameter:
	seq = ""
	mode = ""
	orf = ""
	arguments = {"seq":"--seq ", "mode":"--mode ", "orf":"--orf "}
	
	def __init__(self):
		conf = ConfigParser.ConfigParser()
		conf.read(Settings.param)   
		self.seq = conf.get('MetaCV', 'seq')
		self.mode = conf.get('MetaCV', 'mode')
		self.orf = conf.get('MetaCV', 'orf')        
            
            
class Blastn_Parameter:
	
	import_search_strategy = ""
	task_name = "metpipe-blastn "
	db = ""
	dbsize = ""
	gilist = ""
	seqidlist = ""
	negative_gilist = ""
	entrez_query = ""
	db_soft_mask = ""
	db_hard_mask = ""
	subject = ""
	subject_loc = ""
	evalue = ""
	word_size = ""
	gapopen = ""
	gapextend = ""
	perc_identity = 100.0
	xdrop_ungap = ""
	xdrop_gap = ""
	xdrop_gap_final = ""
	searchsp = ""
	max_hsps_per_subject = ""
	penalty = ""
	reward = ""
	no_greedy = False
	min_raw_gapped_score = ""
	template_type = ""
	template_length = ""
	dust = ""
	filtering_db = ""
	window_masker_taxid = ""
	window_masker_db = ""
	soft_masking = ""
	ungapped = False
	culling_limit = ""
	best_hit_overhang = ""
	best_hit_score_edge = ""
	window_size = ""
	off_diagonal_range = ""
	use_index = False
	index_name = ""
	lcase_maskingm = False
	query_loc = ""
	strand = ""
	parse_deflines = False
	outfmt = 5
	show_gis = False
	num_descriptions = ""
	num_alignments = ""
	html = False
	max_target_seqs = ""
	arguments = {}
	
	def __init__(self):
		conf = ConfigParser.ConfigParser()
		conf.read(Settings.param)
		self.import_search_strategy = conf.get('blastn', 'import_search_strategy')
		self.task_name = conf.get('blastn', 'task_name')
		self.db = conf.get('blastn', 'db')
		self.dbsize = conf.get('blastn', 'dbsize')
		self.gilist = conf.get('blastn', 'gilist')
		self.seqidlist = conf.get('blastn', 'seqidlist')
		self.negative_gilist = conf.get('blastn', 'negative_gilist')
		self.entrez_query = conf.get('blastn', 'entrez_query')
		self.db_soft_mask = conf.get('blastn', 'db_soft_mask')
		self.db_hard_mask = conf.get('blastn', 'db_hard_mask')
		self.subject = conf.get('blastn', 'subject')
		self.subject_loc = conf.get('blastn', 'subject_loc')
		self.evalue = conf.get('blastn', 'evalue')
		self.word_size = conf.get('blastn', 'word_size')
		self.gapopen = conf.get('blastn', 'gapopen')
		self.gapextend = conf.get('blastn', 'gapextend')
		self.perc_identity = conf.get('blastn', 'perc_identity')
		self.xdrop_ungap = conf.get('blastn', 'xdrop_ungap')
		self.xdrop_gap = conf.get('blastn', 'xdrop_gap')
		self.xdrop_gap_final = conf.get('blastn', 'xdrop_gap_final')
		self.searchsp = conf.get('blastn', 'searchsp')
		self.max_hsps_per_subject = conf.get('blastn', 'max_hsps_per_subject')
		self.penalty = conf.get('blastn', 'penalty')
		self.reward = conf.get('blastn', 'reward')
		self.no_greedy = conf.get('blastn', 'no_greedy')
		self.min_raw_gapped_score = conf.get('blastn', 'min_raw_gapped_score')
		self.template_type = conf.get('blastn', 'template_type')
		self.template_length = conf.get('blastn', 'template_length')
		self.dust = conf.get('blastn', 'dust')
		self.filtering_db = conf.get('blastn', 'filtering_db')
		self.window_masker_taxid = conf.get('blastn', 'window_masker_taxid')
		self.window_masker_db = conf.get('blastn', 'window_masker_db')
		self.soft_masking = conf.get('blastn', 'soft_masking')
		self.ungapped = conf.get('blastn', 'ungapped')
		self.culling_limit = conf.get('blastn', 'culling_limit')
		self.best_hit_overhang = conf.get('blastn', 'best_hit_overhang')
		self.best_hit_score_edge = conf.get('blastn', 'best_hit_score_edge')
		self.window_size = conf.get('blastn', 'window_size')
		self.off_diagonal_range = conf.get('blastn', 'off_diagonal_range')
		self.use_index = conf.get('blastn', 'use_index')
		self.index_name = conf.get('blastn', 'index_name')
		self.lcase_maskingm = conf.get('blastn', 'lcase_maskingm')
		self.query_loc = conf.get('blastn', 'query_loc')
		self.strand = conf.get('blastn', 'strand')
		self.parse_deflines = conf.get('blastn', 'parse_deflines')
		self.outfmt = conf.get('blastn', 'outfmt')
		self.show_gis = conf.get('blastn', 'show_gis')
		self.num_descriptions = conf.get('blastn', 'num_descriptions')
		self.num_alignments = conf.get('blastn', 'num_alignments')
		self.html = conf.get('blastn', 'html')
		self.max_target_seqs = conf.get('blastn', 'max_target_seqs')
            
            
            
            
            
            
            
            
            
            
            
            
            
            
