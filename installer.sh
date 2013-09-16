#!/bin/bash
#
# TITLE:    metpipe_installer.sh - Install metpipe dependencies
# SYNOPSIS: metpipe_installer.sh [-h]
# DATE:     28/08/2013
# VERSION:  0.0.1
# AUTHOR:   Gerhard Schöfl
# LICENCE:  MIT
#
# PLATFORM: Ubuntu Linux
#
# PURPOSE:  Longer description of the purpose of this script.
#
#set -n    # Check syntax without execution.
#set -x    # Trace execution.

#### URLS AND DESTINATION PATHS #####################################

__fastaqc_src=tmp/fastqc.zip
__fastagc_url=http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.10.1.zip

__trimgalore_src=tmp/trim_galore.zip 
__trimgalore_url=http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/trim_galore_v0.2.8.zip

__flash_src=tmp/flash.tar.gz 
__flash_url=http://sourceforge.net/projects/flashpage/files/latest/

__velvet_src=tmp/velvet.tgz
__velvet_url=http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.08.tgz

__metavelvet_src=tmp/metavelvet.tgz
__metavelvet_url=http://metavelvet.dna.bio.keio.ac.jp/src/MetaVelvet-1.2.02.tgz

__blast_src=tmp/blast.tar.gz
__blast_url=ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.28/ncbi-blast-2.2.28+-x64-linux.tar.gz

__metacv_src=tmp/metacv.tgz
__metacv_url=http://sourceforge.net/projects/metacv/files/latest/

__fastx_src=tmp/fastx.tar.bz2
__fastx_url=http://hannonlab.cshl.edu/fastx_toolkit/fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2

__krona_src=tmp/krona.tar
__krona_url=http://sourceforge.net/projects/krona/files/latest/

__blastparser_src=blastparser
__blastparser_url=https://github.com/gschofl/bigBlastParser.git

## 7 parts
__metacv_db_url=http://switch.dl.sourceforge.net/project/metacv/cvdb_2059/db.part0

#### FUNCTIONS ######################################################

usage() {
    # @DESCRIPTION: print usage information
    # @USAGE: usage
    printf "\n%s\n\n" "Installation script for the metpipe pipeline."
    printf "REQUIREMENTS:\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\n" \
            "boost >= 4.8" \
            "python >= 2.6" \
            "gcc >= 4.8" \
            "git" \
            "R >= 3.0.1"
    printf "USAGE:\n\t%s [-h]\n\n" "$0"
    printf "\t%s\t%s\n\n" "-h" "Display this help and exit."
}

die() {
    # @DESCRIPTION: print error message and exit with supplied return code
    # @USAGE: die STATUS [MESSAGE]
    error=$1
    shift
    [ -n "$*" ] &&  printf "%s\n" "$*" >&2
    exit $error
}

create_metpipe_dir() { 
    # @DESCRIPTION: let the user choose where to install metpipe and create
    #  the appropriate file infrastructure.
    # @USAGE: create_metpipe_dir
    echo ""
    echo "In which directory do you want to install metpipe [~/local/bioinf]: " | tr -d "\n"
    local answer=
    read answer
    eval __base__=${answer:-${HOME}/local/bioinf}
    answer=
    
    __metdir=${__base__}/metpipe
    __extdir=${__metdir}/ext
    __tmpdir=${__extdir}/tmp

    __pkgdir=${__metdir}/pkg
    __srcdir=${__metdir}/src
    __db_dir=${__metdir}/db

    if [ ! -d "$__metdir" ]; then
        mkdir -p ${__tmpdir}
        [ $? -eq 0 ] || die 1 "Use \"sudo metpipe_installer.sh\" or set a different target directory"
        mkdir ${__pkgdir}
        mkdir ${__srcdir}
        mkdir ${__db_dir}
    else
        printf "\nA metpipe installation is already in place in %s.\n" "${__metdir}"
        printf "Do you want to overwrite the existing installation? [y|N]: " | tr -d "\n"
        read answer
        __force=
        if [ "${answer}" == "y" ]; then
            __force="-f"
        fi
        answer=
    fi

    cp ${__force} ./pkg/*.tar.gz ${__pkgdir}
    cp ${__force} ./src/*.py ${__srcdir}
    cp ${__force} ./{*.py,*.txt,*.conf,*.md} ${__metdir} 

    echo ""
    echo "Where do you want to install the binaries [${__metdir}/bin]: " | tr -d "\n"
    read answer
    eval __bindir=${answer:-${__metdir}/bin}
    answer=
    [ -d "$__bindir" ] || mkdir -p $__bindir

    printf "\nCreating File Structure ...\n\n"
}

check_dependency() {
    # @DESCRIPTION: check if a dependency is already available somewhere
    # on the system or in the specified $__bindir. If this is the case,
    # ask if we want do use the installed binary, or if a dependency
    # should be installed/reinstalled specifically for metpipe.
    # @USAGE: check_dependency IN:cmd OUT:fetch[y|n] OUT:cmdpath
    # @REQUIRES $__bindir

    ## first look globally for cmd
    local found=$(command -v $1)

    ## if it isn't there look in $__bindir
    if [ -z "${found}" ]; then
        found=$(find ${__bindir} -name $1 -print 2> /dev/null)
    fi

    local __fetch=$2
    local __cmdpath=$3

    if [ -n "$found" ]; then
        echo ""
        echo "\"$1\" is already available at \"${found%/*}\"."
        echo "Do you want to (re)install a version for metpipe? [y|N] " | tr -d "\n"
        local answer=
        read answer
        eval $__fetch="'${answer:-n}'"
        if [ "$answer" == "y" ]; then
            eval $__cmdpath="'$__bindir/$1'"
        else
            eval $__cmdpath="'$found'"
        fi
    else
        eval $__fetch="y"
        eval $__cmdpath="'$__bindir/$1'"
    fi
}

set_param_in_conf() {
    # @DESCRIPTION: Set a parameter-value pair in the configuration file [parameter.conf}
    # directly on the line after a [TAG]. Omit the brackets around the tag!
    # @USAGE: set_param_in_conf $tag $param $value
    # @EXAMPLE: set_param_in_conf TrimGalore path /opt/metpipe/bin
    # will set "path = /opt/metpipe/bin" under [TrimGalore]

    local __tag=$1
    local __param=$2
    local __value=$3
    local __conf=${__metdir}/parameter.conf

    sed -e '/\['"${__tag}"'\]/ {
            n
            c'"${__param}"' = '"${__value}"'
    }' < ${__conf} > ${__conf}~
    mv ${__conf}~ ${__conf}
}

install_fastqc() {
    # @USAGE: install_fastqc

    local fetch=
    local cmdpath=
    check_dependency fastqc fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading FastQC ...\n"
        curl -# -o ${__extdir}/${__fastaqc_src} ${__fastagc_url}

        printf "Installing FastQC ."
        unzip -o -q -d ${__extdir} ${__extdir}/${__fastaqc_src}
        [ -d "${__extdir}/fastqc" ] && rm -rf "${__extdir}/fastqc"
        mv ${__extdir}/FastQC ${__extdir}/fastqc

        printf "."
        chmod 755 ${__extdir}/fastqc/fastqc
        cmdpath=${__bindir}/
        ln -sf ${__extdir}/fastqc/fastqc ${cmdpath}
    fi

    printf "."
    set_param_in_conf "FastQC" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_trimgalore() {
    # @USAGE: install_trimgalore

    local fetch=
    local cmdpath=
    check_dependency trim_galore fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading Trim Galore! ...\n"
        curl -# -o ${__extdir}/${__trimgalore_src} ${__trimgalore_url}

        printf "Installing Trim Galore! ."
        unzip -o -q -d ${__extdir} ${__extdir}/${__trimgalore_src}
        [ -d "${__extdir}/trim_galore" ] && rm -rf "${__extdir}/trim_galore"
        mv ${__extdir}/trim_galore_zip ${__extdir}/trim_galore 

        printf "."
        chmod 755 ${__extdir}/trim_galore/trim_galore
        cmdpath=${__bindir}/
        ln -sf ${__extdir}/trim_galore/trim_galore ${cmdpath}
    fi

    printf "."
    set_param_in_conf "TrimGalore" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_flash() {
    # @USAGE: install_flash

    local fetch=
    local cmdpath=
    check_dependency flash fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading Flash ...\n"
        curl -# -o ${__extdir}/${__flash_src} -L ${__flash_url}

        printf "Installing Flash ."
        tar -C ${__extdir} -xzvf ${__extdir}/${__flash_src} > /dev/null
        [ -d "${__extdir}/flash" ] && rm -rf "${__extdir}/flash"
        mv ${__extdir}/FLASH* ${__extdir}/flash

        printf "."
        __cwd=$(pwd)
        cd ${__extdir}/flash
            printf "."
            make -s
            [ $? -eq 0 ] || die 1 "ERROR: Installation of Flash failed"
            # clean up the installation manually
            rm *.o
        cd ${__cwd} 

        cmdpath=${__bindir}/
        ln -sf ${__extdir}/flash/flash ${cmdpath}
    fi

    printf "."
    set_param_in_conf "FLASH" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_velvet() {
    # @USAGE: install_velvet

    local fetch=
    local cmdpath=
    local ncores=
    check_dependency velvetg fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading Velvet ...\n"
        curl -# -o ${__extdir}/${__velvet_src} ${__velvet_url}

        printf "Installing Velvet ."
        tar -C ${__extdir} -xzvf ${__extdir}/${__velvet_src} > /dev/null

        printf "."
        __cwd=$(pwd)
        cd ${__extdir}/velvet
            printf "."
            ncores=$(cat /proc/cpuinfo | awk '/^processor/ { print $3 }' | wc -l)
            make -s 'MAXKMERLENGTH=251' 'BIGASSEMBLY=1' 'LONGSEQUENCES=1' "OPENMP=${ncores}"
            [ $? -eq 0 ] || die 1 "ERROR: Installation of Velvet failed"
        cd ${__cwd} 

        cmdpath=${__bindir}/
        ln -sf ${__extdir}/velvet/velvetg ${cmdpath}
        ln -sf ${__extdir}/velvet/velveth ${cmdpath}
    fi

    printf "."
    set_param_in_conf "Velvet" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_metavelvet() {
    # @USAGE: install_metavelvet

    local fetch=
    local cmdpath=
    check_dependency meta-velvetg fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading MetaVelvet ...\n"
        curl -# -o ${__extdir}/${__metavelvet_src} ${__metavelvet_url}

        printf "Installing MetaVelvet ."
        tar -C ${__extdir} -xzvf ${__extdir}/${__metavelvet_src} > /dev/null
        [ -d "${__extdir}/metavelvet" ] && rm -rf "${__extdir}/metavelvet"
        mv ${__extdir}/MetaVelvet* ${__extdir}/metavelvet

        printf "."
        __cwd=$(pwd)
        cd ${__extdir}/metavelvet
            printf "."
            # compile MetaVelevet with MiSeq k-mers 
            make -s 'MAXKMERLENGTH=251'
            [ $? -eq 0 ] || die 1 "ERROR: Installation of MetaVelvet failed"
        cd ${__cwd} 

        cmdpath=${__bindir}/
        ln -sf ${__extdir}/metavelvet/meta-velvetg ${cmdpath}
    fi

    printf "."
    set_param_in_conf "MetaVelvet" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_fastx() {
    # @USAGE: install_fastx

    local fetch=
    local cmdpath=
    check_dependency fastq_to_fasta fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading FastX ...\n"
        curl -# -o ${__extdir}/${__fastx_src} ${__fastx_url}

        printf "Installing FastX ."
        tar -C ${__extdir} -xvjf ${__extdir}/${__fastx_src} > /dev/null
        [ -d "${__extdir}/fastx" ] && rm -rf "${__extdir}/fastx"
        mv ${__extdir}/bin ${__extdir}/fastx

        [ $? -eq 0 ] || die 1 "ERROR: Installation of FastX failed"

        cmdpath=${__bindir}/ 
        ln -sf ${__extdir}/fastx/fastq_to_fasta ${cmdpath}        
    fi

    printf "."
    set_param_in_conf "FastX" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_blastparser() {
    # @USAGE: install_xmlparser

    local fetch=
    local cmdpath=
    check_dependency bigBlastParser fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading blastParser ...\n"
        [ -d "${__extdir}/${__blastparser_src}" ] && rm -rf "${__extdir}/${__blastparser_src}"
        git clone ${__blastparser_url} ${__extdir}/${__blastparser_src} > /dev/null

        printf "Installing blastParser ."
        __cwd=$(pwd)
        cd ${__extdir}/${__blastparser_src}
            make -s
            printf "."
            [ $? -eq 0 ] || die 1 "ERROR: Installation of blastParser failed"
            make clean > /dev/null
        cd ${__cwd}

        cmdpath=${__bindir}/
        ln -sf ${__extdir}/${__blastparser_src}/bigBlastParser ${cmdpath}         
    fi

    printf "."
    set_param_in_conf "blastParser" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

install_blast() {
    # @USAGE: install_blast

    local fetch=
    local cmdpath=
    check_dependency blastn fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading Blast ...\n"
        curl -# -o ${__extdir}/${__blast_src} ${__blast_url}

        printf "Installing Blast ."
        tar -C ${__extdir} -xzvf ${__extdir}/${__blast_src} > /dev/null
        printf "."
        [ -d "${__extdir}/blast" ] && rm -rf "${__extdir}/blast"
        mv -f ${__extdir}/ncbi-blast* ${__extdir}/blast

        [ $? -eq 0 ] || die 1 "ERROR: Installation of Blast failed"

        cmdpath=${__bindir}/ 
        ln -sf ${__extdir}/blast/bin/blastn ${cmdpath}
        ln -sf ${__extdir}/blast/bin/update_blastdb.pl ${cmdpath}/update_blastdb
    fi

    printf "."
    set_param_in_conf "blastn" "path" ${cmdpath%/*}
    printf ". OK!\n\n"

    get_nt_db ${cmdpath%/*}
}

get_nt_db() {
    # @USAGE: get_nt_db path/to/update_blastdb
    # @REQUIRES: $__db_dir $__metdir

    local __blast_db=${__db_dir}/blast
    [ -e "${__blast_db}" ] || mkdir -p ${__blast_db}

    echo ""
    echo "**** metpipe requires a local installation of the nt BLAST database. ****"
    echo ""
    echo "You can skip this step entirely for now and adapt the settings in"
    echo "\"${__metdir}/parameter.conf\" at a later point."
    echo ""
    echo "Alternatively, you can proceed and provide the path to an existing"
    echo "BLAST nt database or download the entire nt database to \"${__blast_db}\"."
    echo "Be aware that this will take a lot of time!"
    echo ""
    echo "Skip? [Y|n] " | tr -d "\n"
    local skip=
    read skip
    eval skip=${skip:-y}
    if [ "$skip" != "n" -a "$skip" != "N" ]; then
        echo ""
        return 0
    else
        echo ""
        echo "To download the BLAST nt database to \"${__blast_db}\" press ENTER."
        echo "Alternatively, provide the path to an existing nt database: " | tr -d "\n"
        local answer=
        read answer
        eval __nt_dir=${answer}
        answer=
        if [ -n "${__nt_dir}" ]; then
            ## if a path was provided count the number of nt.xx.nsq files in
            ## the db directory.
            ## Abort if 0 or not all 14 are available 
            nt_files=$(ls ${__nt_dir}/nt.{01..12}.nsq 2> /dev/null | wc -l)
            [ $nt_files -gt 0 -a $nt_files -eq 12 ] || die 1 "ERROR: No or not all nt database files found at ${__nt_dir}.\n"
        else
            local counter=0
            local cwd=$(pwd)
            cd ${__blast_db}
                printf "[create or update nt database]\n"
                ${1}/update_blastdb --passive --decompress nt
                while [ $counter -lt 3 -a ! $? -eq 0 ]; do
                    ${1}/update_blastdb --passive --decompress nt
                    $(( counter++ ))
                    printf "\n"
                done
            cd ${cwd}
            __nt_dir=${__blast_db}
        fi
        ## finally set __nt_dir in parameter.conf
        local __conf=${__metdir}/parameter.conf
        sed -e '/# location of db/ {
                n
                s:db =:db = '"${__nt_dir}"':
            }' < ${__conf} > ${__conf}~
        mv ${__conf}~ ${__conf}
    fi
    echo ""
}

install_metacv() {
    # @USAGE: install_metacv

    local fetch=
    local cmdpath=
    check_dependency metacv fetch cmdpath

    if [ "$fetch" == "y" ]; then
        printf "Downloading MetaCV ...\n"
        curl -# -o ${__extdir}/${__metacv_src} -L ${__metacv_url}

        printf "Installing MetaCV ."
        tar -C ${__extdir} -xzvf ${__extdir}/${__metacv_src} > /dev/null
        printf "."
        [ -d "${__extdir}/metacv" ] && rm -rf "${__extdir}/metacv"
        mv -f ${__extdir}/metacv_* ${__extdir}/metacv

        printf "."
        __cwd=$(pwd)
        cd ${__extdir}/metacv
            printf "."
            make -s
            [ $? -eq 0 ] || die 1 "ERROR: Installation of MetaCV failed"
        cd ${__cwd} 

        cmdpath=${__bindir}/
        ln -sf ${__extdir}/metacv/metacv ${cmdpath}        
    fi

    printf "."
    set_param_in_conf "MetaCV" "path" ${cmdpath%/*}
    printf ". OK!\n\n"

    get_metacv_db ${__metacv_db_url}
}

get_metacv_db() {
    # @DESCRIPTION
    # @USAGE: get_metacv_db url
    # @REQUIRES: $__db_dir

    local __metacv_db=${__db_dir}/metacv
    [ -e "${__metacv_db}" ] || mkdir -p ${__metacv_db}

    echo ""
    echo "**** MetaCV requires downloading about 16GB of database files. ****"
    echo ""
    echo "If you already have MetaCV installed on your system you should"
    echo "skip this step."
    echo ""
    echo "You can also skip this step for now and place the database files"
    echo "into \"${__metacv_db}/\" at a later point by rerunning this script."
    echo ""
    echo "Skip? [Y|n] " | tr -d "\n"
    local skip=
    read skip
    eval skip=${skip:-y}
    if [ "$skip" != "n" -a "$skip" != "N" ]; then
        echo ""
        return 0
    else
        local counter=0
        local cwd=$(pwd)
        printf "\n[creating MetaCV database]\n"
        cd ${__metacv_db}
        while [ $counter -lt 3 -a ! -e cvk6_2059.cnt ]
        do
            for n in {0..7}
            do
                local __url__=${1}${n}
                local __part__=${__url__##*/}
                if [ ! -e ${__part__} ]; then
                    printf "downloading Part ${__part__: -1}/7 ...\n"
                    curl -o ${__part__} -# ${__url__}
                elif [ download_is_incomplete ]; then
                    printf "Download not complete. Try again!\n"
                    rm ${__part__}
                    printf "downloading Part ${__part__: -1}/7 ...\n"
                    curl -o ${__part__} -# ${__url__}
                fi
            done
			cat db.part* | tar xvfzp -
            $(( counter++ ))
            if [ -e cvk6_2059.cnt ]; then
                rm db.part*
                break
            fi
        done
		set_param_in_conf "MetaCV" "db" ${__metacv_db}
        cd ${cwd}
    fi
    echo ""
}

download_is_incomplete() {
    # @USAGE: download_is_incomplete
    # @REQUIRES: $__url__
    file=${__url__##*/}
    if [[ "$(ls -l ${file} | awk '{ print $5 }')" -lt "$(curl -sI ${__url__} | awk '/Content-Length/ { print $2}')" ]]
    then
        return 0
    else
        return 1
    fi
}

install_r_pkgs() {
    # @REQUIRES $__pkgdir
	
    ## Bioconductor dependencies & devtools
    local bioc_pkgs="'BiocGenerics','IRanges','GenomicRanges','Biostrings','XVector','devtools'"
    local rmisc= rentrez= biofiles= blastr= ncbi=
    eval rmisc=( ${__pkgdir}/rmisc*gz ) 
    eval rentrez=( ${__pkgdir}/Rentrez*gz )
    eval biofiles=( ${__pkgdir}/biofiles*gz ) 
    eval blastr=( ${__pkgdir}/blastr*gz )
    eval ncbi=( ${__pkgdir}/ncbi*gz )
    
    R --quiet --no-save > /dev/null <<-RDOC
    is.installed <- function(pkg) is.element(pkg, .packages(TRUE))
    not.installed <- Negate(is.installed)
    "%&&%" <- function(condition, code) {
      if (condition) force(code) else invisible(TRUE)
    }
    bioc_install <- function(pkgs) {
      source("http://bioconductor.org/biocLite.R")
      library(BiocInstaller)
      try(useDevel(), silent=TRUE)
      sapply(pkgs, function(pkg) {
        not.installed(pkg) %&&% biocLite(pkg, suppressUpdates=TRUE)
        if (!is.installed(pkg))
          stop("Package ", pkg, " is not available for install.")
      })
      invisible()
    }
    cpp11 <- function(code) {
      Sys.setenv("PKG_CXXFLAGS"="-std=c++11")
      on.exit(Sys.setenv("PKG_CXXFLAGS"=""))
      force(code)
    }
    bioc_install(c(${bioc_pkgs}))
    not.installed("assertthat") %&&% devtools::install_github("assertthat", "hadley")
    not.installed("rmisc") %&&% cpp11(devtools::install_local("${rmisc}"))
    not.installed("rentrez") %&&% devtools::install_local("${rentrez}")
    not.installed("biofiles") %&&% devtools::install_local("${biofiles}")
    not.installed("blastr") %&&% devtools::install_local("${blastr}")
    not.installed("ncbi") %&&% cpp11(devtools::install_local("${ncbi}"))
RDOC

[ $? -eq 0 ] || die 1 "ERROR: Installation of requied R packages failed"

}

install_krona() {
    # @USAGE: install_krona

    local fetch=
    local cmdpath=
    check_dependency ktImportBLAST fetch cmdpath

    if [ "$fetch" == "y" ]; then

        local __taxon_db=${__db_dir}/taxonomy
        [ -e "${__taxon_db}" ] || mkdir -p ${__taxon_db}

        printf "Downloading KronaTools ...\n"
        curl -# -o ${__extdir}/${__krona_src} -L ${__krona_url}

        printf "Installing KronaTools ."
        tar -C ${__extdir} -xvf ${__extdir}/${__krona_src} > /dev/null
        printf "."
        [ -d "${__extdir}/krona" ] && rm -rf "${__extdir}/krona"
        mv -f ${__extdir}/Krona* ${__extdir}/krona
        printf "." 
        __cwd=$(pwd)
        cd ${__extdir}/krona
	    	# create a backup file
	    	cp updateTaxonomy.sh updateTaxonomy.sh.bak 
	    	# change the unzip command to leave the .gz files untouched for metaR taxonomy db
	    	sed -e 's/gunzip -f \$zipped/gunzip -c $zipped \> \$unzipped/g' updateTaxonomy.sh > updateTaxonomy.new
	    	# replace the original update file and make it accessable
	    	mv updateTaxonomy.new updateTaxonomy.sh && chmod 744 updateTaxonomy.sh
            ./install.pl --prefix ${__bindir%/bin*} --taxonomy ${__taxon_db} > /dev/null
            ## disable removing gi_taxid_nucl.dmp, gi_taxid_prot.dmp
            ## nodes.dmp, names.dmp so that we can reuse it for the ncbi pkg
            [ $? -eq 0 ] || die 1 "ERROR: Installation of KronaTools failed"
        cd ${__cwd}

        cmdpath=${__bindir}/       
    fi

    printf "."
    set_param_in_conf "Krona Tools" "path" ${cmdpath%/*}
    printf ". OK!\n\n"
}

get_taxonomy_db_metaR() {
    # @USAGE: get_taxonomy_db_metaR
    # @REQUIRES: $__db_dir

    local __taxon_db=${__db_dir}/taxonomy
    [ -e "${__taxon_db}" ] || mkdir -p ${__taxon_db}
	
    echo ""
    echo "**** metpipe requires the NCBI taxonomy files. ****"
    echo ""
    echo "You can also skip this step for now and generate the necessary database"
    echo "files in \"${__taxon_db}/\" at a later point by rerunning this script."
    echo ""
    echo "Skip? [Y|n] " | tr -d "\n"
    local skip=
    read skip
    eval skip=${skip:-y}
    if [ "$skip" != "n" -a "$skip" != "N" ]; then
        echo ""
        return 0
    else
        echo ""
        R --quiet --no-save > /dev/null <<-RDOC
		suppressPackageStartupMessages(require(rmisc))
        suppressPackageStartupMessages(require(ncbi))
        createTaxonDB('${__taxon_db}')
        createGeneidDB('${__taxon_db}')
RDOC
	set_param_in_conf "Taxonomical Annotation" "taxon_db" ${__taxon_db}
	set_param_in_conf "Subsetting of Database" "taxon_db" ${__taxon_db}
    fi
	
}

get_taxonomy_db_krona() {
    # @USAGE: get_taxonomy_db_krona PATH/TO/KRONA
    # @REQUIRES: $__db_dir

    local __taxon_db=${__db_dir}/taxonomy
    [ -e "${__taxon_db}" ] || mkdir -p ${__taxon_db}

    echo ""
    echo "**** Krona requires the NCBI taxonomy files. ****"
    echo ""
    echo "If you already have Krona installed on your system you should"
    echo "skip this step."
    echo ""
    echo "You can also skip this step for now and place the database files"
    echo "into \"${__taxon_db}/\" at a later point by rerunning this script."
    echo ""
    echo "Skip? [Y|n] " | tr -d "\n"
    local skip=
    read skip
    eval skip=${skip:-y}
    if [ "$skip" != "n" -a "$skip" != "N" ]; then
        echo ""
        return 0
    else
        local cwd=$(pwd)
        cd ${1}
        if [ -e "${__taxon_db}/gi_taxid.dat" ]; then
            echo ""
            echo "A taxonomy db already lives in \"${__taxon_db}\""
            echo ""
            echo "Do you want to update? [y|N]" | tr -d "\n"
            local update=
            read update
            if [ "$update" != "y" -o "$update" != "Y" ]; then
                echo ""
                return 0
            else
                echo ""
                ./updateTaxonomy.sh
            fi
        else
            echo ""
            ./updateTaxonomy.sh
        fi
        cd ${cwd}
    fi
    echo ""
}

#### BEGINNING OF MAIN ##############################################

while getopts h opt; do 
    case $opt in
        \?) echo "Invalid option: -$OPTARG\n"; exit 0;;
        h)  usage; exit 0;;
    esac
done

create_metpipe_dir
#install_fastqc
#install_fastx
#install_trimgalore
#install_flash
#install_blastparser
#install_velvet
#install_metavelvet
#install_blast
install_metacv
#install_krona
#get_taxonomy_db_krona "${__extdir}/krona"
#install_r_pkgs
#get_taxonomy_db_metaR 



exit 0

# --shell-- vim:set ft=sh:ai:et:sw=4:sts=4:

