import subprocess
import shlex
import sys, os
import shutil
import time
from src.utils import getDHMS, createOutputDir, ParamFileArguments, moveFile, logging, updateReads, convertInput
from src.settings import Settings, FastQC_Parameter, TrimGalore_Parameter


class Preprocess:
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def qualityCheck(self,outputdir):
        createOutputDir(Settings.output + os.sep + outputdir)
    
    def trim_and_filter(self,outputdir):
        pass