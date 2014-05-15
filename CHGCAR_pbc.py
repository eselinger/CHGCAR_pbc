#!/usr/bin/python

import numpy as np
import copy as cp

#Read CHGCAR file
infile = open('CHGCAR','r')
f = open('CHGCAR_mod','w')

#copy supercell header to outfile
header = infile.readline() + infile.readline()
f.write(header)

#multiply supercell and write out
supercell = []

for i in xrange(3):
    line = infile.readline()
    supercell = [2*float(element) for element in line.split()]
    for element in supercell:
        f.write(str(element) + ' ')
    f.write('\n')

#multiply number of atoms
line = infile.readline()
anum = []
for element in line.split(): anum.append(int(element)) #storing number of each atom

atoms = [int(element)*8 for element in line.split()] #write out new number of atoms
for element in atoms: f.write(str(element) + '\n')

#copy Direct header to outfile
header = infile.readline()
f.write(header)

#Add molecule coordinates in each direction
atot = 0
if len(anum) < 1:			#get total number of atoms
    for i in xrange(len(anum)):
        atot = atot + anum[i]
else:
    atot = anum[0]

coord = []
coordinates = []
ncoord = []
newcoord = []

for i in xrange(atot):			#read in atom coordinates
    line = infile.readline()
    coord = [float(element)*0.5 for element in line.split()] #original coords/2 for new supercell
    ncoord = [float(element)+0.5 for element in coord] #make array of shifted coordinates
    for element in coord:		#write out coords of original atoms for new supercell
        f.write(str(element) + ' ')
    f.write('\n')
    coordinates.append(coord) #coords of original atoms for new supercell
    newcoord.append(ncoord) #coords of complete shift (x,y,z)

for j in xrange(0,3):			#loop over x y and z columns
    for i in xrange(0,atot):            #for original atoms coordinates (new supercell fractions) replace with (coord+0.5) only all x + write, then all only y + write, etc. 
        fcoord = cp.deepcopy(coordinates)
        fcoord[i][j] = newcoord[i][j]   
        for element in fcoord[i]:
            f.write(str(element) + ' ')
        f.write('\n')

    for i in xrange(0,atot):		#for coord+0.5 coordinates replace with original coordinates, only all x + write, only all y + write
        fcoord = cp.deepcopy(newcoord)
        fcoord[i][j] = coordinates[i][j]
        for element in fcoord[i]:
            f.write(str(element) + ' ')
        f.write('\n')

for i in xrange(0,atot):		#write out all coord+0.5 for all x,y,z
    for element in newcoord[i]:
        f.write(str(element) + ' ')
    f.write('\n')

f.write('\n') #blank line

#multiply number of charges defined in each direction
ignore = infile.readline()
line = infile.readline()

cnum = []
for element in line.split(): cnum.append(int(element)) #storing each number

chgnum = [int(element)*2 for element in line.split()] #write out new number of defined points
for element in chgnum: f.write(str(element) + ' ')
f.write('\n')

#Defined charges array
CHG_i = infile.readlines()
infile.close()

chgvec = [[float(digit) for digit in line.split()] for line in CHG_i[:]]
a = np.array(chgvec)
charges = a.flatten() #one big 1D list

#print charges[0:20]

x = cnum[0] #Defined at this many x,y,z points
y = cnum[1]
z = cnum[2]

xlist = [charges[i:i+x] for i in xrange(0,len(charges),x)] #split into x length sublists

j=0

for i in xrange(len(xlist)): #repeat each x sublist after itself
    xlist.insert(i+j+1,xlist[i+j])
    j=j+1

b = np.array(xlist)
charges = b.flatten()
ylist = [charges[i:i+(y*x*2)] for i in xrange(0,len(charges),y*x*2)]
j=0
i=0

for i in xrange(len(ylist)):
    ylist.insert(i+j+1,ylist[i+j])
    j=j+1

ylist=ylist*2
c = np.array(ylist)
charges = c.flatten()

final = [charges[i:i+5] for i in xrange(0,len(charges),5)] #split into rows of 5, CHGCAR format

np.savetxt('CHG_s.tmp',final)
infile = open("CHG_s.tmp")
charges = infile.read()
infile.close()

#Write output modified CHGCAR
f.write(charges)
f.close()
