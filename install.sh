#!/bin/bash

while getopts h opt
	do
		case $opt in
			\?) echo "Invalid option :-$OPTARG"; exit 0;;
			h) echo "
This is the install script of the pipeline. All relevant programms will be checked and installed if not existing.

Requierments: boost, OpenMPI, sparsehash (abyss)
              python 2.6+ (stitch)
              
USAGE: $0 [-h]

 -h show help screen 
"
exit 0;
		esac
	done

exit 0;

echo "create all required dirs"

mkdir blast/
mkdir blast/db/
mkdir download/
mkdir program/
mkdir program/stitch
mkdir program/meta-velvet
mkdir program/velvet

echo "install programs"
cd download/
#download and install blast
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.2.$
tar -xzf ncbi-blast* -C ~/blast/
rm ncbi-blast-2.2.27+-x64-linux.tar.gz
cd ~/blast/
# clean install dir
mv ncbi-blast*/* ~/blast/
rm -r ncbi-blast*

# download and install stitch
cd ~/program/stitch/
wget https://github.com/audy/stitch/blob/master/stitch/stitch.py
wget https://github.com/audy/stitch/blob/master/stitch/__init__.py
wget https://github.com/audy/stitch/blob/master/stitch/fasta.py
wget https://github.com/audy/stitch/blob/master/stitch/length_filter.py

echo "downlaod Blast Database"

cd ~/blast/db/
perl ../bin/update_blastdb.pl --decompress --passive nt
perl ../bin/update_blastdb.pl --decompress --passive 16SMicrobial

echo "COMPLETE"

