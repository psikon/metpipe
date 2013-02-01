#!/bin/sh

while getopts h opt
	do
		case $opt in
			\?) echo "Invalid option :-$OPTARG"; exit 0;;
			h) echo "
This is the install script of the pipeline. All relevant programms will be checked and installed if not existing.

Requierments: boost, OpenMPI, sparsehash (abyss)
              python 2.6+ (stitch)
			  perl (blast database download)ls 
              
USAGE: $0 [-h]

 -h show help screen 
"
exit 0;
		esac
	done

echo "Installation of the metPipe Programms.\n"

# create needed directories
if ! [ -d program ]; then
	mkdir program/
fi 

if ! [ -d download ]; then
	mkdir download/
fi 
# Installation of stitch for concatinate the reads
while true
	do
	if [ -f program/stitch/stitch.py ]; then
		echo "Installation of stitch found"
		break
	fi
	echo -n "stitch not found. Needed for concatination (optional)\n Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
		mkdir program/stitch
		cd program/stitch/
		wget https://github.com/audy/stitch/blob/master/stitch/stitch.py
		wget https://github.com/audy/stitch/blob/master/stitch/__init__.py
		wget https://github.com/audy/stitch/blob/master/stitch/fasta.py
		wget https://github.com/audy/stitch/blob/master/stitch/length_filter.py
		cd ../
		break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done

# Installation of blastn for annotation of the reads
while true
	do
	if [ -f program/blast/bin/blastn ]; then
		echo "Installation of blastn found"
		break
	fi
	echo -n "blastn not found. Needed for annotation. Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
		cd program/
		wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-2.2.27+-x64-linux.tar.gz
		tar xzfv ncbi-blast*
		rm ncbi-blast-2.2.27+-x64-linux.tar.gz
		mv ncbi-blast-2.2.27+ blast
		cd ..
		break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done

# Checking and install the databases of blast
while true
	do
	if [ -f program/db/nt.nal ]; then
		echo "nt Database found for blast"
		break
	fi
	echo -n "nt database not found. Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
		mkdir program/db/
		cd program/db
		perl ../blast/bin/update_blastdb.pl nt --decompress --passive
		break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done

while true
	do
	if [ -f program/db/16SMIcrobial.nal ]; then
		echo "16SMircobial Database found for blast"
		break
	fi
	echo -n "nt database not found. Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
		mkdir program/db/
		cd program/db
		perl ../blast/bin/update_blastdb.pl nt --decompress --passive
		break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done
ls 


while true
	do
	if [ -f program/meta-velvetg ]; then
		echo "Installation of MetaVelvet found"
		break
	fi
	echo -n "MetaVelvet not found. Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
		wget http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.08.tgz
		tar xzfv velvet_
		rm velvet_
		mv velvet_1.2.08 velvet
		cd velvet/
		./configure 
		mkdir program/metavelvet


		break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done

exit 0;

exit 0;
echo "create all required dirs"

mkdir blast/
mkdir blast/db/
mkdir download/


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

