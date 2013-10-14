import os, sys
from src.exceptions import NoExecutable, FastQException
# utils.py contains various functions for simple testing purposes or conversion of 
# objects written here to clean up the code
# 
#@author:Philipp Sehnert
#@contact: philipp.sehnert[a]gmail.com

# convert the input to a string
def to_string(value):
    
    if len(value) > 1:
        return str(' '.join(str(i)for i in value))
    else:
        try:
            return str(value[0])
        except IndexError:
            return None

# test the input for fastq file extensions
def is_fastq(file):
    
    if all(i.endswith('.fastq') for i in file ):
        return True
    else:
        raise FastQException(file)

# make it sense?
def is_paired(file):
    
    if len(file) == 1:
        return False
    else:
        return True
       
# test the executable - is it existing and callable?
def is_executable(path):
    
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return True
        else:
            raise NoExecutable(path)
       

def is_xml(file):
    
    if file.endswith('.xml') or file.endswith('.XML'):
        return True
    else:
        return False

def is_tabular(file):
    
    if file.endswith('.tab') or file.endswith('.tabular'):
        return True
    else:
        return False
    
def is_db(file):
    
    if to_string(file).endswith('.db') or to_string(file).endswith('.sql'):
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

      
        	

