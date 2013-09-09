import os, sys
import glob
import shutil
import subprocess
import shlex
from src.settings import Executables

# function to create a dir for the results of processing
def create_outputdir(path):
    
        try:
            os.makedirs(path)
        except OSError:
            # if dir exists and is dir go ahead
            if not os.path.isdir(path):
                raise

# make it sense?
def is_paired(input):
    
    if len(input) == 1:
        return False
    else:
        return True
    
# convert the input to a string
def str_input(input):
    
    if len(input) > 1:
        return str(' '.join(str(i)for i in input))
    else:
        return str(input[0])

# test the input for fastq-fileextensions
def is_fastq(test_file):
    
    if  test_file.endswith(".fq") or test_file.endswith(".fastq"):
        return True
    else:
        return False

# traverse through the given directory and filter out the new input 
#for given parameters
def update_reads(directory, word, extension): 
   
   files = glob.glob1(directory, '*%s*.%s' % (word, extension))
   return [(directory + os.sep +  f) for f in files]

# test the executable - is it existing and callable?
def is_executable(program_path):
    if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
        return True
    else: 
        sys.stdout.write(os.linesep)
        sys.stderr.write('Executable for ' + program_path.split(os.sep)[-1] + ' not found - Please reinstall\n')
        sys.stdout.write(os.linesep)
        return False

def merge_files(input, output):
    merge = open(output + os.sep + 'merged.fasta','w')
    for i in range(len(input)):
        shutil.copyfileobj(open(input[i],'rb'),merge)
    merge.close()
    return update_reads(output,'merged','fasta')
    
def convert_fastq(input, output, CONVERTER):
    
    for i in range(len(input)):
        p = subprocess.Popen(shlex.split('%s -n -Q33 -i %s -o %s' % (CONVERTER,
                                                                     input[i],
                                                                     output + os.sep + 
                                                                     'converted.' + str(i) + 
                                                                     '.fasta')))
        p.wait()
    return update_reads(output,'converted','fasta')

def remove_file(path, word, extension):
    files = glob.glob1(path, '*%s*.%s'%(word,extension))
    for i in range(len(files)):
        os.remove(path + files[i])
    
def blast_output(value):
    
    if value is str(5):
        return 'blastn.xml'
    elif value is str(6) or str(7):
        return 'blastn.tab'
    else:
        return 'blastn.blast'

def is_xml(file):
    
    if file.endswith('.xml'):
        return True
    else:
        return False
    
# important function to get all used arguments from a settings object and convert it to an argument string
def parse_parameter(instance):

    args = ''
    # get all used vars of the instance
    var = vars(instance)
    for name in var:
        # if var is boolean and true only print the name of the var in dict
        if getattr(instance, name):
            if str(getattr(instance, name)).lower() in 'true':
                args += ' ' + instance.arguments.get(str(name))
            # if var is boolean and false discard it
            elif str(getattr(instance, name)).lower() in 'false':
                pass
            # else var has a value - print var from dict + value
            else: 
                args += ' ' + instance.arguments.get(str(name)) + getattr(instance, name)
    
    return args