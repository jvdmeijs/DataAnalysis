import os
class Atom:
	" Defines an atom."
	def __init__(self, name = 'H', fullname = '' , weight = float(1), protons = 1):
		self.atomname = name
		self.atomweight = weight
		self.atomprotons = protons
		self.fullname = fullname
		self.periodictable = []
		path = os.path.abspath(os.path.dirname(__file__))
		try:
			f = open(path+'/elements.txt','r')
			f.close()
		except:
			quit("Could not find elemental data file, please check the atom directory and make sure 'elements.txt' is located here!")
		f = open(path+'/elements.txt','r')
		for i in f.readlines():
			element = i.split("|")
			del element[-1]
			self.periodictable.append(element)
		f.close()
		elementname = ''
		for i in self.atomname:
			isstr = False
			try:
				foo = int(i)
			except:
				isstr = True
			if isstr == True:
				elementname = elementname + i
		self.atomname = elementname
	def makeatom(self):
		self.found = False
		for i in self.periodictable:
			if i[1] == self.atomname:
				self.found = True
				self.atomprotons = int(i[2])
				self.fullname = i[0]
				break
		if self.found == False:
			quit("Element not found!, please make sure the elemental data file is located in the Atom directory of the program")