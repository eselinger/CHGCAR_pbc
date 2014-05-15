#!/usr/bin/python

import numpy as np
import copy as cp

#Read CHGCAR file
infile = open('CHGCAR','r')
f = open('out','w')

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

atoms = [int(element)*8 for element in line.split()]
for element in atoms: f.write(str(element) + '\n')

#copy Direct header to outfile
header = infile.readline()
f.write(header)

#Add molecule coordinates in each direction
if len(anum) > 1:			#get total number of atoms
    for i in xrange(len(anum)):
        atot = anum[i] * anum[i+1]
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

for j in xrange(0,3):
    for i in xrange(0,atot):        
        fcoord = cp.deepcopy(coordinates)
        fcoord[i][j] = newcoord[i][j]   
        for element in fcoord[i]:
            f.write(str(element) + ' ')
        f.write('\n')

print coordinates
print fcoord

#Defined charges array
CHG_i = infile.readlines()
print CHG_i[1:2]
array = [[float(digit) for digit in line.split()] for line in CHG_i[17:-64]]
a = np.array(array)
charges = a.flatten() #one big 1D list

#print charges[0:20]

x=3 #Defined at this many x,y,z points
y=4
z=5

zlist = [charges[i:i+z] for i in xrange(0,len(charges),z)] #split into z length sublists

j=0

for i in xrange(len(zlist)): #repeat each z sublist after itself
    zlist.insert(i+j+1,zlist[i+j])
    j=j+1

b = np.array(zlist)
charges = b.flatten()
ylist = [charges[i:i+(y*z*2)] for i in xrange(0,len(charges),y*z*2)]
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
i = open("CHG_s.tmp")
charges = i.read()
i.close()

#Write output modified CHGCAR
infile.close()
f.close()
