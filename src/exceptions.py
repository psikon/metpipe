class ParameterFileNotFound(Exception):
    
    def __init__(self, args):
        self.args = args
        
class NoParameterSection(Exception):
        
    def __init__(self, args):
        self.args = args
