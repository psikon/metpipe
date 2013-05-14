# metPipe

This software package bundles a number of standard software for the analysis of metagenomic datasets 
under one surface. The pipeline is developed for the processing of the new Illumina MiSeq technology 
with its long read lengths of up to 250 bp, but is also capable to process the older Illumina HiSeq 
reads.

## Requirements

  - Python >= 2.6
  - R >= 2.15
  - Java Runtime Environment (z.B. open-jre)

## Installation

The pipeline provide an automatic installer script in the main folder. To install all necassary components 
for the pipeline just start this skript in a unix shell by the following command.

```bash
sh install.sh
```
Folow the instructions on the screen and all necassary programs will be downloaded and make runable 
automatically.

## Usage:

```python
python metpipe.py [-h] [--version] [-v] [-t THREADS] [-p PARAM]
                  [-s {Preprocessing,Assembly,Annotation}] [-o OUTPUT]
                  [-a {metavelvet,concat}] [-k KMER] [-c {metacv,blastn,both}]
                  [--notrimming] [--noquality]
                  input [input ...]

positional arguments:
  input                 single or paired input files in <fastq> format

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v                    more detailed output (default=False)
  -t THREADS            number of threads to use (default=3)
  -p PARAM              use alternative config file (default=parameter.conf)
  -s {Preprocessing,Assembly,Annotation}
                        skip steps in the pipeline (default=None)
  -o OUTPUT             use alternative output folder
  -a {metavelvet,concat}
                        assembling program to use (default= MetaVelvet)
  -k KMER               k-mer size to be used (default=85)
  -c {metacv,blastn,both}
                        classifier to use for annotation (default= both)
  --notrimming          trimm and filter input reads? (default=True)
  --noquality           create quality report (default=True)

```

All step specific settings can be found in the parameter.conf file in the root dir of this program.
 
### not working

- change parameter for metavelvet
- no verbose mode at the moment
- no log functions
- analysis of the results under development
 
## Citations
