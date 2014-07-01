Data Analysis
=============

A program for RDFX data analysis using python.
This program is a quick way to generate a trajectory file from a output.

The supported input files at this moment are:
-Vasp
Output files that the support will be build for in the future:
-ADF
-QE
-Gaussian

The output file from the program looks like this (general structure)

>Atoms:
>0  X  Fullname AtomNumber
>1  X  Fullname AtomNumber
>.. .. ..       ..
>n  Y  Fullname AtomNumber
>States:
>State 0
>X	positions (x,y,z) forces (x,y,z)
>X	positions (x,y,z) forces (x,y,z)
>..	..                ..
>Y	positions (x,y,z) forces (x,y,z)
>State 1
>X	positions (x,y,z) forces (x,y,z)
>X	positions (x,y,z) forces (x,y,z)
>..	..                ..
>Y	positions (x,y,z) forces (x,y,z)
>Lattice a vector (x,y,z)
>Lattice b vector (x,y,z)
>Lattice c vector (x,y,z)
>state ...
>...	...	...
>...	...	...
>...	...	...
>state N
>X	positions (x,y,z) forces (x,y,z)
>X	positions (x,y,z) forces (x,y,z)
>..	..                ..
>Y	positions (x,y,z) forces (x,y,z)
>Lattice a vector (x,y,z)
>Lattice b vector (x,y,z)
>Lattice c vector (x,y,z)

A quick guide to using the program:
running the program can be done using: ".\Excec.py" or "python Excec.py"
the supported arguments (at this moment) are:

help function: '-h' or '--help'.

for the data collection:
atoms:			-e or --element
coordinates:		-p or --pos
forces:			-f or --force
lattice vectors:	-l or --lattice
all of the above	-a or --all

The standard setting is no data collection at all.
So giving one or more of the arguments above is mandatory for data gathering.
The argument for the input file (Which is an output file from one of the mentioned supported programs) is:
	-n or --name
After the argument a filename is specified with directories relative to the directory one is working in currenty.
So when working in directory 'A' and the file is in directory 'B' and the file is called 'output' the arguments together would be:
	'-n B/output' or '--name B/output'

The last feature of this program (at this moment) is the ability to produce a clean file (trajectory of the given input) or to merge the output with an already exsisting output.
The command for a clean output is '-c' or '--clean' (This is also the standard option).
The command for a merged output is '-m' or '--merge'. After this command a merge file should be specified the same way as with -n.
Please note however the merge file is a file previous produced by the program, it is called a 'pickled' file.
The merging can only be done with the files containing the class data! So the 'Human Readable File' or hrf for short,
is for further use for the user. The pickled file is for further use for the progam. 
Note that a merge is between the output from a calculation and a already exsisting merge-file.

An example for excecuting the program:
for a clean file: 'python Excec.py -a -n B/output -c'
for a merged file 'python Excec.py -a -n B/output -m C/mergefile'

A last thing to know is that the output of this program is a file with a uniqe name, it is however a long name.
So it is not neccesary to change the name of the produced files but still advisable.

If there are any bugs please feel free to contact the developers of the program:
I.A.W.Filot@tue.nl		Ivo A.W. Filot
B.Zijlstra@student.tue.nl	Bart Zijlsta
J.v.d.Meijs@student.tue.nl	Joost van der Meijs
