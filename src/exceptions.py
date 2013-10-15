import sys, os
from src.settings import FileSettings

# General Exceptions

class InputNotFound(Exception):
    
    def __init__(self, args):
        sys.stderr.write('ERROR 2: Input file(s) could not be found!\n')
        sys.stderr.write('Please check path for:\n%s\n\n' % (args))
        sys.exit(1)

class ParamFileNotFound(Exception):
    
    def __init__(self, args):
        sys.stderr.write('ERROR 4: Parameter File could not be found!\n')
        sys.stderr.write('Please check path for:\n%s\n\n' % (args))
        sys.exit(1)
  
class NoExecutable(Exception):
    
    def __init__(self, args):
        sys.stderr.write('ERROR 5: No Executable found!') 
        sys.stderr.write('Please check path in parameter file:\n%s\n'
                         % (args))
        sys.exit(1)

class DBNotFound(Exception):
    
    def __init__(self, args):
        sys.stderr.write('ERROR 6: Database for %s cold not be found!') 
        sys.stderr.write('Please check rerun the install-script or\n copy database files to db dir')
        sys.exit(1)

# Preprocess Exceptions

class FastQException(Exception):
    
    def __init__(self, args):
        sys.stdout.write('ERROR 9: Input File not in FASTQ Format!:\n%s\n'
                         % (args))
        sys.stdout.write('Quality Information is needed for Preprocessing!\n\n')
        
class FastQCException(Exception):
    
    def __init__(self):
        sys.stderr.write('ERROR 10: Error during Quality Analysis with FastQC!\n')
        sys.stderr.write('Please check the parameter file!\n\n')
        sys.stderr.write('Skip Quality Analysis')

class TrimGaloreException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 11: Error during Trimming Process with TrimGalore!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)            
    
# Assembly Exceptions
        
class FlashException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 12: Error during Concatination of Reads with Flash!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
        
class VelvetHException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 13: Error while Creating Hashmaps with Velveth!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
        
class VelvetGException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 14: Error during Graph Construction with Velvetg!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     

class MetaVelvetException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 15: Error during Assembly with MetaVelvet!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)

# Annotation Exceptions

class FastQConvertException(Exception):
    
    def __init__(self, args):
        sys.stderr.write('ERROR 16: Error during FastQ to Fasta Conversion\n')
        sys.stderr.write('Cannot convert file:\n%s\n\n' % (args))
        sys.exit(1)  
    
class BlastnException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 17: Error during Annotation with Blastn!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
          
class MetaCVException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 18: Error during Annotation with MetaCV!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
        
class MetaCVSumException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 19: Error during Analysis of MetaCV results!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
            
# Analysis Exceptions 
       
class ParserException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 20: Error during Parsing the Blast XML File!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
        
class AnnotateDBException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 21: Error during Annotation of the database!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     
        
class SubsetDBException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 22: Error during Subsetting of the database!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1)     

class KronaException(Exception):
    
    def __init__(self, args): 
        sys.stderr.write('ERROR 22: Error during Creation of Pie chart with Krona Webtools!\n')
        sys.stderr.write('Please check error log:\n%s\n\n' % (args))
        sys.exit(1) 
        
class KronaFormatException(Exception):
    
    def __init__(self):
        sys.stderr.write('ERROR 23: Input must be in Blast table or XML format! \n')                     
        sys.stderr.write('change Blast Parameter "outfmt" to 5 or 6')
        sys.exit(1)

