import os
class ReadVasp:
    """ A class that handles the 'vasp' output files"""
    def __init__(self,fname,handling = '111'):
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
        #return self.fline
    def getdata(self):
        for i in xrange(0,self.handling):
            if i == 0 and self.handling[i] == '1':
                atoms = self.getatoms()
                continue
            elif i == 1 and self.handling[i] == '1':
                coor = self.getcoordinates()
                continue
            elif i == 2 and self.handling[i] == '1':
                forces = self.getforce()
                continue
    def getatoms(self):
        """ Getting the list of atoms, if the first argument of the handling is 1."""
        pass
    def getcoordinates(self):
        """ Getting coordinates coronsponding with the atoms, if the second argument of the handling is 1."""
        pass
    def getforce(self):
        """ Fetching the forces coronsponding with the atoms, id the third argument of the handling is 1."""
        pass