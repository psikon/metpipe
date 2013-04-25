#!/bin/bash

while getopts hscq opt
	do
		case $opt in
			\?) echo "Invalid option :-$OPTARG"; exit 0;;
			c) less citations.txt; exit 0;;			
			q) echo "Quiet install enabled"
			   quiet="y";;
			s) echo "Components of metpipe:
[Read Quality Check and Trimming]
- FastQC
- Trim Galore!
[Assembler]
- MetaVelvet
- Velvet
- concatination of the reads
[Annotate]
- Blastn (nt|16SMicrobial)
- MetaCV
[Classifier]
- MetaCV
"
exit 0;;
			-h) echo "
This is the install script of the pipeline. All relevant programms will be checked and installed if not existing.

Requirments: boost
             python 2.6+
             perl
              
USAGE: $0 [-h]

 -h show help screen 
 -q silent install install all required components
 -s show all included programms
 -c show all citations for the used programs
"
exit 0;
		esac
	done

echo "Installation of the metPipe Programms.\n"

# create needed directories
if ! [ -d program ]; then
	mkdir program/
fi 

if ! [ -d program/db ]; then
	mkdir program/db/
fi



##### Preprocessing Tools #####

# Installation of FastQC for quality checks
while true
	do
		# checking for install
		if [ -f program/fastqc/fastqc ]; then
			echo "Installation of FastQC found"
			break
		fi
	
		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "FastQC not found. Needed for quality checks.\nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download and uncompress FastQC
http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.10.1.zip
				wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.10.1.zip
				unzip fastqc*
				rm fastqc_*.zip
				mv FastQC* fastqc
			cd ..
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
		if [ -f program/trim_galore/trim_galore ]; then
			echo "Installation of Trim Galore! found"
			break
		fi
		
		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "Trim Galore! not found. Needed for quality trimming.\nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download Trim Galore! 
				mkdir trim_galore
				cd trim_galore
					wget http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/trim_galore_v0.2.8.zip
					unzip trim_galore*
					if [ -d trim_galore_zip ]; then
						mv trim_galore_zip/* ../trim_galore && rm -r trim_galore_zip
					fi
					rm trim_galore_v0.2.*.zip
			cd ../..
			break;;
		n|N|no|NO|No)
			break;
		;;
		*) echo Please enter only y or n
		esac
	done

##### Assembly Tools #####

while true
	do
		# checking for install
		if [ -f program/stitch/stitch/stitch.py ]; then
			echo "Installation of stitch found"
			break
		fi


		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "stitch not found. Needed for concatination (optional).\n Download and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			mkdir program/stitch
			cd program/
				# Download of stitch (python scripts)
				git clone https://github.com/audy/stitch.git
			cd ..
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
	
		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "MetaVelvet not found. Download and install it? <y|n> :"
			read CONFIRM
		fi
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

##### Annotate Tools #####

# Installation of blastn for annotation of the reads
while true
	do	
		# checking for install
		if [ -f program/blast/bin/blastn ]; then
			echo "Installation of blastn found"
			break
		fi

		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "blastn not found. Needed for annotation! \n Download and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download and unpack program
				wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-*-x64-linux.tar.gz
				chmod 775 ncbi-blast*
				tar xzfv ncbi-blast*
				rm ncbi-blast-2.2.28+-x64-linux.tar.gz
				mv ncbi-blast-2.2.28+ blast
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
		
		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "nt database not found. Needed for annotation! \nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/db
				# download and decompress the databases with the provided blast script
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
	
		if [ "$quiet" = "y" ]; then	
			CONFIRM="n"
		else
			echo -n "16SMicrobial database not found. (optional for 16S analysis)\nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/db
				# download and decompress the databases with the provided blast script
				perl ../blast/bin/update_blastdb.pl 16SMicrobial --decompress --passive
			cd ../..
			break;;
		n|N|no|NO|No)
			break;
		;;
		*) echo Please enter only y or n
		esac
	done

##### Classify Tools #####


# Installation of MetaCV
while true
	do
		# checking for install
		if [ -f program/metacv/metacv ]; then
			echo "Installation of MetaCV found"
			break
		fi
	
		if [ "$quiet" = "y" ]; then	
			CONFIRM="n"
		else
			echo -n "MetaCV not found. (optional classify)\nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program
				wget http://sourceforge.net/projects/metacv/files/latest/metacv_2_3_0.tgz
				tar xzfv metacv_*
				rm metacv_2_3_0.tgz
				mv metacv_* metacv
				cd metacv/
					make
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
		# checking for MetaCV Database
		if [ -f program/db/cvk6_2059.cnt ]; then
			echo "MetaCV database found"
			break
		fi
	
		if [ "$quiet" = "y" ]; then	
			CONFIRM="n"
		else
			echo -n "MetaCV database not found. (optional for classify with MetaCV)\nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/db/
				# download and decompress the database for MetaCV
				if [ ! -f db.part00 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part00
				fi
				if [ ! -f db.part01 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part01
				fi
				if [ ! -f db.part02 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part02
				fi
				if [ ! -f db.part03 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part03
				fi
				if [ ! -f db.part04 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part04
				fi
				if [ ! -f db.part05 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part05
				fi
				if [ ! -f db.part06 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part06
				fi
				if [ ! -f db.part07 ]; then
					wget http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part07
				fi
				cat db.part* | tar xvzp
				rm db.part*
			cd ../..
			break;;
		n|N|no|NO|No)
			break;
		;;
		*) echo Please enter only y or n
		esac
	done

#while true
#	do
#		# checking for Phylosift installation
#		if [ -f program/phylosift/phylosift ]; then
#			echo "Phylosift installation found"
#			break
#		fi
#	
#		if [ "$quiet" = "y" ]; then	
#			CONFIRM="n"
#		else
#			echo -n "Phylosift installation not found. (optional for classify)\nDownload and install it? <y|n> :"
#			read CONFIRM
#		fi
#	case $CONFIRM in
#		y|Y|YES|yes|Yes) 
#			cd program/
#				wget http://edhar.genomecenter.ucdavis.edu/~koadman/phylosift/releases/phylosift_v1.0.0_01.tar.bz2
#				tar -xvf phylosift*
#				rm phylosift_v1.0.0_01.tar.bz2
#				mv phylosift* phylosift
#			cd ..
#			break;;
#		n|N|no|NO|No)
#			break;
#		;;
#		*) echo Please enter only y or n
#		esac

##### Misc Tools #####

while true
	do
		if [ -f program/fastx/fastq_to_fasta ]; then
			echo "Installation of FastX toolkit found"
			break
		fi
	
		if [ "$quiet" = "y" ]; then	
			CONFIRM="y"
		else
			echo -n "FastX toolkit not found. (required)\nDownload and install it? <y|n> :"
			read CONFIRM
		fi
	case $CONFIRM in
		y|Y|YES|yes|Yes) 
			cd program/
				# Download and uncompress the binaries 
				wget http://hannonlab.cshl.edu/fastx_toolkit/fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2
				tar xvjf fastx*
				rm fastx*.tar.bz2
				mv bin* fastx
			cd ..
			break;;
		n|N|no|NO|No)
		break;
		;;
		*) echo Please enter only y or n
		esac
	done


echo "\n Checking Installations\n"
echo "[Read preprocessing]"
if [ -f program/fastqc/fastqc ] && [ -f program/trim_galore/trim_galore ]; then
	echo "Preprocessing tools OK!"
	ln -s -f fastqc/fastqc program/quality && chmod 775 program/quality
	ln -s -f trim_galore/trim_galore program/filter && chmod 775 program/filter
else 
	echo "Preprcessing tool missing"
fi
echo "\n[Assembly programs]"
if [ -f program/stitch/stitch/stitch.py ]; then
	echo "Assembly - Concatenation OK!"
	ln -s -f stitch/stitch/stitch.py program/concat && chmod 775 program/concat
fi	

if [ -f program/velvet/velveth ] && [ -f program/velvet/velvetg ] && [ -f program/metavelvet/meta-velvetg ]; then
	echo "Assembly - MetaVelvet OK!"
	ln -s -f velvet/velveth program/velveth && chmod 775 program/velveth
	ln -s -f velvet/velvetg program/velvetg && chmod 775 program/velvetg
	ln -s -f metavelvet/meta-velvetg program/metavelvetg && chmod 775 program/metavelvetg
fi

echo "\n[Annotation programs]"
if [ -f program/blast/bin/blastn ] && [ -f program/db/nt.nal ]; then
	echo "Annotate - Blastn OK!"
	ln -s -f blast/bin/blastn program/blastn && chmod 775 program/blastn
fi

if  [ -f program/metacv/metacv ] && [ -f program/db/cvdb_2059.cnt ]; then
	echo "Annotate - MetaCV OK!"
	ln -s -f metacv/metacv program/metaCV && chmod 775 program/metaCV
fi



	


exit 0;


