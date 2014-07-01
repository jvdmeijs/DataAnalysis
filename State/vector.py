class Vector:
	def __init__(self,lattice):
		""" A class to do calculations on the lattice vectors if needed. Obsolete at the moment."""
		self.lattice = lattice
		self.states = len(lattice)