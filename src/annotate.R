#!/usr/bin/env Rscript
suppressPackageStartupMessages(library('optparse'))

# specify the commandline interface
option_list <- list(
  make_option(c("-i", "--input"), type = "character",
              help = "Blast or Taxonomy SQL Database"),
  make_option(c("-o", "--output"), type = "character",
              help = "output dir and name for the new Database"),
  make_option(c("-c", "--coverage"), type = "numeric", default = 0.50,
              help = "query coverage for hit filtering [default= %default]"),
  make_option(c("-b", "--bitscore"), type = "numeric", default = 0.98,
              help = "bitscore tolerance for hsp filtering [default= %default]"),
  make_option("--taxon", type = "character",
              help = "path to NCBI taxonomy db"))

# init the commandline interface
opt <- parse_args(OptionParser(option_list=option_list))

# load requiered packages for analysis
suppressPackageStartupMessages(library('metaR'))
suppressPackageStartupMessages(library('rmisc'))

# load the input values
blastReport <- blastReportDBConnect(opt$input)
taxon_db <- connectTaxonDB(opt$taxon)

# annotate the data
sprintf('Annotating Data ...')
annotate <- assignTaxon(query_id = 1:10000,
                        taxRanks = c("species", "genus", "tribe", "family", "order",
                                     "class", "phylum", "kingdom", "superkingdom"),
                        coverage_threshold = opt$coverage,
                        bitscore_tolerance = opt$bitscore,
                        blast_db = blastReport,
                        taxon_db = taxon_db)
# create the new database
sprintf('Creating new Database ...')
createTaxonomyReportDB(opt$output,
                       blastReport,
                       annotate,
                       opt$bitscore)

