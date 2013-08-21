import subprocess
import shlex
import sys, os
import shutil
import time
from src.utils import getDHMS, createOutputDir, ParamFileArguments, moveFile, logging, updateReads, convertInput
from src.settings import Settings, FLASH_Parameter, Velveth_Paramater, Velevtg_Parameter, MetaVelvet_Parameter