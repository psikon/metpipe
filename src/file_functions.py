import os, sys
import glob
import shutil

# function to create a dir for the results of processing
def create_outputdir(path):
    
        try:
            os.makedirs(path)
        except OSError:
            # if dir exists and is dir go ahead
            if not os.path.isdir(path):
                raise
            
# copy number of files from source to destination
def move(src, dst, fileExtension):
    
    # generate list of files matching the file extension
    listofFiles = [f for f in os.listdir(src) if f.endswith(fileExtension)]
    for f in listofFiles:
        # if path exists remove it and overwrite results
        if os.path.exists(dst + os.sep + f):
            os.remove(dst + os.sep + f)
        shutil.move(src + f, dst)

# make it sense?
def is_paired(input):
    
    if len(input) == 1:
        return False
    else:
        return True
# convert the input to a string
def str_input(input):
    
    if len(input)>1:
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
def update_reads(directory, word, ending): 
   
   files = glob.glob1(directory, '*%s*.%s'%(word,ending))
   return [(directory + os.sep +  f) for f in files]

# test the executable - is it existing and callable?
def is_exe(program_path):
    
    return os.path.isfile(program_path) and os.access(program_path, os.X_OK)
        