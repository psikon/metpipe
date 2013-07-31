#!/bin/bash

# commandline interface

while getopts h opt
	do 
		case $opt in
			\?) echo "Invalid optopn: -$OPTARG"; exit 0;;
			h) echo "
Install script for the metpipe pipeline. 

Requierements: 
  boost 
  python >=2.6
  gcc 4.8
  git
  R >=2.15

USAGE: $0 [-h]

  -h show this help screen
"
exit 0;
		esac
	done

printf "Creating File Structure ...\n"

if ! [ -d programs ]; then
	mkdir programs
	cd programs/
	mkdir db/ temp/ bin/
	cd ..
fi

printf "Downloading Components ...\n"
	
	if ! [ -e programs/fastqc/fastqc ]
	then
		printf "[FastQC] \n"
		fastqc="y"
		curl -# -o programs/temp/fastqc.zip http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.10.1.zip
	fi

	if ! [ -e programs/trim_galore/trim_galore ]
	then
		printf "[TrimGalore!] \n"
		trimgalore="y"
		curl -# -o programs/temp/trim_galore.zip http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/trim_galore_v0.2.8.zip
	fi 

	if ! [ -e programs/flash/flash ]
	then
		printf "[Flash] \n"
		flash="y"
		curl -# -o programs/temp/flash.tar.gz -L http://sourceforge.net/projects/flashpage/files/latest/
	fi

	if ! [ -e programs/velvet/velvetg ]
	then
		printf "[Velvet] \n"
		velvet="y"
		curl -# -o programs/temp/velvet.tgz http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.08.tgz
	fi
 
	if ! [ -e programs/metavelvet/meta-velvetg ]
	then
		printf "[MetaVelvet] \n"
		metavelvet="y"
		curl -# -o programs/temp/metavelvet.tgz http://metavelvet.dna.bio.keio.ac.jp/src/MetaVelvet-1.2.02.tgz 
	fi
	
	if ! [ -e programs/blast/bin/blastn ]
	then
		printf "[Blast] \n"
		blast="y"
		curl -# -o programs/temp/blast.tar.gz ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.28/ncbi-blast-2.2.28+-x64-linux.tar.gz
	fi
	
	if ! [ -e programs/metacv/metacv ]
	then
		printf "[MetaCV] \n"
		metacv="y"
		curl -# -o programs/temp/metacv.tgz -L http://sourceforge.net/projects/metacv/files/latest/
	fi
	
	if ! [ -e programs/fastx/fastq_to_fasta ]
	then
		printf "[FastX toolkit] \n"
		fastx="y"
		curl -# -o programs/temp/fastx.tar.bz2 http://hannonlab.cshl.edu/fastx_toolkit/fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2 
	fi

	if ! [ -e programs/krona/install.pl ]
	then
		printf "[krona webtools] \n"
		krona="y"
		curl -# -o programs/temp/krona.tar -L http://sourceforge.net/projects/krona/files/latest/
	fi

	if ! [ -d programs/xmlParser/ ]
	then
		printf "[XML parser] \n"
		xmlParser="y"
		git clone https://github.com/gschofl/bigBlastParser.git programs/xmlParser
	fi

	printf "Extracting ...\n"

	if [ "$fastqc" = "y" ] 
	then
		unzip -o -q -d programs/ programs/temp/fastqc.zip 
		mv programs/FastQC programs/fastqc 
	fi
	if [ "$trimgalore" = "y" ] 
	then
		unzip -o -q -d programs/ programs/temp/trim_galore.zip
		mv programs/trim_galore_zip programs/trim_galore 
	fi

	if [ "$flash" = "y" ] 
	then
		tar -C programs/ -xzvf programs/temp/flash.tar.gz  > /dev/null
		mv programs/FLASH* programs/flash
		cd programs/flash
			make -s
			rm *.o
		cd ../.. 
	fi

	if [ "$velvet" = "y" ] 
	then
		tar -C programs/ -xzvf programs/temp/velvet.tgz > /dev/null  
		cd programs/velvet
			 compile Velvet with Multicore and MiSeq k-mers
			make -s 'MAXKMERLENGTH=251' 'BIGASSEMBLY=1' 'LONGSEQUENCES=1' 'OPENMP=1'
		cd ../..
	fi

	if [ "$metavelvet" = "y" ]
	then 
		tar -C programs/ -xzvf programs/temp/metavelvet.tgz > /dev/null
		mv programs/MetaVelvet* programs/metavelvet
		cd programs/metavelvet
			make -s 'MAXKMERLENGTH=251' > /dev/null
		cd ../..
	fi

	if [ "$blast" = "y" ]
	then 
		tar -C programs/ -xzvf programs/temp/blast.tar.gz > /dev/null 
		mv programs/ncbi-blast* programs/blast
	fi

	if [ "$metacv" = "y" ]
	then 
		tar -C programs/ -xzvf programs/temp/metacv.tgz > /dev/null 
		mv programs/metacv_* programs/metacv 
		cd programs/metacv
			make -s 
		cd ../..
	fi

	if [ "$fastx" = "y" ]
	then 
		tar -C programs/ -xvjf programs/temp/fastx.tar.bz2 > /dev/null 
		mv programs/bin programs/fastx 
	fi

	if [ "$krona" = "y" ]
	then 
		tar -C programs/ -xvf programs/temp/krona.tar > /dev/null && 
		mv programs/Krona* programs/krona
		./programs/krona/install.pl --prefix . > /dev/null
	fi

	if [ "$xmlParser" = "y" ]
	then 
		cd programs/xmlParser/
			make -s
			make clean
		cd ../..
	fi


	printf "Creating Databases ... \n"
	
	printf "[create or update nt database]\n"
	cd programs/db/
	#	./../blast/bin/update_blastdb.pl --passive --decompress nt
	

	printf "[create or update taxonomy database]\n"
	
	#if ! [ -e taxon.db ] && ! [ -f geneid.db ]
	#then
	#	R -q -e "require(ncbi);createTaxonDB('.')"
	#fi
	
	#cd ../krona/
	#	./updateTaxonomy.sh
	#cd ../db/
	counter="0"
	while  ! [ -e cvk6_2059.cnt ] && ! [ "$counter" -eq 3 ]
	do
		printf "[create MetaCV database]\n"

		if [ ! -e db.part00 ]
	 	then
			printf "downloading Part 0/7 ...\n"
			curl -o db.part00 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part00 
		elif [ "$(ls -l db.part00 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part00 | awk '/Content-Length/ { print $2 }')" ]
		then
			printf "Download not complete. Try again!\n"
			rm db.part00
			printf "downloading Part 0/7 ...\n"
			curl -o db.part00 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part00 
		fi

		if [ ! -e db.part01 ]
		then
			printf "downloading Part 1/7 ...\n"
			curl -o db.part01 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part01
		elif [ "$(ls -l db.part01 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part01 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part01
			printf "downloading Part 1/7 ...\n"
			curl -o db.part01 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part01
		fi 
	
		if [ ! -e db.part02 ]
		then
			printf "downloading Part 2/7 ...\n"
			curl -o db.part02 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part02
		elif [ "$(ls -l db.part02 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part02 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part02
			printf "downloading Part 2/7 ...\n"
			curl -o db.part02 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part02
		fi 
		
		if [ ! -e db.part03 ]
		then
			printf "downloading Part 3/7 ...\n"
			curl -o db.part03 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part03
		elif [ "$(ls -l db.part03 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part03 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part03
			printf "downloading Part 3/7 ...\n"
			curl -o db.part03 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part03
		fi 

		if [ ! -e db.part04 ]
		then
			printf "downloading Part 4/7 ...\n"
			curl -o db.part04 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part04
		elif [ "$(ls -l db.part04 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part04 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part04
			printf "downloading Part 4/7 ...\n"
			curl -o db.part04 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part04
		fi 

		if [ ! -e db.part05 ]
		then
			printf "downloading Part 5/7 ...\n"
			curl -o db.part05 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part05
		elif [ "$(ls -l db.part01 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part05 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part05
			printf "downloading Part 5/7 ...\n"
			curl -o db.part05 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part05
		fi 

		if [ ! -e db.part06 ]
		then
			printf "downloading Part 6/7 ...\n"
			curl -o db.part06 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part06
		elif [ "$(ls -l db.part06 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part06 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part06
			printf "downloading Part 6/7 ...\n"
			curl -o db.part06 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part06
		fi 
		
		if [ ! -e db.part07 ]
		then
			printf "downloading Part 7/7 ...\n"
			curl -o db.part07 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part07
		elif [ "$(ls -l db.part07 | awk '{ print $5 }')" -lt "$(curl -sI http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part07 | awk '/Content-Length/ { print $2 }')" ]
		then 
			printf "Download not complete. Try again!\n"
			rm db.part07
			printf "downloading Part 7/7 ...\n"
			curl -o db.part07 -# http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part07
		fi
		
		cat db.part* | tar xvzp
		counter=$(($counter+1))
		if [ -e cvk6_2059.cnt ] 
		then 
			rm db.part*
			break
		fi
	done

exit 0;		
