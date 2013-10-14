# metPipe


Philipp Sehnert
philipp.sehnert@gmail.com

This software package bundles a number of standard software for the analysis of metagenomic datasets 
under one surface. The pipeline is developed for the processing of the new Illumina MiSeq technology 
with its long read lengths of up to 250 bp, but is also capable to process the older Illumina HiSeq 
reads.

### Requirements

  - Python >= 2.6
  - R >= 2.15 
  - (for R >= 3.0 useDevel() - Parameter for Bioconductor - biocLite muss be assigned
    see: http://www.bioconductor.org/developers/useDevel/)
  - libboost-dev
  - libboost-regex-dev
  - Java Runtime Environment (z.B. open-jre)
  - Linux (Mac OS X possible, but not tested) 
  

### Installation

The pipeline provide an automatic installer script in the main folder. To install all necassary components 
for the pipeline just start this skript in a unix shell by the following command.

```bash
./installer.sh
```
Follow the instructions on the screen and all necassary programs will be downloaded and make runable 
automatically.

### Usage:

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
  -c {metacv,blastn,both}
                        classifier to use for annotation (default= both)
  --notrimming          trimm and filter input reads? (default=True)
  --noquality           create quality report (default=True)

```

All step specific settings can be found in the parameter.conf file in the root dir of this program.

### Parts of this pipeline

- FastQC (http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- TrimGalore! (http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/)
- MetaVelvet (http://metavelvet.dna.bio.keio.ac.jp/) 
	Namiki T*, Hachiya T*, Tanaka H, Sakakibara Y. (2012) 
	MetaVelvet : An extension of Velvet assembler to de novo 
	metagenome assembly from short sequence reads, 
	Nucleic Acids Res.
- stitch audy/stitch
- Blastn (http://www.ncbi.nlm.nih.gov/books/NBK1763/
	Altschul, S.F., Gish, W., Miller, W., Myers, E.W. & Lipman, D.J. 
	(1990) "Basic local alignment search tool." 
	J. Mol. Biol. 215:403-410. PubMed
- MetaCV (http://metacv.sourceforge.net/)
		
	 
