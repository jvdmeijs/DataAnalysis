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
        f = open(self.filename,'r')
        for i in f.readlines():
            self.fline.append(i)
        f.close()
    def getdata(self):
        if (self.handling & 4) == 4:
            self.getatoms()
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
            self.getcoordinates()
        if (self.handling & 1) == 1:
            self.getforce()
        if (self.handling & 8) == 8:
            self.getlattice()
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
    def getlattice(self):
        """ Fetching the lattice vectors for each state."""
        self.lattice = []
        for k in xrange(0,len(self.fline)):
            a = 'a'
            b = 'b'
            c = 'c'
            latticelist = [a,b,c]
            if re.search(r'direct lattice vectors',self.fline[k],re.I|re.M) and re.search('VOLUME',self.fline[k-4],re.I|re.M):
                a = self.fline[k+1].split()
                b = self.fline[k+2].split()
                c = self.fline[k+3].split()
                a = a[0] + ' ' + a[1] + ' ' + a[2]
                b = b[0] + ' ' + b[1] + ' ' + b[2]
                c = c[0] + ' ' + c[1] + ' ' + c[2]
                latticelist = [a,b,c]
            if latticelist != ['a','b','c']:
                self.lattice.append(latticelist)