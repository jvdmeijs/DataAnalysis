#!/bin/python
class State:
	""" Obsolete class atm, however the point is to make sure that the data can be altered in this stage at some point."""
	def __init__(self, poslist, forcelist, stateid ,handler=None):
		self.handler = handler
		self.poslist = poslist
		self.forcelist = forcelist
		self.output = []
		self.type = None
		self.stateid = stateid
	def makestate(self):
		if self.handler == 'f':
			self.type = 'Force'
			for i in self.forcelist:
				self.output.append(i)
		elif self.handler == 'p':
			self.type = 'Position'
			for i in self.poslist:
				self.output.append(i)
		elif self.handler == 'c':
			self.type = 'Complete'
			for i in xrange(0,len(self.poslist)):
				posforce = []
				for k in xrange(0,7):
					if k < 4:
						posforce.append(self.poslist[i][k])
					else:
						posforce.append(self.forcelist[i][k-4])
				self.output.append(posforce)
		else:
			quit("Cannot assign type to state.")