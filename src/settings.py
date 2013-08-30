import ConfigParser
import sys
import os

# class for general settings of the pipeline and variables needed from every program

class Settings:

    # general settings
    kmer = 85
    threads = 8
    verbose = False
    skip = ''
    starting_time = ''
    actual_time = ''
    automatic = False
    step_number = 1
    # File settings
    input = []
    contigs = []
    blast_input = []
    output = ''
    logdir = ''
    logfile=''
    param = ''
    quality_report = []
    metaCV_output = []
    blast_output = ''
    # Program Settings
    trim = True
    quality = True
    use_contigs = False
    assembler = ''
    classify = 'both'
    summary = True
    metacv_db = ''
    blastdb_16S = ''
    blastdb_nt = ''
    
    
    def __init__(self, kmer=None, threads=None, program_dir=None, verbose=False, skip=None, starting_time=None, 
                 infile=None, output=None, logdir=None, param=None, trim=None, quality=None, 
                 use_contigs=None,assembler=None, classify=None, summary=None,automatic=None, step_number= None):

        Settings.kmer = kmer
        Settings.threads = threads
        Settings.verbose = verbose
        Settings.skip = skip.lower()
        Settings.starting_time = starting_time
        Settings.actual_time = starting_time
        Settings.input = infile
        Settings.contigs = []
        Settings.blast_input = []
        Settings.output = output
        Settings.logdir = logdir
        Settings.logfile = open(logdir+"summary.log","w")
        Settings.param = param
        Settings.trim = trim
        Settings.quality = quality 
        Settings.use_contigs = use_contigs
        Settings.assembler = assembler.lower()
        Settings.classify = classify.lower() 
        Settings.summary = summary
        Settings.automatic = automatic
        Settings.step_number = step_number
        # define program paths
        
        # define databases
        Settings.blastdb_nt = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep , 'db', os.sep, 'nt')
        Settings.blastdb_16S = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep , 'db', os.sep, '16S')
        Settings.metacv_db = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep , 'db', os.sep, 'cvk6_2059')

class Executables:

    def __init__(self):
        Executables.FASTQC = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'fastqc', os.sep, 'fastqc')
        Executables.TRIMGALORE = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'trim_galore', os.sep, 'trim_galore')
        Executables.VELVETH = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'velvet', os.sep ,'velveth')
        Executables.VELVETG = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'velvet', os.sep,'velvetg')
        Executables.METAVELVET = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'metavelvet', os.sep, 'meta-velvetg')
        Executables.FLASH = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'flash', os.sep, 'flash')
        Executables.BLASTN = '%s%s%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'blast', os.sep, 'bin', os.sep, 'blastn')
        Executables.METACV = '%s%s%s%s%s' % (sys.path[0], os.sep, 'program', os.sep, 'bacterial')
        Executables.CONVERTER = '%s%s%s%s%s%s%s' % (sys.path[0], os.sep, 'programs', os.sep, 'fastx', os.sep, 'fastq_to_fasta')
        Executables.PARSER = '%s%s%s%s%s' % (sys.path[0], os.sep, 'program', os.sep, 'xmlparser')
        Executables.KRONA_BLAST = '%s%s%s%s%s' % (sys.path[0], os.sep, 'program', os.sep, 'krona' + 
                                               os.sep + 'bin' + os.sep + 'ktImportBLAST')
        Executables.KRONA_TEXT = '%s%s%s%s%s' % (sys.path[0], os.sep, 'program', os.sep, 'krona' + 
                                               os.sep + 'bin' + os.sep + 'ktImportText')
        

# Parameters for FastQC 
class FastQC_Parameter:

    nogroup = False
    contaminants = '' 
    kmers = ''
    # dict with the arguments string
    arguments = {'nogroup' : '--nogroup ', 'contaminants': '-c ', 'kmers': '-k '}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.nogroup = conf.getboolean('FastQC', 'nogroup')
        self.kmers = conf.get('FastQC', 'kmers')
        self.contaminants = conf.get('FastQC', 'contaminants')

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
        self.retain_unpaired = conf.getboolean('TrimGalore', 'retain_unpaired')
        self.length_1 = conf.get('TrimGalore', 'length_1')
        self.length_2 = conf.get('TrimGalore', 'length_2')
        self.trim = conf.getboolean('TrimGalore', 'trim1')

class FLASH_Parameter:
    minOverlap = 10
    maxOverlap = ""
    maxMismatchDensity = ""
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
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.minOverlap = conf.get('FLASH','min-overlap')
        self.maxOverlap = conf.get('FLASH','max-overlap')
        self.maxMismatchDensity = conf.get('FLASH', 'max-mismatch-density')
        self.phred = conf.get('FLASH','phred-offset')
        self.readLength = conf.get('FLASH','read-len')
        self.fragmentLength = conf.get('FLASH','fragment-len')
        self.fragmentLengthStddev = conf.get('FLASH','fragment-len-stddev')
        self.interleavedInput = conf.getboolean('FLASH', 'interleaved-input')
        self.interleavedOutput = conf.getboolean('FLASH', 'interleaved-output')
        
# Parameter for velveth
class Velveth_Parameter:

    file_layout = ''
    read_type = ''
    strand_specific = False
    reuse_Sequences = False
    noHash = False
    create_binary = False
    # dict with the arguments string
    arguments = {'file_layout' : '-', 'read_type' : '-', 'strand_specific':'-strand_specific',
				'reuse_Sequences':'-reuse_Sequences', 'noHash':'-noHash', 'create_binary':'-createBinary'}
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.file_layout = conf.get('MetaVelvet', 'file_layout')
        self.read_type = conf.get('MetaVelvet', 'read_type')
        self.strand_specific = conf.getboolean('MetaVelvet', 'strand_specific')
        self.reuse_Sequences = conf.getboolean('MetaVelvet', 'reuse_Sequences')
        self.noHash = conf.getboolean('MetaVelvet', 'noHash')
        self.create_binary = conf.getboolean('MetaVelvet', 'create_binary')

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
                     'exportFiltered' : '-exportFiltered ','paired_exp_fraction' : '-paired_exp_fraction ', 
                     'shortMatePaired' : '-shortMatePaired ','conserveLong' : '-conserveLong '}  
    
    def __init__(self):
        
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.cov_cutoff = conf.get('MetaVelvet', 'cov_cutoff')
        self.ins_length = conf.get('MetaVelvet', 'ins_length')
        self.read_trkg = conf.getboolean('MetaVelvet', 'read_trkg')
        self.min_contig_lgth = conf.get('MetaVelvet', 'min_contig_lgth')
        self.exp_cov = conf.get('MetaVelvet', 'exp_cov')
        self.long_cov_cutoff = conf.get('MetaVelvet', 'long_cov_cutoff')
        self.ins_length_long = conf.get('MetaVelvet', 'ins_length_long')
        self.ins_length_sd = conf.get('MetaVelvet', 'ins_length_sd')
        self.scaffolding = conf.getboolean('MetaVelvet', 'scaffolding')
        self.max_branch_length = conf.get('MetaVelvet', 'max_branch_length')
        self.max_divergence = conf.get('MetaVelvet', 'max_divergence')
        self.max_gap_count = conf.get('MetaVelvet', 'max_gap_count')
        self.min_pair_count = conf.get('MetaVelvet', 'min_pair_count')
        self.max_coverage = conf.get('MetaVelvet', 'max_coverage')
        self.coverage_mask = conf.get('MetaVelvet', 'coverage_mask')
        self.long_mult_cutoff = conf.get('MetaVelvet', 'long_mult_cutoff')
        self.unused_reads = conf.getboolean('MetaVelvet', 'unused_reads')
        self.alignments = conf.getboolean('MetaVelvet', 'alignments')
        self.exportFiltered = conf.getboolean('MetaVelvet', 'exportFiltered')
        self.paired_exp_fraction = conf.get('MetaVelvet', 'paired_exp_fraction')
        self.shortMatePaired = conf.getboolean('MetaVelvet', 'shortMatePaired')
        self.conserveLong = conf.getboolean('MetaVelvet', 'conserveLong') 
        
# Parameter for meta-velvetg 
class MetaVelvet_Parameter:

    discard_chimera = False
    max_chimera_rate = '' 
    repeat_cov_sd ='' 
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
     
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)   
        self.discard_chimera = conf.get('MetaVelvet', 'discard_chimera')
        self.max_chimera_rate = conf.get('MetaVelvet', 'max_chimera_rate')
        self.repeat_cov_sd = conf.get('MetaVelvet', 'repeat_cov_sd')
        self.min_split_length = conf.get('MetaVelvet', 'min_split_length')
        self.valid_connections = conf.get('MetaVelvet', 'valid_connections')
        self.noise_connections = conf.get('MetaVelvet', 'noise_connections')
        self.use_connections = conf.getboolean('MetaVelvet', 'use_connections')
        self.report_split_detail = conf.getboolean('MetaVelvet', 'report_split_detail')
        self.report_subgraph = conf.getboolean('MetaVelvet', 'report_subgraph')
        self.exp_covs_meta = conf.get('MetaVelvet', 'exp_covs_meta')
        self.min_peak_cov = conf.get('MetaVelvet', 'min_peak_cov')
        self.max_peak_cov = conf.get('MetaVelvet', 'max_peak_cov')
        self.histo_bin_width = conf.get('MetaVelvet', 'histo_bin_width')
        self.histo_sn_ratio = conf.get('MetaVelvet', 'histo_sn_ratio')
        self.amos_file = conf.get('MetaVelvet', 'amos_file')
        self.coverage_mask = conf.get('MetaVelvet', 'coverage_mask')
        self.unused_reads_meta = conf.getboolean('MetaVelvet', 'unused_reads_meta')
        self.alignments_meta = conf.getboolean('MetaVelvet', 'alignments_meta')
        self.exportFiltered_meta = conf.getboolean('MetaVelvet', 'exportFiltered_meta')
        self.paired_exp_fraction_meta = conf.get('MetaVelvet', 'paired_exp_fraction_meta')   

# Parameter for metacv
class MetaCV_Parameter:

    seq = ''
    mode = ''
    orf = ''
    # dict with the arguments string
    arguments = {'seq':'--seq=', 'mode':'--mode=', 'orf':'--orf='}

    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)   
        self.seq = conf.get('MetaCV', 'seq')
        self.mode = conf.get('MetaCV', 'mode')
        self.orf = conf.get('MetaCV', 'orf')        
            
# Parameter for blastn        
class Blastn_Parameter:

    import_search_strategy = ''
    db = ''
    dbsize = ''
    gilist = ''
    seqidlist = ''
    negative_gilist = ''
    entrez_query = ''
    db_soft_mask = ''
    db_hard_mask = ''
    subject = ''
    subject_loc = ''
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
    template_type = ''
    template_length = ''
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
    use_index = False
    index_name = ''
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
    arguments = {'import_search_strategy' : '-import_search_strategy ', 'db' : '-db ',
                 'dbsize' : '-dbsize ', 'gilist' : '-gilist ', 'seqidlist' : '-seqidlist ',
                  'negative_gilist' : '-negative_gilist ', 'entrez_query' : '-entrez_query ',
                  'db_soft_mask' : '-db_soft_mask ', 'db_hard_mask' : '-db_hard_mask ', 'subject' : '-subject ',
                  'subject_loc' : '-subject_loc ', 'evalue' : '-evalue ', 'word_size' : '-word_size ',
                  'gapopen' :  '-gapopen ', 'gapextend' : '-gapextend ', 'perc_identity' : '-perc_identity ',
                  'xdrop_ungap' : '-xdrop_ungap ', 'xdrop_gap' : '-xdrop_gap ', 'xdrop_gap_final' : '-xdrop_gap_final ',
                  'searchsp' : '-searchsp ', 'max_hsps_per_subject' : '-max_hsps_per_subject ',
                  'penalty' : '-penalty ', 'reward' : '-reward ', 'no_greedy' : '-no_greedy ',
                  'min_raw_gapped_score' : '-min_raw_gapped_score ', 'template_type' : '-template_type ',
                  'template_length' : '-template_length ', 'dust' : '-dust ', 'filtering_db' : '-filtering_db ',
                  'window_masker_taxid' : '-window_masker_taxid ', 'window_masker_db' :  '-window_masker_db ',
                  'soft_masking' : '-soft_masking ', 'ungapped' : '-ungapped ', 'culling_limit' : '-culling_limit ',
                  'best_hit_overhang' : '-best_hit_overhang ', 'best_hit_score_edge' : '-best_hit_score_edge ',
                  'window_size' : '-window_size ', 'off_diagonal_range' : '-off_diagonal_range ',
                  'use_index' : '-use_index ', 'index_name' : '-index_name ', 'lcase_masking' : '-lcase_masking ',
                  'query_loc' : '-query_loc ', 'strand' : '-strand ', 'parse_deflines' : '-parse_deflines ',
                  'outfmt' : '-outfmt ', 'show_gis' : '-show_gis ', 'num_descriptions' : '-num_descriptions ',
                  'num_alignments' : '-num_alignments ', 'html' : '-html ', 'max_target_seqs' : '-max_target_seqs ' }

    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.import_search_strategy = conf.get('blastn', 'import_search_strategy')
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
        self.no_greedy = conf.getboolean('blastn', 'no_greedy')
        self.min_raw_gapped_score = conf.get('blastn', 'min_raw_gapped_score')
        self.template_type = conf.get('blastn', 'template_type')
        self.template_length = conf.get('blastn', 'template_length')
        self.dust = conf.get('blastn', 'dust')
        self.filtering_db = conf.get('blastn', 'filtering_db')
        self.window_masker_taxid = conf.get('blastn', 'window_masker_taxid')
        self.window_masker_db = conf.get('blastn', 'window_masker_db')
        self.soft_masking = conf.get('blastn', 'soft_masking')
        self.ungapped = conf.getboolean('blastn', 'ungapped')
        self.culling_limit = conf.get('blastn', 'culling_limit')
        self.best_hit_overhang = conf.get('blastn', 'best_hit_overhang')
        self.best_hit_score_edge = conf.get('blastn', 'best_hit_score_edge')
        self.window_size = conf.get('blastn', 'window_size')
        self.off_diagonal_range = conf.get('blastn', 'off_diagonal_range')
        self.use_index = conf.getboolean('blastn', 'use_index')
        self.index_name = conf.get('blastn', 'index_name')
        self.lcase_maskingm = conf.getboolean('blastn', 'lcase_maskingm')
        self.query_loc = conf.get('blastn', 'query_loc')
        self.strand = conf.get('blastn', 'strand')
        self.parse_deflines = conf.getboolean('blastn', 'parse_deflines')
        self.outfmt = conf.get('blastn', 'outfmt')
        self.show_gis = conf.getboolean('blastn', 'show_gis')
        self.num_descriptions = conf.get('blastn', 'num_descriptions')
        self.num_alignments = conf.get('blastn', 'num_alignments')
        self.html = conf.getboolean('blastn', 'html')
        self.max_target_seqs = conf.get('blastn', 'max_target_seqs')

class xmlParser():
    # Parser settings
    parser_maxHit = 20
    parser_maxHSP = 20
    parser_reset_at = 1000
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(Settings.param)
        self.parser_maxHit = conf.get('xmlParser', 'max_hit')
        self.parser_maxHsp = conf.get('xmlParser', 'max_hsp')
        self.parser_reset_at = conf.get('xmlParser', 'reset_at')

class Krona_Parameter():
    pass