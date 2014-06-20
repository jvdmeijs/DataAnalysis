#!/usr/bin/env python
""" Importing the scrips necessary for the program.  """
import os
import re
import sys
import inspect
""" Parsing subdirs to sys.path. """
for subfolder in ['Atom','Element','State','readfiles']:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],subfolder)))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
""" Importing custom classes"""
from atom import Atom
from vector import Vector
from element import Element
from state import State
from readadf import ReadAdf
from readvasp import ReadVasp
from readqe import ReadQe
from readgaussian import ReadGaussian
""" The beginning of the program. """
class Arguments:
    """ Defines the general behaviour of the program. """
    def __init__(self): #,arguments):
        """ Default settings."""
        #self.arguments = arguments
        self.datareq = '000'
        self.readmode = None
        self.fname = None
    def readargument(self,arguments):
        """ Provide the program with the correct handlers."""
        self.datareq = int('000',2)         # 111 = 7 gives all data
                                            # 000 = 0 gives no data
                                            # 001 = 1 gives forces
                                            # 010 = 2 gives coordinates
                                            # 100 = 4 gives atoms
                                            # a sum of the bits gives both the attributes.
        for i in arguments:
            if self.readmode == 'filename':
                self.fname = i
                self.readmode = None
                continue
            elif i == '-h' or i == '--help':
                self.help()
                sys.exit()
            elif i == 'Excec.py':
                continue
            elif i == '--all' or i == '-a' or i == '':
                print "All data requested by user."
                self.datareq = self.datareq | int('111',2)
                continue
            elif i == '-e' or i == '--element':
                self.datareq = self.datareq | int('100',2)
                print "Elemental data requested by user."
                continue
            elif i == '--pos' or i == '--p':
                self.datareq = self.datareq | int('10',2)
                print "Positional data requested by user."
                continue
            elif i == '--force' or i == '-f':
                self.datareq = self.datareq | int('1',2)
                print "Forces requested by user."
                continue
            elif i == '-n' or i == '--name':
                self.readmode = 'filename'
                continue
            else:
                self.help()
                sys.exit()
    def help(self):
        """  A help function called by using help. """
        print "A short manual for the program:"
        print "You can request different types of data."
        print "Use '-a' or '--all' to get all data available."
        print "Use '-f' or '--force' to get all force data"
        print "Use '-p' or '--pos' to get position data"
        print "Use '-e' or '--element' to get the atoms as output."
        print "Further use:"
        print "Use '-n' or '--name' to specify a file name. Note that this argument is mandatory. Unless you use the '-h' or '--help' argument."
        print "After the '-n' or '--name' argument a filename must be given."
        print "Note that more than one handler can be used, with the exeption of -h' and '--help'. The '-a' and '--all' can only be used in comination with '-n' or '--name'."
        print "So if you for example want to request the positions and forces on the file 'out' use: ' -p -f -n out'."
        print "The supported files are at this moment: Vasp, Quantum Esspresso, Gaussian and ADF."
class Output:
    """ This class creates a structurized file using all data available. 
    Using the general structure: atom, positions (posx posy posz),
    force (posx posy posz).  """
    def __init__(self, cwd, filename, darray):
        self.cwd = cwd
        self.filename = filename
        self.darray = darray
    def writefile(self, filename, darray): 
        """ Write everything to a external file.  """
        pass
class Parser:
    """ A general data parser."""
    def __init__(self, atoms = [], atomnumbers = [], pos = [], force = [],handler = 7):
        self.atoms = atoms
        self.atomnumbers = atomnumbers
        self.pos = pos
        self.force = force
        self.handler = handler
        self.atomlist = []
        self.atominstance = []
        self.state = 0
    def data(self):
        """ Input for raw data."""
        if (self.handler & 2) == 2 or (self.handler & 1) == 1:
            if (len(self.pos) != len(self.force)) and len(self.pos) != 0  and len(self.force) != 0:
                quit("The number of states cannot be determained. The forces and positions do not match!")
            if len(self.pos)>0:
                self.state = len(self.pos)
            else:
                self.state = len(self.force)
            if self.state <= 0:
                quit('No states found! There should be atleast one state. Please make sure output is correct!')
        if (self.handler & 4) == 4: #Atom data requested.
            print "Parsing atomic data."
            for i in xrange(0,len(self.atomnumbers)):
                n = 0
                while n < self.atomnumbers[i]:
                    self.atomlist.append(self.atoms[i]+str(n+1))
                    n += 1
            for i in xrange(0,len(self.atomlist)):
                foo = self.atomlist[i]
                self.atomlist[i] = Atom(foo)
                self.atomlist[i].makeatom()
            print "Parsing Completed"
        if (self.handler & 2) == 2: #position data requested.
            print "Parsing coordinates."
            for statenr in xrange(0,self.state):
                print "NEW STATE: " + str(statenr+1)
                for atomnr in xrange(0,len(self.pos[statenr])):
                    for coorid in xrange(0,len(self.pos[statenr][atomnr])):
                        if coorid == 2:
                            foo = self.pos[statenr][atomnr][coorid].replace('\n','').replace('\r','')
                            self.pos[statenr][atomnr][coorid] = foo
                    self.pos[statenr][atomnr].insert(0,atomnr)
                self.pos[statenr] = State('p',self.pos[statenr])
            print "Parsing completed."
        if (self.handler & 1) == 1: #Force data reqested.
            print "Parsing Forces."
            for statenr in xrange(0,self.state):
                print "NEW STATE: " + str(statenr+1)
                for atomnr in xrange(0,len(self.force[statenr])):
                    for coorid in xrange(0,len(self.force[statenr][atomnr])):
                        if coorid == 2:
                            foo = self.force[statenr][atomnr][coorid].replace('\n','').replace('\r','')
                            self.force[statenr][atomnr][coorid] = foo
                    self.force[statenr][atomnr].insert(0,atomnr)
                self.force[statenr] = State('f',self.force[statenr])
            print "Parsing Completed."
    def organizedata(self):
        """ Organize all the data available and requested.  """
        pass
    def makedarray(self):
        """ Make the array of all data available and requested. """
        pass
class FileReader:
    """ Selecting the right type of method for reading the files
        given to the program.  """
    def __init__(self, fname,handler = 7):
        self.fname = fname
        self.type = None
        self.handler = handler
        if self.fname == None:
            quit('No file name specified. use -h or -help for more information.')
        elif re.search(r'-',self.fname,re.I|re.M):
            quit("Argument specified instead of file name. Please make sure to specify the filename after the '-n' or '-name' argument.")
    def findtype(self):
        """ Find out which filetype the output file is, i.e.
            Vasp, Gaussian, Quantum Esspresso or ADF."""
        cwd = os.getcwd()
        filename = cwd + '/' + self.fname
        try:
            f = open(filename,'r')
            f.close()
        except:
            quit('File not found, please make sure correct filename is given in arguments.')
        f = open(filename,'r')
        for i in f.readlines():
            if re.search(r'vasp',i,re.I):
                self.type = 'vasp'
                print 'File identified as Vasp file.'
                break
            elif re.search(r'adf',i,re.I):
                self.type = 'adf'
                print 'File identified as ADF file.'
                break
            elif re.search(r'qe',i,re.I) or re.search(r'Quantum Esspresso',i,re.I):
                self.type = 'qe'
                print 'File identified as QE file.'
                break
            elif re.search(r'gaussian',i,re.I):
                self.type = 'gaussian'
                print 'File identified as Gaussian file.'
                break
            if self.type != None:
                break
        f.close()
    def read(self):
        if self.type == None:
            quit("No filetype found in the file given to the program. Please make sure that your outputfile is supported. Use '-h' or '-help' to read the help manual. ")
        elif self.type == 'adf':
            self.reader = ReadAdf(self.fname ,self.handler)
        elif self.type == 'vasp':
            self.reader = ReadVasp(self.fname ,self.handler)
        elif self.type == 'qe':
            self.reader = ReadQe(self.fname ,self.handler)
        elif self.type == 'gaussian':
            self.reader = ReadGaussian(self.fname ,self.handler)
        else:
            quit("Filetype handler not equal to known filetypes.")
        self.reader.readfile()

def main(inarg):
    arguments = Arguments()
    arguments.readargument(inarg)     
    fileread = FileReader(arguments.fname, int(arguments.datareq))
    fileread.findtype()
    fileread.read()
    rawdata = fileread.reader
    rawdata.getdata()
    print "Total number of atoms: " + str(rawdata.totalatoms)
    if(len(rawdata.numberofstates)>0):print "Total number of states requested: " + str(len(rawdata.numberofstates))
    parser = Parser(rawdata.atomlist, rawdata.atomnumber, rawdata.position, rawdata.force,int(arguments.datareq))
    parser.data()
    print parser.pos[1]
main(sys.argv)