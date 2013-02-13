class Helper:
	
	def __init__(self,params):
		self.params = params
	
	def __del__(self):
		pass

	def checkParameter(self,item, value):
		import ConfigParser
		x = ConfigParser.ConfigParser()
		x.read(self.params)
		return x.get(item,value)
	
