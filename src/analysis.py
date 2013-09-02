# standard imports
import subprocess
import shlex
import sys, os
import shutil
import time
# imports of own functions and classes
from src.utils import ParamFileArguments
from src.settings import Settings, Executables, Blastn_Parameter, MetaCV_Parameter
from src.file_functions import create_outputdir, str_input, is_paired, is_fastq, update_reads, is_exe
from src.log_functions import Logging

class Analysis:
    
    def __init__(self, input, blast_out, metacv_out, krona):
        pass
    
    def __del__(self):
        pass
        