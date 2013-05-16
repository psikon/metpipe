args <- commandArgs(trailingOnly=T)
#args <- "SPICEIII/miseq/scripts/metpipe/result/RAW/forward_fastqc/fastqc_data.txt"
lines <- readLines(args)
encoding <- lines[grep("Encoding",lines)]
idx <- c(grep(">>Per base sequence quality",lines)+1,grep(">>END_MODULE",lines)[2]-1)
quality <- read.table(textConnection(lines[idx[1]:idx[2]]),sep="\t",header=F)

c(tail(quality$V2,n=1),encoding)
