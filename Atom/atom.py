class Vector:
	def __init__(self,xx,yy,zz):
		pass
class Atom:
	" Defines an atom."
	def __init__(self, name = 'H', weight = float(1), protons = 1):
		self.atomname = name
		self.atomweight = weight
		self.atomprotons = protons