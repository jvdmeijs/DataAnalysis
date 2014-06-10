import os
class ReadVasp:
    """ A class that handles the 'vasp' output files"""
    def __init__(self,fname,handling = 7):
        """ Initialization of the class. Default settings"""
        self.fname = fname
        self.filename = os.getcwd() + "/" + self.fname
        self.handling = handling
    def readfile(self):
        """ Reading of the outfile."""
        self.fline = []
        try:
            f = open(self.filename,'r')
            f.close()
        except:
            quit("File: '" + self.filename +"' not found! Please make sure it is in the correct directory.")
        print "Opening file '" + self.filename +"'."
        f = open(self.filename,'r')
        for i in f.readlines():
            self.fline.append(i)
        print "Closing file '" + self.filename +"'."
        f.close()
        fline = self.fline
    def getdata(self):
        if (self.handling & 4) == 4:
            print "Getting atoms"
            self.getatoms()
        if (self.handling & 2) == 2:
            print "getting positions"
            self.getcoordinates()
        if (self.handling & 1) == 1:
            print "getting forces"
            self.getforce()
    def getatoms(self):
        """ Getting the list of atoms."""
        pass
    def getcoordinates(self):
        """ Getting coordinates coronsponding with the atoms."""
        pass
    def getforce(self):
        """ Fetching the forces coronsponding with the atoms."""
        pass