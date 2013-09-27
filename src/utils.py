import os, sys
from src.exceptions import NoExecutable 
# utils.py contains various functions for simple testing purposes or conversion of 
# objects written here to clean up the code
# 
#@author:Philipp Sehnert
#@contact: philipp.sehnert[a]gmail.com

# convert the input to a string
def to_string(input):
    
    if len(input) > 1:
        return str(' '.join(str(i)for i in input))
    else:
        try:
            return str(input[0])
        except IndexError:
            return None

# test the input for fastq file extensions
def is_fastq(test_file):
    
    if  test_file.endswith(".fq") or test_file.endswith(".fastq"):
        return True
    else:
        return False

# make it sense?
def is_paired(input):
    
    if len(input) == 1:
        return False
    else:
        return True
       
# test the executable - is it existing and callable?
def is_executable(program_path):
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return True
        else:
            raise NoExecutable(program_path)
       

def is_xml(file):
    
    if to_string(file).endswith('.xml'):
        return True
    else:
        return False

def is_tabular(file):
    
    if to_string(file).endswith('.tab') or to_string(file).endswith('.tabular'):
        return True
    else:
        return False
    
def is_db(file):
    
    if to_string(file).endswith('.db'):
        return True
    else:
        return False
	
def blast_output(value):

    if int(value) == 5:
        return 'blastn.xml'
    elif int(value) == 6 or int(value) == 7:
        return 'blastn.tab'
    else:
        return 'blastn.blast'
    
def file_exists(file):
    
    if not os.path.isfile(file):
        
        sys.stdout.write("ERROR: %s could not be found" % (file))
        sys.exit()

        
        	

