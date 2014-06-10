class ReadAdf:
	def __init__(self,fname):
		self.fname = fname
		print "reading file: " + self.fname + "."
		filename = os.getcwd() + "/" + self.fname
		print "opening file: '" + filename + "'."
	def readfile(self):
		pass