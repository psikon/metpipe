#!/bin/sh

#starting options
while getopts hi:j:o:s:b:c: opt
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
			o)  output=$OPTARG;;
			s)  stepsize=$OPTARG;;
			c)  cores=$OPTARG;;
			h) echo "USAGE: $0 [-h|-i|-j|-o|-s|-c] <fastq>
	-i forward fastq 
	-j reverse fastq
	-o outputfile
	-s stepsize
	-c cores"
		esac
	done
# init

if [ ! -d "tmp/" ]; then
	mkdir tmp
fi

if [ ! -d "results/" ]; then
	mkdir results
fi

# 4 lanes for 1 read in fastq file
step=$(($stepsize*4))
i=1
until [ $i = 5 ]
do  
    #create datasets
    head -n $step $input1 > tmp/$step.1.fastq
    head -n $step $input2 > tmp/$step.2.fastq
    python stitch/stitch.py -i tmp/$step.1.fastq -j tmp/$step.2.fastq -o tmp/$step -t $cores
    fastq_to_fasta -n -Q33 -i tmp/$step-contigs.fastq -o tmp/$step.c.fasta
    blastn -db nt -perc_identity 90 -num_threads $cores -query tmp/$step.c.fasta -outfmt 6 -out results/$step.table
    #cleaning tmp
    rm tmp/$step.* tmp/$step-*
    step=$(($step+($stepsize*4)))
    i=$(($i+1))
echo $i
done

    
