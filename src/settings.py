import ConfigParser
import sys
import os
from src.utils import *

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
    
    metavelvet_discard_chimera = False
    metavelvet_max_chimera_rate = 0.0 
    metavelvet_repeat_cov_sd = 0.1 
    metavelvet_min_split_length = 0
    metavelvet_valid_connections = 1 
    metavelvet_noise_connections = 0 
    metavelvet_use_connections = True 
    metavelvet_report_split_detail = False
    metavelvet_report_subgraph = False 
    metavelvet_exp_covs_meta = "auto"  
    metavelvet_min_peak_cov = 0 
    metavelvet_max_peak_cov = 500        
    metavelvet_histo_bin_width = 1  
    metavelvet_histo_sn_ratio = 10
    metavelvet_amos_file = False
    metavelvet_coverage_mask = 1
    metavelvet_unused_reads_meta = False 
    metavelvet_alignments_meta = False
    metavelvet_exportFiltered_meta = False
    metavelvet_paired_exp_fraction_meta = 0.1
    # Annotate Options
    metacv_seq = ""
    metacv_mode = ""
    metacv_orf = ""
    metacv_prefix = ""
    blastn_import_search_strategy = ""
    blastn_task_name = "metpipe-blastn "
    blastn_db = ""
    blastn_dbsize = ""
    blastn_gilist = ""
    blastn_seqidlist = ""
    blastn_negative_gilist = ""
    blastn_entrez_query = ""
    blastn_db_soft_mask = ""
    blastn_db_hard_mask = ""
    blastn_subject = ""
    blastn_subject_loc = ""
    blastn_evalue = ""
    blastn_word_size = ""
    blastn_gapopen = ""
    blastn_gapextend = ""
    blastn_perc_identity = 90.0
    blastn_xdrop_ungap = ""
    blastn_xdrop_gap = ""
    blastn_xdrop_gap_final = ""
    blastn_searchsp = ""
    blastn_max_hsps_per_subject = ""
    blastn_penalty = ""
    blastn_reward = ""
    blastn_no_greedy = False
    blastn_min_raw_gapped_score = ""
    blastn_template_type = ""
    blastn_template_length = ""
    blastn_dust = ""
    blastn_filtering_db = ""
    blastn_window_masker_taxid = ""
    blastn_window_masker_db = ""
    blastn_soft_masking = ""
    blastn_ungapped = False
    blastn_culling_limit = ""
    blastn_best_hit_overhang = ""
    blastn_best_hit_score_edge = ""
    blastn_window_size = ""
    blastn_off_diagonal_range = ""
    blastn_use_index = False
    blastn_index_name = ""
    blastn_lcase_maskingm = False
    blastn_query_loc = ""
    blastn_strand = ""
    blastn_parse_deflines = False
    blastn_outfmt = 5
    blastn_show_gis = False
    blastn_num_descriptions = ""
    blastn_num_alignments = ""
    blastn_html = False
    blastn_max_target_seqs = ""

    

    def __init__(self, kmer=None, threads=None, program_dir=None, verbose=False, skip=None, input=None, output=None,
                param=None, filter=None, quality=None, assembler=None, classify=None):
        
        conf = ConfigParser.ConfigParser()
        conf.read(param)
        Settings.kmer = kmer
        Settings.threads = threads
        Settings.verbose = verbose
        Settings.skip = skip
        Settings.input = input
        Settings.output = output
        Settings.param = param
        Settings.filter = filter
        Settings.quality = quality 
        Settings.assembler = assembler
        Settings.classify = classify
        
        Settings.metavelvet_discard_chimera = conf.get('MetaVelvet', 'discard_chimera')
        Settings.metavelvet_max_chimera_rate = conf.get('MetaVelvet', 'max_chimera_rate')
        Settings.metavelvet_repeat_cov_sd = conf.get('MetaVelvet', 'repeat_cov_sd')
        Settings.metavelvet_min_split_length = conf.get('MetaVelvet', 'min_split_length')
        Settings.metavelvet_valid_connections = conf.get('MetaVelvet', 'valid_connections')
        Settings.metavelvet_noise_connections = conf.get('MetaVelvet', 'noise_connections')
        Settings.metavelvet_use_connections = conf.get('MetaVelvet', 'use_connections')
        Settings.metavelvet_report_split_detail = conf.get('MetaVelvet', 'report_split_detail')
        Settings.metavelvet_report_subgraph = conf.get('MetaVelvet', 'report_subgraph')
        Settings.metavelvet_exp_covs_meta = conf.get('MetaVelvet', 'exp_covs_meta')
        Settings.metavelvet_min_peak_cov = conf.get('MetaVelvet', 'min_peak_cov')
        Settings.metavelvet_max_peak_cov = conf.get('MetaVelvet', 'max_peak_cov')
        Settings.metavelvet_histo_bin_width = conf.get('MetaVelvet', 'histo_bin_width')
        Settings.metavelvet_histo_sn_ratio = conf.get('MetaVelvet', 'histo_sn_ratio')
        Settings.metavelvet_amos_file = conf.get('MetaVelvet', 'amos_file')
        Settings.metavelvet_coverage_mask = conf.get('MetaVelvet', 'coverage_mask')
        Settings.metavelvet_unused_reads_meta = conf.get('MetaVelvet', 'unused_reads_meta')
        Settings.metavelvet_alignments_meta = conf.get('MetaVelvet', 'alignments_meta')
        Settings.metavelvet_exportFiltered_meta = conf.get('MetaVelvet', 'exportFiltered_meta')
        Settings.metavelvet_paired_exp_fraction_meta = conf.get('MetaVelvet', 'paired_exp_fraction_meta')
        # Annotate Options
        Settings.metacv_prefix = conf.get('MetaCV', 'prefix')
        Settings.metacv_seq = conf.get('MetaCV', 'seq')
        Settings.metacv_mode = conf.get('MetaCV', 'mode')
        Settings.metacv_orf = conf.get('MetaCV', 'orf')
        Settings.blastn_import_search_strategy = conf.get('blastn', 'import_search_strategy')
        Settings.blastn_task_name = conf.get('blastn', 'task_name')
        Settings.blastn_db = conf.get('blastn', 'db')
        Settings.blastn_dbsize = conf.get('blastn', 'dbsize')
        Settings.blastn_gilist = conf.get('blastn', 'gilist')
        Settings.blastn_seqidlist = conf.get('blastn', 'seqidlist')
        Settings.blastn_negative_gilist = conf.get('blastn', 'negative_gilist')
        Settings.blastn_entrez_query = conf.get('blastn', 'entrez_query')
        Settings.blastn_db_soft_mask = conf.get('blastn', 'db_soft_mask')
        Settings.blastn_db_hard_mask = conf.get('blastn', 'db_hard_mask')
        Settings.blastn_subject = conf.get('blastn', 'subject')
        Settings.blastn_subject_loc = conf.get('blastn', 'subject_loc')
        Settings.blastn_evalue = conf.get('blastn', 'evalue')
        Settings.blastn_word_size = conf.get('blastn', 'word_size')
        Settings.blastn_gapopen = conf.get('blastn', 'gapopen')
        Settings.blastn_gapextend = conf.get('blastn', 'gapextend')
        Settings.blastn_perc_identity = conf.get('blastn', 'perc_identity')
        Settings.blastn_xdrop_ungap = conf.get('blastn', 'xdrop_ungap')
        Settings.blastn_xdrop_gap = conf.get('blastn', 'xdrop_gap')
        Settings.blastn_xdrop_gap_final = conf.get('blastn', 'xdrop_gap_final')
        Settings.blastn_searchsp = conf.get('blastn', 'searchsp')
        Settings.blastn_max_hsps_per_subject = conf.get('blastn', 'max_hsps_per_subject')
        Settings.blastn_penalty = conf.get('blastn', 'penalty')
        Settings.blastn_reward = conf.get('blastn', 'reward')
        Settings.blastn_no_greedy = conf.get('blastn', 'no_greedy')
        Settings.blastn_min_raw_gapped_score = conf.get('blastn', 'min_raw_gapped_score')
        Settings.blastn_template_type = conf.get('blastn', 'template_type')
        Settings.blastn_template_length = conf.get('blastn', 'template_length')
        Settings.blastn_dust = conf.get('blastn', 'dust')
        Settings.blastn_filtering_db = conf.get('blastn', 'filtering_db')
        Settings.blastn_window_masker_taxid = conf.get('blastn', 'window_masker_taxid')
        Settings.blastn_window_masker_db = conf.get('blastn', 'window_masker_db')
        Settings.blastn_soft_masking = conf.get('blastn', 'soft_masking')
        Settings.blastn_ungapped = conf.get('blastn', 'ungapped')
        Settings.blastn_culling_limit = conf.get('blastn', 'culling_limit')
        Settings.blastn_best_hit_overhang = conf.get('blastn', 'best_hit_overhang')
        Settings.blastn_best_hit_score_edge = conf.get('blastn', 'best_hit_score_edge')
        Settings.blastn_window_size = conf.get('blastn', 'window_size')
        Settings.blastn_off_diagonal_range = conf.get('blastn', 'off_diagonal_range')
        Settings.blastn_use_index = conf.get('blastn', 'use_index')
        Settings.blastn_index_name = conf.get('blastn', 'index_name')
        Settings.blastn_lcase_maskingm = conf.get('blastn', 'lcase_maskingm')
        Settings.blastn_query_loc = conf.get('blastn', 'query_loc')
        Settings.blastn_strand = conf.get('blastn', 'strand')
        Settings.blastn_parse_deflines = conf.get('blastn', 'parse_deflines')
        Settings.blastn_outfmt = conf.get('blastn', 'outfmt')
        Settings.blastn_show_gis = conf.get('blastn', 'show_gis')
        Settings.blastn_num_descriptions = conf.get('blastn', 'num_descriptions')
        Settings.blastn_num_alignments = conf.get('blastn', 'num_alignments')
        Settings.blastn_html = conf.get('blastn', 'html')
        Settings.blastn_max_target_seqs = conf.get('blastn', 'max_target_seqs')
        # define program paths
        Settings.FASTQC = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'quality')
        Settings.TRIMGALORE = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'filter')
        Settings.VELVETH = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'velveth')
        Settings.VELVETG = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'velvetg')
        Settings.CONCAT = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'concat')
        Settings.METAVELVET = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'meta-velvetg')
        Settings.BLASTN = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'blastn')
        Settings.METACV = "%s%s%s%s%s" % (sys.path[0], os.sep, 'program', os.sep, 'metacv')
        
class FastQC_Parameter:
    
    fastqc_nogroup = False
    fastqc_contaminants = "" 
    fastqc_kmers = ""
    arguments = {"nogroup" : "--nogroup ", "contaminants": "-c ", "kmers": "-k "}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        utils = Utils()
        self.fastqc_nogroup = str2bool(conf.get('FastQC', 'nogroup'))
        self.fastqc_kmers = conf.get('FastQC', 'kmers')
        self.fastqc_contaminants = conf.get('FastQC', 'contaminants')
        
    def checkUsedArguments(self):
        args = ""
        if self.fastqc_nogroup:
            args += self.arguments.get("nogroup")
        if self.fastqc_contaminants:
            args += ' ' + self.arguments.get("contaminants") + self.fastqc_contaminants
        if self.fastqc_kmers:
            args += ' ' + self.arguments.get("kmers") + self.fastqc_kmers
            
        return args
    
class TrimGalore_Parameter:
    
    trim_quality = 20 
    trim_phred = ""
    trim_adapter = ""
    trim_adapter2 = ""
    trim_stringency = ""
    trim_error_rate = 0.1
    trim_length = 150
    trim_paired = False
    trim_retain_unpaired = False
    trim_length_1 = ""
    trim_length_2 = ""
    trim_trim1 = False
    arguments = {"quality":"-q ", "phred":"--phred", "adapter":"-a ", "adapter2":"-a2 ", "stringency":"-s ",
                 "error_rate":"-e ", "length":"--length ", "paired":"--paired", "unpaired":"--retain_unpaired",
                 "length1":"-r1 ", "length2":"-r2 ", "trim1":"-t "}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.trim_quality = conf.get('TrimGalore', 'quality')
        self.trim_phred = conf.get('TrimGalore', 'phred')
        self.trim_adapter = conf.get('TrimGalore', 'adapter')
        self.trim_adapter2 = conf.get('TrimGalore', 'adapter2')
        self.trim_stringency = conf.get('TrimGalore', 'stringency')
        self.trim_error_rate = conf.get('TrimGalore', 'error_rate')
        self.trim_length = conf.get('TrimGalore', 'length')
        self.trim_paired = conf.getboolean('TrimGalore', 'paired')
        self.trim_retain_unpaired = conf.get('TrimGalore', 'retain_unpaired')
        self.trim_length_1 = conf.get('TrimGalore', 'length_1')
        self.trim_length_2 = conf.get('TrimGalore', 'length_2')
        self.trim_trim1 = conf.get('TrimGalore', 'trim1')
        
    def checkUsedArguments(self):
        args = ""
        if self.trim_quality:
            args += self.arguments.get("quality") + self.trim_quality
        if self.trim_phred:
            args += " " + self.arguments.get("phred") + self.trim_phred
        if self.trim_adapter:
            args += " " + self.arguments.get("adapter") + self.trim_adapter
        if self.trim_adapter2:
            args += " " +  self.arguments.get("adapter2") + self.trim_adapter2
        if self.trim_stringency:
            args+= " " +  self.arguments.get("stringency") + self.trim_stringency
        if self.trim_error_rate:
            args += " " + self.arguments.get("error_rate") + self.trim_error_rate
        if self.trim_length:
            args += " " +self.arguments.get("length") + self.trim_length
        if self.trim_paired:
            args += " " + self.arguments.get("paired")
            if self.trim_retain_unpaired:
                args += " " + self.arguments.get("unpaired")
            if self.trim_length_1:
                args += " " + self.arguments.get("length1") + self.trim_length_1
            if self.trim_length_2:
                args += " " + self.arguments.get("length2") + self.trim_length_2
            if self.trim_trim1:
                args += " " + self.arguments.get("trim1")  
        else: 
            args += ""   
        return args   
    
class Concat_Parameter:
     
    concat_pretty_out = False
    concat_score = 20
    arguments = {"pretty_out" : "-p", "score" : "-s "}
       
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.concat_pretty_out = conf.get('concat', 'pretty_output')
        self.concat_score = conf.get('concat', 'score')
        
    
    def checkUsedArguments(self):
        args = ""
        if self.concat_pretty_out:
            args += self.arguments.get("pretty_out")
        if self.concat_score:
            args += " " + self.arguments.get("score") + self.concat_score
        return args

class Velveth_Parameter:
    
    velveth_file_layout = ""
    velveth_read_type = ""
    velveth_strand_specific = False
    velveth_reuse_Sequences = False
    velveth_noHash = False
    velveth_create_binary = False
    arguments = {"strand":"-strand_specific","reuse":"-reuse_Sequences","noHash":"-noHash","binary":"-createBinary"}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.velveth_file_layout = conf.get('MetaVelvet', 'file_layout')
        self.velveth_read_type = conf.get('MetaVelvet', 'read_type')
        self.velveth_strand_specific = conf.get('MetaVelvet', 'strand_specific')
        self.velveth_reuse_Sequences = conf.get('MetaVelvet', 'reuse_Sequences')
        self.velveth_noHash = conf.get('MetaVelvet', 'noHash')
        self.velveth_create_binary = conf.get('MetaVelvet', 'create_binary')
        
    def checkUsedArguments(self):
        args = "-%s -%s"%(self.velveth_read_type,self.velveth_file_layout) 
        if self.velveth_strand_specific:
            args += ' ' + self.arguments.get("strand")
        if self.velveth_reuse_Sequences:
            args += ' ' + self.arguments.get("reuse")
        if self.velveth_noHash:
            args += ' ' + self.arguments.get("noHash")
        if self.velveth_create_binary:
            args+= ' ' + self.arguments.get("binary")
        return args

class Velvetg_Parameter:
    
    velvetg_cov_cutoff = ""
    velvetg_ins_length = ""
    velvetg_read_trkg = False
    velvetg_min_contig_lgth = 250
    velvetg_exp_cov = "auto"
    velvetg_long_cov_cutoff = ""
    velvetg_ins_length_long = ""
    velvetg_ins_length_sd = ""
    velvetg_scaffolding = True
    velvetg_max_branch_length = 100
    velvetg_max_divergence = 0.2
    velvetg_max_gap_count = 3
    velvetg_min_pair_count = 5
    velvetg_max_coverage = False
    velvetg_coverage_mask = 1
    velvetg_long_mult_cutoff = 2
    velvetg_unused_reads = False
    velvetg_alignments = False
    velvetg_exportFiltered = False 
    velvetg_clean = False 
    velvetg_very_clean = False
    velvetg_paired_exp_fraction = 0.1
    velvetg_shortMatePaired = False
    velvetg_conserveLong = False  
    arguments = {"cov_cutoff" : "-cov_cutoff ", "ins_length" : "-ins_length ",
                     "read_trkg" : "-read_trkg ", "min_contig_lgth" : "-min_contig_lgth ",
                     "exp_cov" : "-exp_cov ", "long_cov" : "-long_cov ", "long_cov_cutoff":"-long_cov_cutoff ",
                     "ins_length_long" : "-ins_length_long ", "ins_length_sd" : "-ins_length_sd ",
                     "scaffolding":"-scaffolding ","max_branch_length":"-max_branch_length ",
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
        self.velvetg_cov_cutoff = conf.get('MetaVelvet', 'cov_cutoff')
        self.velvetg_ins_length = conf.get('MetaVelvet', 'ins_length')
        self.velvetg_read_trkg = conf.get('MetaVelvet', 'read_trkg')
        self.velvetg_min_contig_lgth = conf.get('MetaVelvet', 'min_contig_lgth')
        self.velvetg_exp_cov = conf.get('MetaVelvet', 'exp_cov')
        self.velvetg_long_cov_cutoff = conf.get('MetaVelvet', 'long_cov_cutoff')
        self.velvetg_ins_length_long = conf.get('MetaVelvet', 'ins_length_long')
        self.velvetg_ins_length_sd = conf.get('MetaVelvet', 'ins_length_sd')
        self.velvetg_scaffolding = conf.get('MetaVelvet', 'scaffolding')
        self.velvetg_max_branch_length = conf.get('MetaVelvet', 'max_branch_length')
        self.velvetg_max_divergence = conf.get('MetaVelvet', 'max_divergence')
        self.velvetg_max_gap_count = conf.get('MetaVelvet', 'max_gap_count')
        self.velvetg_min_pair_count = conf.get('MetaVelvet', 'min_pair_count')
        self.velvetg_max_coverage = conf.get('MetaVelvet', 'max_coverage')
        self.velvetg_coverage_mask = conf.get('MetaVelvet', 'coverage_mask')
        self.velvetg_long_mult_cutoff = conf.get('MetaVelvet', 'long_mult_cutoff')
        self.velvetg_unused_reads = conf.get('MetaVelvet', 'unused_reads')
        self.velvetg_alignments = conf.get('MetaVelvet', 'alignments')
        self.velvetg_exportFiltered = conf.get('MetaVelvet', 'exportFiltered')
        self.velvetg_clean = conf.get('MetaVelvet', 'clean')
        self.velvetg_very_clean = conf.get('MetaVelvet', 'very_clean')
        self.velvetg_paired_exp_fraction = conf.get('MetaVelvet', 'paired_exp_fraction')
        self.velvetg_shortMatePaired = conf.get('MetaVelvet', 'shortMatePaired')
        self.velvetg_conserveLong = conf.get('MetaVelvet', 'conserveLong') 
        
       
    def checkUsedArguments(self):
        args= self.arguments.get("exp_cov") + self.velvetg_exp_cov
        if self.velvetg_cov_cutoff:
            args += ' ' + self.arguments.get("cov_cutoff") + self.velvetg_cov_cutoff
        if self.velvetg_ins_length:
            args += ' ' + self.arguments.get("ins_length") + self.velvetg_ins_length
        if self.velvetg_read_trkg:
            args += ' ' + self.arguments.get("read_trkg") + bool2Str(self.velvetg_read_trkg)
        if self.velvetg_min_contig_lgth:
            args += ' ' + self.arguments.get("min_contig_lgth") + self.velvetg_min_contig_lgth
        if self.velvetg_long_cov_cutoff:
            args += ' ' + self.arguments.get("long_cov_cutoff") + self.velvetg_long_cov_cutoff
        if self.velvetg_ins_length_long:
            args += ' ' + self.arguments.get("ins_length_long") + self.velvetg_ins_length_long
        if self.velvetg_ins_length_sd:
            args += ' ' + self.arguments.get("ins_length_sd") + self.velvetg_ins_length_sd
        if self.velvetg_scaffolding:
            args += ' ' + self.arguments.get("scaffolding") + bool2Str(self.velvetg_scaffolding)
        if self.velvetg_max_branch_length:
            args += ' ' + self.arguments.get("max_branch_length") + self.velvetg_max_branch_length
        if self.velvetg_max_divergence:
            args += ' ' + self.arguments.get("max_divergence") + self.velvetg_max_divergence
        if self.velvetg_max_gap_count:
            args += ' ' + self.arguments.get("max_gap_count") + self.velvetg_max_gap_count
        if self.velvetg_min_pair_count:
            args += ' ' + self.arguments.get("min_pair_count") + self.velvetg_min_pair_count
        if self.velvetg_max_coverage:
            args += ' ' + self.arguments.get("max_coverage") + bool2Str(self.velvetg_max_coverage)
        if self.velvetg_coverage_mask:
            args += ' ' + self.arguments.get("coverage_mask") + self.velvetg_coverage_mask
        if self.velvetg_long_mult_cutoff:
            args += ' ' + self.arguments.get("long_mult_cutoff") + self.velvetg_long_mult_cutoff
        if self.velvetg_unused_reads:
            args += ' ' + self.arguments.get("unused_reads") + bool2Str(self.velvetg_unused_reads)
        if self.velvetg_alignments:
            args += ' ' + self.arguments.get("alignments") + bool2Str(self.velvetg_alignments)
        if self.velvetg_exportFiltered:
            args += ' ' + self.arguments.get("exportFiltered") + bool2Str(self.velvetg_exportFiltered)
        if self.velvetg_clean:
            args += ' ' + self.arguments.get("clean") + bool2Str(self.velvetg_clean)
        if self.velvetg_very_clean:
            args += ' ' + self.arguments.get("very_clean") + bool2Str(self.velvetg_very_clean)
        if self.velvetg_paired_exp_fraction:
            args += ' ' + self.arguments.get("paired_exp_fraction") + self.velvetg_paired_exp_fraction
        if self.velvetg_shortMatePaired:
            args += ' ' + self.arguments.get("shortMatePaired") + bool2Str(self.velvetg_shortMatePaired)
        if self.velvetg_conserveLong:
            args += ' ' + self.arguments.get("conserveLong") + bool2Str(self.velvetg_conserveLong)
        return args
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            