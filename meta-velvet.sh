#!/bin/bash

# this script execute all 3 meta-velvet steps and do an optional blast search at the end
while getopts hi:j:w:k:b:d:f:o:p:c: opt
	do
		case $opt in
			i)  if [ -e $OPTARG ]; then 
					input1=$OPTARG
				else 
					echo "Inputfile 1 not found"
					exit 1
				fi;;
			j) if [ -e $OPTARG ]; then 
					input2=$OPTARG
				else 
					echo "Inputfile 2 not found"
					exit 1
				fi;;
			w)  workingdir=$OPTARG;;
			k)  kmer=$OPTARG;;
			b)  blast=$OPTARG;;
			d)  db=$OPTARG;;
			f)  format=$OPTARG;;
			o)  output=$OPTARG;;
			p)  identity=$OPTARG;;
			c)  cores=$OPTARG;;
			h) echo "
This script execute all 3 meta-velvet steps and do an optional blast search at the end

USAGE: $0 [-h|-i|-j|-w|-k|-b|-db|-f|-o|-p|-c] <fastq>

	-i forward fastq       <fastq file>
	-j reverse fastq       <fastq file>
	-w working dir         <dir>
	-k k-mer size          <int>
	-b blastsearch         <yes|no>
	-d blast db            <name or location of db>
	-f blast outformat     <blast out format>
	-o blast outputfile    <blast outputfile>
	-p blast perc_identity <min identity of blast>
	-c cores for blast     <int>"
exit 0;
		esac
	done
if [ ! -d $workingdir ]; then
	mkdir $workingdir
fi

#velveth $workingdir $kmer -fastq -shortPaired $input1 $input2

velvetg "$workingdir" -exp_cov auto -ins_length 450

meta-velvetg $workingdir 

if [ "$blast" = "yes" ] ;then
	blastn -db $db -query $workingdir/meta-velvetg.contigs.fa -perc_identity $identity -outfmt $format -out $output -num_threads $cores
fi
exit 0;

