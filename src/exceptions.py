from src.utils import to_string
from src.settings import General

class ParameterFileNotFound(Exception):
    
    def __init__(self, args):
        self.args = args
        
class NoParameterSection(Exception):
        
    def __init__(self, args):
        self.args = args
