# metPipe

The metagenomic pipeline metPipe bundles a number of bioinformatical tools for analyising metagenomic short read datasets 
from RAW data to complete taxonomically annotated data. 

## 1. Requirements

### a) Hardware

The metPipe Pipeline was designed to run on s standard 64-bit Linux computer. For the analysis of short datasets and tutorial purposes (without a run of MetaCV) a minimum of 8 GB RAM is required. To analyse larger datasets and include a run of MetaCV 32 GB RAM and a multiple CPU-Cores are recommended. For the installation of the pipeline and the required databases a disk space 77 GB will be used. 

### b) Software

The Pipeline was developed with Python 2.7 and R 2.15 for standard Linux 64-bit workstations.  Before running the install script please check the following dependencies:

* Python >= 2.6
* R >= 2.15  (for R >= 3.0 useDevel() - Parameter for Bioconductor - biocLite must be assigned; see: http://www.bioconductor.org/developers/useDevel/)
* Java Runtime Environment (z.B. open-jre)
* gcc >= 4.8.0
* git
* libboost-dev
* libboost-regex-dev
* libxerces-c-dev 
* libsqlite3-dev

## 2.) Installation

After downloading the software from https://github.com/psikon/metpipe, unpack the files and run the installation script with following command :

```bash
./installer.sh
```

All external dependencies will be downloaded and installed in a local folder. The installation process may take some minutes or hours, depending on the connection speed and the databases.

## 3.) Usage:

```
usage: metpipe.py [-h] [--version] [-v] [-t THREADS] [-p PARAM]
                  [-s {preprocessing,assembly,annotation,analysis}]
                  [-o OUTPUT] [-a {metavelvet,flash,both}]
                  [-c {metacv,blastn,both}] [--use_contigs] [--notrimming]
                  [--noquality] [--noreport] [--merge]
                  input [input ...]

positional arguments:
  input                 single or paired input files in <fastq> format

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v                    more detailed output (default = False)
  -t THREADS            number of threads to use (default = 7)
  -p PARAM              use alternative config file (default = parameter.conf)
  -s {preprocessing,assembly,annotation,analysis}
                        skip steps in the pipeline (default = None)
  -o OUTPUT             use alternative output folder
  -a {metavelvet,flash,both}
                        assembling program to use (default = MetaVelvet)
  -c {metacv,blastn,both}
                        classifier to use for annotation (default = both)
  --use_contigs         should MetaCV use assembled Reads or RAW Reads
                        (default = RAW
  --notrimming          trim and filter input reads? (default = True)
  --noquality           create no quality report (default = True)
  --noreport            create no pie chart with the annotated taxonomical
                        data (default = True)
  --merge               merge concatinated reads with not concatinated
                        (default = False)
```

All step specific settings can be found in the parameter.conf file in the root dir of this program.

## 4. Quickstart

For testing/tutorial purporses a little test dataset is included in the root folder. This data include 15.000 paired-end MiSeq reads with a length of 250bp.

run the pipeline with the following command:

```bash
./metpipe.sh -t 7 -p parameter.conf -o ../example -a flash -c both sequences/forward.fastq sequences/reverse/fastq
```

After processing you will get 5 files in the analysis folder:

	- blastn.db       - blast XML results parsed in SQL Lite DB
	- annotated.db    - taxonomical annotated SQL Lite DB
	- bacteria.db     - seperated bacteria from SQL Lite DB
	- eukaryota.db    - seperated eukaryota from SQL Lite DB
	- metpipe.html    - interactic HTML5 piechart of taxonomies

## 5. Contact

If you encounter a problem/bug, please first check the wiki page:
https://github.com/psikon/metpipe/wiki
and the known issues pages:
https://github.com/psikon/metpipe/issues
to see if it has already been documented.

If not, please report the issue either using the contact information below or 
by submitting a new issue online. Please include information on your run,
and every log file produced by your run.

Philipp Sehnert: philipp.sehnert@gmail.com

## 6. Citing



		
	 
