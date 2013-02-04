#!/bin/bash

while getopts hsc opt
	do
		case $opt in
			\?) echo "Invalid option :-$OPTARG"; exit 0;;
			s) echo "Components of metpipe:
[Read Quality Check and Trimming]
- FastQC
- Trim Galore!
[Assembler]
- MetaVelvet
- Abyss
- Velvet
- concatination of the reads
[Annotate]
- Blastn (nt|16SMicrobial)
- MetaCV
[Classifier]
- MetaCV
"
exit 0;;
			h) echo "
This is the install script of the pipeline. All relevant programms will be checked and installed if not existing.

Requirments: boost
             python 2.6+ (stitch)
			 perl (blast database download)ls 
              
USAGE: $0 [-h]

 -h show help screen 
 -q silent install install all required components
 -s show all included programms
"
exit 0;
		esac
	done

echo "Installation of the metPipe Programms.\n"

# create needed directories
if ! [ -d program ]; then
	mkdir program/
fi 



# Installation of FastQC for quality checks
while true
	do
		# checking for install
		if [ -f program/fastqc/fastqc ]; then
			echo "Installation of FastQC found"
			break
		fi
	echo -n "FastQC not found. Needed for quality checks.\nDownload and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download and uncompress FastQC
				wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.10.1.zip
				unzip fastqc*
				rm fastqc_v0.10.1.zip
				mv FastQC* fastqc
			cd ..
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
		# checking for install
		if [ -f program/fast ]; then
			echo "Installation of Trim Galore! found"
			break
		fi
	echo -n "Trim Galore! not found. Needed for quality trimming.\nDownload and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download Trim Galore! 
				mkdir trim_galore
				cd trim_galore
					wget http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/trim_galore_v0.2.5.zip
					unzip trim_galore*
					rm trim_galore_v0.2.5.zip
			cd ../..
			break;;
		n|N|no|NO|No)
			break;
		;;
		*) echo Please enter only y or n
		esac
	done
ls
# Installation of stitch for concatinate the reads
while true
	do
		# checking for install
		if [ -f program/stitch/stitch.py ]; then
			echo "Installation of stitch found"
			break
		fi
	echo -n "stitch not found. Needed for concatination (optional).\n Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			mkdir program/stitch
			cd program/stitch/
				# Download of stitch (python scripts)
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
		# checking for install
		if [ -f program/blast/bin/blastn ]; then
			echo "Installation of blastn found"
			break
		fi
	echo -n "blastn not found. Needed for annotation! \n Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download and unpack program
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
		# checking for install
		if [ -f program/db/nt.nal ]; then
			echo "nt Database found for blast"
		break
		fi
	echo -n "nt database not found. Needed for annotation! \nDownload and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			mkdir program/db/
			cd program/db
				# download and compress the databases with the provided blast script
				perl ../blast/bin/update_blastdb.pl nt --decompress --passive
				cd ../..
			break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done

while true
	do
		# checking for install
		if [ -f program/db/16SMicrobial.nhr ]; then
			echo "16SMircobial Database found for blast"
			break
		fi
	echo -n "16SMicrobial database not found. (optional for 16S analysis)\nDownload and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			mkdir program/db/
			cd program/db
				# download and compress the databases with the provided blast script
				perl ../blast/bin/update_blastdb.pl 16SMicrobial --decompress --passive
			cd ../..
			break;;
		n|N|no|NO|No)
			break;
		;;
		*) echo Please enter only y or n
		esac
	done

while true
	do
		# checking for install
		if [ -f program/metavelvet/meta-velvetg ] && [ -f program/velvet/velvetg ]; then
			echo "Installation of MetaVelvet found"
			break
		fi
	echo -n "MetaVelvet not found. Download and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download and uncompress Velvet assembler (required from MetaVelvet)
				wget http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.08.tgz
				tar xzfv velvet_*
				rm velvet_1.2.08.tgz
				mv velvet* velvet
				cd velvet/
					# compile Velvet with Multicore and MiSeq k-mers
					make 'MAXKMERLENGTH=251' 'BIGASSEMBLY=1' 'LONGSEQUENCES=1' 'OPENMP=1'
				cd ..
					# Download and uncompress Velvet extension - MetaVelvet
					wget http://metavelvet.dna.bio.keio.ac.jp/src/MetaVelvet-1.2.02.tgz
					tar xzfv MetaVelvet*
					rm MetaVelvet-1.2.02.tgz
					mv MetaVelvet* metavelvet
					cd metavelvet
						# Compile MetaVelvet with MiSeq k-mers
						make 'MAXKMERLENGTH=251' 
			cd ../..
			break;;
		n|N|no|NO|No)
			break;
		;;
		*) echo Please enter only y or n
		esac
	done

while true
	do
		if [ -f program/abyss/ABYSS/ABYSS ]; then
			echo "Installation of Abyss found"
			break
		fi
	echo -n "Abyss not found. (optional for assembly)\nDownload and install it? <y|n> :"
	read CONFIRM
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				mkdir lib
				cd lib/
					# Download google sparsehash (required for abyss compilation)
					wget http://sparsehash.googlecode.com/files/sparsehash-2.0.2.tar.gz
					tar xzfv sparsehash*
					rm sparsehash-2.0.2.tar.gz
					mv sparsehash* sparsehash
					cd sparsehash/ 
						# configure and compile google sparsehash
						./configure && make
					cd ..
					# Download and uncompress openmpi (required for multithreading in abyss)
					wget http://www.open-mpi.org/software/ompi/v1.6/downloads/openmpi-1.6.3.tar.gz
					tar xzfv openmpi*
					rm openmpi-1.6.3.tar.gz
					mv openmpi* openmpi
					cd openmpi/
						# configure and compile openmpi
						./configure && make
				cd ../..
				# Download and uncompress abyss
				wget http://www.bcgsc.ca/downloads/abyss/abyss-1.3.4.tar.gz
				tar xzfv abyss*
				rm abyss-1.3.4.tar.gz
				mv abyss* abyss 
				cd abyss/
					# configure abyss for multithreading and MiSeq k-mers (max. 96) and compile
					./configure '--enable-maxk=96' '--with-mpi=../lib/openmpi/ompi' && make
			cd ../..
			break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done

echo "\n Checking Installations"
echo "Read preprocessing"
	if [ -f program/fastqc/fastqc ]; then
			echo "Installation of Abyss found"
			break
	fi 


exit 0;


