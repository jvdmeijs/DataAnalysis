#!/bin/python
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
import atom
import vector
import element
import state
import readadf
import readvasp
import readqe
import readgaussian
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
        """ Providing the program with the correct handlers."""
        self.datareq = 0    # The variable that specifies the requested data.
                            # 000 => no data
                            # 100 => only atoms
                            # 010 => only positions
                            # 001 => only forces
                            # 110 => atoms and positions
                            # 101 => atoms and forces
                            # 011 => positions and forces
                            # 111 => all data
        for i in arguments:
            if self.readmode == 'filename':
                self.fname = i
                self.readmode = None
                continue
            elif i == '-h' or i == '-help':
                self.help()
                sys.exit()
            elif i == 'Excec.py':
                continue
            elif i == '-all' or i == '-a' or i == '':
                print "All data requested by user."
                self.datareq = 111
                continue
            elif i == '-e' or i == '-element':
                self.datareq += 100
                continue
            elif i == '-pos' or i == '-p':
                self.datareq += 10
                continue
            elif i == '-force' or i == '-f':
                self.datareq += 1
                continue
            elif i == '-n' or i == '-name':
                self.readmode = 'filename'
                continue
            else:
                self.help()
                sys.exit()
        if self.datareq >= 100:
            self.datareq = str(self.datareq)
        elif self.datareq == 10 or self.datareq == 11:
            self.datareq = '0' + str(self.datareq)
        else:
            self.datareq = '00' + str(self.datareq)
        if self.datareq not in ['000','100','010','001','110','101','011','111']:
            quit("Unexpected error in handeling given arguments. use '-h' or '-help' for more information")
    def help(self):
        """  A help function called by using help. """
        print "A short manual for the program:"
        print "You can request different types of data."
        print "Use '-a' or '-all' to get all data available."
        print "Use '-f' or '-force' to get all force data"
        print "Use '-p' or '-pos' to get position data"
        print "Use '-e' or '-element' to get the atoms as output."
        print "Further use:"
        print "Use '-n' or '-name' to specify a file name. Note that this argument is mandatory. Unless you use the '-h' or '-help' argument."
        print "After the '-n' or '-name' argument a filename must be given."
        print "Note that more than one handler can be used, with the exeption of -h' and '-help'. The '-a' and -'all' can only be used in comination with '-n' or '-name'."
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
        """ A function to write everythin to a external file.  """
        pass
class Parser:
    """ A general data parser."""
    atoms = []
    positions = []
    forces = []
    def __init__(self, atom, posx, posy, posz, fx, fy, fz):
        pass
    def organizedata(self, atom, posx, posy, posz, fx, fy, fz):
        """ A function to organize all the data available.  """
        pass

    def makedarray(self, atoms, positions, forces):
        """ A function to make the full array for all the data available.  """
        pass
class FileReader:
    """ Selecting the right type of method for reading the files
        given to the program.  """
    def __init__(self, fname):
        self.fname = fname
        self.type = None
        if self.fname == None:
            quit('No file name specified. use -h or -help for more information.')
        elif re.search(r'-',self.fname,re.I|re.M):
            quit("Argument specified instead of file name. Please make sure to specify the filename after the '-n' or '-name' argument.")
    def findtype(self):
        """ The function that determines the file type such as 
            Vasp, Gaussian, Quantum Esspresso or ADF."""
        cwd = os.getcwd()
        filename = cwd + '/' + self.fname
        try:
            f = open(filename,'r')
            f.close()
        except:
            quit('File not found, please make sure correct filename is given in arguments.')
        f = open(filename,'r')
        n = 0
        while n < 10:
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
                n = n + 1
                if self.type != None:
                    break
            n = n + 1
        f.close()
    def read(self):
        if self.type == None:
            quit("No filetype found in the file given to the program. Please make sure that your outputfile is supported. Use '-h' or '-help' to read the help manual. ")
        elif self.type == 'adf':
            readadf.ReadAdf(self.fname)
        elif self.type == 'vasp':
            readvasp.ReadVasp(self.fname)
        elif self.type == 'qe':
            readqe.ReadQe(self.fname)
        elif self.type == 'gaussian':
            readgaussian.ReadGaussian(self.fname)
        else:
            quit("Filetype handler not equal to known filetypes.")
def main(inarg):
    arguments = Arguments()
    arguments.readargument(inarg)      
    fileread = FileReader(arguments.fname)
    fileread.findtype()
    fileread.read()
main(sys.argv)