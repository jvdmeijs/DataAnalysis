#!/bin/python
class State:
	def __init__(self,handler,statelist):
		self.handler = handler
		self.statelist = statelist
	def makestate(self):
		if self.handler == 'f':
			print "May the force be with you!"
		elif self.handler == 'p':
			print "You cannot be in two places at once, or so they want you to belive."
		else:
			quit("Wrong handler when calling on State-class.")