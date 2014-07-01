#!/usr/bin/env python
""" Importing the scrips necessary for the program.  """
import os
import re
import sys
import inspect
import cPickle
import datetime
""" Parsing subdirs to sys.path. """
for subfolder in ['Atom','State','readfiles']:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],subfolder)))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
""" Importing custom classes"""
from atom import Atom
from vector import Vector
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
        self.mergename = None
        self.merge = None
    def readargument(self,arguments):
        """ Provide the program with the correct handlers."""
        self.datareq = int('000',2)         # 1111 = 7 gives all data
                                            # 0000 = 0 gives no data
                                            # 0001 = 1 gives forces
                                            # 0010 = 2 gives coordinates
                                            # 0100 = 4 gives atoms
                                            # 1000 = 8 gives lattice vectors
                                            # a sum of the bits gives both the attributes.
        for i in arguments[1:]:
            if self.readmode == 'filename':
                self.fname = i
                self.readmode = None
                continue
            elif self.readmode == 'merge':
                self.mergename = i
                self.readmode = None
                continue
            elif i == '-h' or i == '--help':
                self.help()
                sys.exit()
            elif i == '--all' or i == '-a' or i == '':
                self.datareq = self.datareq | int('1111',2)
                continue
            elif i == '-e' or i == '--element':
                self.datareq = self.datareq | int('100',2)
                continue
            elif i == '--pos' or i == '-p':
                self.datareq = self.datareq | int('10',2)
                continue
            elif i == '--force' or i == '-f':
                self.datareq = self.datareq | int('1',2)
                continue
            elif i == '-l' or i == '--latice':
                self.datareq = self.datareq | int('1000',2)
                continue
            elif i == '-n' or i == '--name':
                self.readmode = 'filename'
                continue
            elif i == '-m' or i == '--merge':
                self.readmode = 'merge'
                self.merge = 1
                continue
            elif i == '-c' or i == '--clean':
                self.merge = 0
                continue
            else:
                print "Argument '"+i+ "' not a valid argument."
                print
                print "Here is the help function [--help]"
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
        print "The supported file types are at this moment: Vasp."# , Quantum Esspresso, Gaussian and ADF."
        print "This program can produce clean oufiles with the '-c' '--clean' argument,"
        print "or it can merge the data with another outfile produced by this program by using '-m [FILENAME]' or '--merge [FILENAME]'."
        print "The default settings for this specific setting is: 'clean', so be sure to rename your file to prevent data loss."
class Output:
    """ This class creates a structurized file using all data available. 
    Using the general structure: atom, positions (posx posy posz),
    force (posx posy posz).  """
    def __init__(self, handler, darray, filename = None):
        self.handler = handler
        self.filename = filename
        self.darray = darray
    def writefile(self): 
        """ Write everything to a external file.  """
        if self.handler == 1 and self.filename != None:
            print "Merging the files."
            self.mergefile()
        else:
            print "Generating a clean file."
        date = str(datetime.datetime.now()).replace(':','').replace(' ','').replace('-','').replace('.','')
        allavaildata = cPickle.dumps(self.darray)
        picklename = 'PickledFileOutput' + date
        fileloc = os.getcwd()+'/'+picklename
        print "Writing all class data."
        f = open(fileloc,'w+')
        f.write(allavaildata)
        f.close
        print "All class data is written to: "+ fileloc
        filename = os.getcwd() + '/state_output' + date
        avail = [False,False,False]
        if self.darray[0] != 0:
            avail[0] = True
        if self.darray[1] != 0:
            avail[1] = True
        if self.darray[2] != 0:
            avail[2] = True
        print "Writing all data to hrf:"
        f = open(filename,'w+')
        if avail[0] == True:
            for i in xrange(0,len(self.darray[0])):
                line = str(int(self.darray[0][i].id))+' '+str(self.darray[0][i].atomname)+' '+str(self.darray[0][i].fullname)+' '+str(self.darray[0][i].atomprotons) + '\n'
                if i == 0:
                    f.write("Atoms:\n")
                f.write(line)
        if avail[1] == True:
            for state in xrange(0,len(self.darray[1])):
                if state == 0:
                    f.write('States:\n')
                f.write('State: '+str(state)+'\n')
                for atom in xrange(0,len(self.darray[1][state].output)):
                    line = ''
                    for iden in xrange(0,len(self.darray[1][state].output[atom])):
                        if iden == 0:
                            atomname = str()
                            for at in self.darray[0]:
                                if int(at.id) == int(self.darray[1][state].output[atom][iden]):
                                    atomname = at.atomname
                            line  = line + atomname + ' '
                        else:
                            line = line + str(self.darray[1][state].output[atom][iden]) + ' '
                    f.write(line + '\n')
                if avail[2] == True:
                    n = 0
                    line = ''
                    while n<3:
                        line  = line  + self.darray[2][state][n] + '\n'
                        n += 1
                    f.write(line)
        f.close()
        print "All data written to: " + filename
    def mergefile(self):
        print "Opening Pickled file."
        try:
            f = open(os.getcwd()+"/"+self.filename,'r')
            f.close()
        except:
            quit("Pickled filename incorrect, please try again and make sure the filename is correct.")
        f = open(os.getcwd()+'/'+self.filename)
        olddata = cPickle.load(f)
        f.close()
        print "Closing Pickled file."
        print "Combining all data."
        nratoms = len(olddata[0])
        nrstates = len(olddata[1])
        for atoms in self.darray[0]:
            atoms.id = atoms.id + nratoms
        for states in self.darray[1]:
            for atom in states.output:
                atom[0] = atom[0] + nratoms
            states.stateid = states.stateid +  nrstates
        self.darray[0] = olddata[0] + self.darray[0]
        self.darray[1] = olddata[1] + self.darray[1]
        self.darray[2] = olddata[2] + self.darray[2]
        print "All data combined."
class Parser:
    """ A general data parser."""
    def __init__(self, atoms = [], atomnumbers = [], pos = [], force = [], lattice = [], handler = 7):
        self.atoms = atoms
        self.atomnumbers = atomnumbers
        self.pos = pos
        self.force = force
        self.handler = handler
        self.lattice = lattice
        self.atomlist = []
        self.atominstance = []
        self.states = []
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
            aid = 0
            for i in xrange(0,len(self.atomnumbers)):
                n = 0
                while n < self.atomnumbers[i]:
                    self.atomlist.append(self.atoms[i]+str(aid))
                    n += 1
                    aid += 1
            for i in xrange(0,len(self.atomlist)):
                foo = self.atomlist[i]
                self.atomlist[i] = Atom(foo)
                self.atomlist[i].makeatom()
            print "Parsing Completed"
        if (self.handler & 2) == 2 and (self.handler & 1) != 1: #position data requested.
            print "Parsing coordinates."
            for statenr in xrange(0,self.state):
                for atomnr in xrange(0,len(self.pos[statenr])):
                    for coorid in xrange(0,len(self.pos[statenr][atomnr])):
                        if coorid == 2:
                            foo = self.pos[statenr][atomnr][coorid].replace('\n','').replace('\r','')
                            self.pos[statenr][atomnr][coorid] = foo
                    self.pos[statenr][atomnr].insert(0,atomnr)
                foo = self.pos[statenr]
                self.pos[statenr] = State(foo,None,statenr,'p')
                self.pos[statenr].makestate()
                self.states = self.pos
            print "Parsing completed."
        if (self.handler & 1) == 1 and (self.handler & 2) != 2: #Force data reqested.
            print "Parsing Forces."
            for statenr in xrange(0,self.state):
                for atomnr in xrange(0,len(self.force[statenr])):
                    for coorid in xrange(0,len(self.force[statenr][atomnr])):
                        if coorid == 2:
                            foo = self.force[statenr][atomnr][coorid].replace('\n','').replace('\r','')
                            self.force[statenr][atomnr][coorid] = foo
                    self.force[statenr][atomnr].insert(0,atomnr)
                foo = self.force[statenr]
                self.force[statenr] = State(None,foo,statenr,'f')
                self.force[statenr].makestate()
                self.states = self.force
            print "Parsing Completed."
        if (self.handler & 2) == 2 and (self.handler & 1) == 1:
            print "Parsing complete states:"
            for statenr in xrange(0,self.state):
                for atomnr in xrange(0,len(self.force[statenr])):
                    for coorid in xrange(0,len(self.force[statenr][atomnr])):
                        if coorid == 2:
                            foo = self.force[statenr][atomnr][coorid].replace('\n','').replace('\r','')
                            self.force[statenr][atomnr][coorid] = foo
                            fooo = self.pos[statenr][atomnr][coorid].replace('\n','').replace('\r','')
                            self.pos[statenr][atomnr][coorid] = fooo
                    self.pos[statenr][atomnr].insert(0,atomnr)
                self.states.append(State(self.pos[statenr],self.force[statenr],statenr,'c'))
                self.states[-1].makestate()
            print "Parsing Completed."
        if (self.handler & 8 ) == 8 and len(self.lattice) != 0:
            print "Parsing Lattice parameters:"
            self.lattice_list = Vector(self.lattice)
            print "Parsing Lattice parameters completed."
    def makedarray(self):
        self.darray = []
        if len(self.atomlist)>0:
            self.darray.append(self.atomlist)
        else:
            self.darray.append(0)
        if len(self.states)>0:
            self.darray.append(self.states)
        else:
            self.darray.append(0)
        if len(self.lattice_list.lattice)>0:
            self.darray.append(self.lattice_list.lattice)
        else:
            self.darray.append(0)
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
    if rawdata.totalatoms>0:
        print "Total number of atoms: " + str(rawdata.totalatoms)
    if(len(rawdata.numberofstates)>0):print "Total number of states requested: " + str(len(rawdata.numberofstates))
    parser = Parser(rawdata.atomlist, rawdata.atomnumber, rawdata.position, rawdata.force,rawdata.lattice,int(arguments.datareq))
    parser.data()
    parser.makedarray()
    alldata = parser.darray
    output = Output(arguments.merge, alldata, arguments.mergename)
    output.writefile()
main(sys.argv)