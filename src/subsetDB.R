#!/usr/bin/env Rscript
suppressPackageStartupMessages(library('optparse'))

# specify the commandline interface
option_list <- list(
  make_option(c("-i", "--input"), type = "character",
              help = "Blast or Taxonomy SQL Database"),
  make_option(c("-o", "--output"), type = "character",
              help = "output dir and name for the new Database"),
  make_option(c("-c", "--classifier"), type = "character",
              help = "classifier for subsetting, e.g 'bacteria'"),
  make_option(c("-b", "--bitscore"), type = "numeric", default = 0.98,
              help = "bitscore tolerance for hsp filtering [default= %default]"),
  make_option(c("-r", "--rank"), type = "character", default = "superkingdom",
              help = "taxonomical rank for subsetting [default= %default]"),
  make_option("--blast",type = "character",
              help = "parsed Blast Database"),
  make_option("--taxon", type = "character",
              help = "path to NCBI taxonomy db"))

# init the commandline interface
opt <- parse_args(OptionParser(option_list=option_list))

# load requiered packages for analysis
suppressPackageStartupMessages(library('metaR'))
suppressPackageStartupMessages(library('rmisc'))

# load the input values
input <- taxonomyReportDBConnect(opt$input)
blastReport <- blastReportDBConnect(opt$blast)
taxon_db <- connectTaxonDB(opt$taxon)


sprintf("Subset %s from %d taxonomies ...",opt$classifier,db_count(input,'taxonomy'))
classified <- selectByRank(x = input,
                           taxRank = opt$rank,
                           classifier = opt$classifier,
                           taxon_db = taxon_db)

sprintf("create new database ...")
createTaxonomyReportDB(opt$output,
                       blastReport,
                       classified,
                       opt$bitscore)
