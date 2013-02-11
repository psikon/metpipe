class helper:
	
	def __init__(self,path):
		self.path =path
	
	def __del__(self):
		pass

	def readParameter(self):
		import ConfigParser
		parameter = ConfigParser.ConfigParser()
		parameter.read(self.path)
		assembly = parameter.get("Assembly","program")
		annotate = parameter.items("Annotate")
		print assembly
		print annotate
	

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False
