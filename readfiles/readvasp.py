import os
import re
class ReadVasp:
    """ A class that handles the 'vasp' output files"""
    def __init__(self,fname,handling = 7):
        """ Initialization of the class. Default settings"""
        self.fname = fname
        self.filename = os.getcwd() + "/" + self.fname
        self.handling = handling
        self.fline = []
        self.atomlist = []
        self.atomnumber = []
        self.numberofstates = []
        self.position = []
        self.force = []
    def readfile(self):
        """ Reading of the outfile."""
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
    def getdata(self):
        if (self.handling & 4) == 4:
            print "Getting atoms"
            self.getatoms()
            print "Atoms found!"
        # Fetching Lines where a new state begins:
        if ((self.handling & 2) == 2) or ((self.handling & 1) == 1):
            self.stateinfo = []
            self.numberofstates = []
            for i in xrange(0,len(self.fline)):
                if re.search(r"TOTAL-FORCE",self.fline[i],re.I):
                    self.numberofstates.append(i)
            if len(self.numberofstates) == 0:
                quit("No coordinates and forces found in file: '" + self.filename) + "'"
            for k in self.numberofstates:
                self.state = []
                for i in xrange(k+2,k+self.totalatoms+2):
                    self.state.append(self.fline[i])
                self.stateinfo.append(self.state)
        #Fetching information needed from the states:
        if (self.handling & 2) == 2:
            print "Getting coordinates"
            self.getcoordinates()
            print "Coordinates found!"
        if (self.handling & 1) == 1:
            print "Getting forces"
            self.getforce()
            print "Forces found!"
    def getatoms(self):
        """ Getting the list of atoms."""
        for i in self.fline:
            if re.search(r'poscar:',i,re.I):
                self.atomarray = i.replace("}","").split("{")
                break
        for k in self.atomarray:
                if re.search(r'VASPAtoms',k,re.I):
                    self.atoms = k.replace(" ","").replace("\n","").split(":")
        for m in xrange(0,len(self.atoms[1])):
            n = True
            last = True
            try:
                Foo = int(self.atoms[1][m]) #A tryout if the input is a integer
            except:
                n = False
            if m > 0:
                try:
                    Foo = int(self.atoms[1][m-1])
                except:
                    last = False
            if n == True:
                if last == True and m > 0 and len(self.atomnumber) > 0:
                    self.atomnumber[-1] = self.atomnumber[-1] * 10 + int(self.atoms[1][m])
                else:
                    self.atomnumber.append(int(self.atoms[1][m]))
            else:
                if last == False and m > 0 and len(self.atomlist) > 0:
                    self.atomlist[-1] = self.atomlist[-1] + self.atoms[1][m]
                else:
                    self.atomlist.append(str(self.atoms[1][m]))
        if len(self.atomlist) != len(self.atomnumber):
            quit("The number of atoms is inconsistend with the times each atom appears in the outfile.")
        self.totalatoms = 0
        for i in self.atomnumber:
            self.totalatoms += i
    def getcoordinates(self):
        """ Getting coordinates coronsponding with the atoms."""
        for state in self.stateinfo:
            self.stateposition = []
            for line in state:
                positionList = line.replace("      ", " ").replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").split(" ")
                self.positionOnly = [positionList[1], positionList[2], positionList[3]]
                self.stateposition.append(self.positionOnly)
            self.position.append(self.stateposition)

    def getforce(self):
        """ Fetching the forces coronsponding with the atoms."""
        for state in self.stateinfo:
            self.stateforce = []
            for line in state:
                forceList = line.replace("      ", " ").replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").split(" ")
                self.forceOnly = [forceList[4], forceList[5], forceList[6]]
                self.stateforce.append(self.forceOnly)
            self.force.append(self.stateforce) 
