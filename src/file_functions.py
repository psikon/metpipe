import os, sys
import glob
import shutil
import subprocess
import shlex
import sqlite3 as db
from src.settings import Executables
from src.exceptions import FastQConvertException

# file_functions.py contains all important file manipulation functions, needed 
# during the processing of the pipeline.
# 
#@author: Philipp Sehnert
#@contact: philipp.sehnert[a]gmail.com

def create_outputdir(path):
    '''create a dir for the results of processing'''
    try:
        os.makedirs(path)
    except OSError:
        # if dir exists and is dir go ahead
        if not os.path.isdir(path):
            raise

def update_reads(directory, word, extension): 
    '''traverse through a directory and filter out the new input for parameters''' 
    # find all files that fit in the given command
    files = glob.glob1(directory, '*%s*.%s' % (word, extension))
    # and return the files as list
    return [(directory + os.sep +  f) for f in files]

def merge_files(input, output, name, extension):
    '''combine the content of many files in one file'''
    try:
        # open file for merging
        merge = open(output + os.sep + name + '.' + extension, 'w')
        # copy all mergeable files in the file connection
        for i in range(len(input)):
            shutil.copyfileobj(open(input[i], 'rb'), merge)
        # close the file stream
        merge.close()
        return update_reads(output, name, extension)
   
    except IOError:
        print 'Error: '+ e.message

def convert_fastq(input, output, CONVERTER):
    '''convert fastq files to fasta'''
    
    for i in range(len(input)):
        p = subprocess.Popen(shlex.split('%s -n -Q33 -i %s -o %s' % 
                                        (CONVERTER,
                                         input[i],
                                         output + os.sep + 'converted.' 
                                         + str(i) + '.fasta')))
        p.wait()
        if p.returncode:
            raise FastQConvertException(input[i])
            
    return update_reads(output,'converted','fasta')

# simply delete file 
def remove_file(path, word, extension):
    
    # create a list of files fitting in the given command
    files = glob.glob1(path, '*%s*.%s'%(word,extension))
    # delete them all in a loop
    for i in range(len(files)):
        try: 
            os.remove(path + files[i])
        except IOError:
            print 'Error' + e.message
  
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

def absolute_path(file):
    tmp = []
    for i in range(len(file)):
        tmp.append(os.path.abspath(file[i]))
    
    return tmp
         
# create from the parsed blast database a file in blast tabular output to use the 
# krona import script for these type of file
def extract_tabular(location_of_db, destination):
    
    # open a file for writting
    output = open(destination + os.sep + 'extracted_from_DB.tab','w')
    # establish connection to the database
    con = db.connect(location_of_db)
    
    with con:
        # set the dictionary cursor for access the database tables by name
        con.row_factory = db.Row
        # create three cursors for the tables (q = query, h = hit and c = hsp)
        c = con.cursor()
        q = con.cursor()
        h = con.cursor()
        # get the whole content of the hsp table
        c.execute('Select * from hsp')
        # fetch all rows
        rows = c.fetchall()
        # iterate through the rows
        for row in rows:
            # get the missing values from the query table
            q.execute('Select query_def from query where query_id = ?', [row['query_id']])
            query_id = q.fetchone()[0].split(' ')[0]
            # get the missing values from the hit table
            h.execute('Select gene_id, accession from hit where hit_id = ?', [row['hit_id']])
            tmp = h.fetchone()
            subject_id= 'gi|%s|gb|%s|'% (tmp[0],tmp[1])
            # calculate the new values for tabular output
            perc = round((float(row['identity'])/float(row['align_len'])*100),2)
            mismatch = row['align_len'] - row['identity']
            # write line by line in the output file
            # 12 values tab seperated
            output.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s \n'% (query_id,
                                                          subject_id,
                                                          perc,
                                                          row['align_len'],
                                                          mismatch,
                                                          row['gaps'],
                                                          row['query_from'],
                                                          row['query_to'],
                                                          row['hit_from'],
                                                          row['hit_to'],
                                                          row['evalue'],
                                                          row['bit_score']))
            
        # after the last line close the db connections
        c.close()
        q.close()
        h.close()
        # close the file connection
        output.close()
            
           