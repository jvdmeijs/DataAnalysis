#!/bin/python
class Element:
	def __init__(self,symbol):
		self.symbol = symbol
		file_name = getcwd().elements.txt
		f = open(file_name,'r')
		for i in f.readlines():
			pass