#!/usr/bin/python

import numpy as np
import copy as cp

infile = open('CHGCAR','r')
f = open('CHGCAR_mod','w')

header = infile.readline() + infile.readline()		#COPY FILE HEADERS TO OUTFILE
f.write(header)

supercell = []				#MULTIPLY SUPERCELL SIZE

for i in xrange(3):			#for the next three lines (x,y,z of supercell)
    line = infile.readline()		#read in line
    supercell = [2*float(element) for element in line.split()] #split line, copy cell size outward in each direction
    for element in supercell:					#write new supercell to output
        f.write(str(element) + ' ')
    f.write('\n')

							#MULTIPLY NUMBER OF ATOMS
line = infile.readline()				#line with number of atoms
anum = []
for element in line.split(): anum.append(int(element))	#store number of each type of atom as elements of anum array

atoms = [int(element)*8 for element in line.split()]	#new number of each type of atom in expanded supercell
for element in atoms: f.write(str(element) + '\n') 	#write out new number of each 

header = infile.readline()		#copy Direct header to outfile
f.write(header)

					#ADD MOLECULE COORDINATES IN EACH DIRECTION
atot = 0
if len(anum) > 1:			#if more than one type of atom (more than one element in anum)
    for i in xrange(len(anum)):		#find total number of all atoms (regardless of type)
        atot = atot + anum[i]
else:
    atot = anum[0]			#if only one type of atom, value of anum[0] = total number of atoms

coord = []
coordinates = []
ncoord = []
newcoord = []

for i in xrange(atot):			#number of Direct coordinate lines = number of total atoms
    line = infile.readline()		#read in one line at a time, each element in line is x,y,z respectively
    coord = [float(element)*0.5 for element in line.split()] #original atoms location for new supercell
    ncoord = [float(element)+0.5 for element in coord] #array of fully shifted coordinates in all directions
    for element in coord:		#write out coordinates of original atoms for new supercell
        f.write(str(element) + ' ')
    f.write('\n')
    coordinates.append(coord)	#array of coordinates of original atom locations in new supercell
    newcoord.append(ncoord)	#array of coordinates of completely translated atom locations

for j in xrange(0,3):			#loop over x y z, create 6 new arrays 
    for i in xrange(0,atot):            #for total number of atoms of shifted atom coordinates
        fcoord = cp.deepcopy(coordinates) 	#fcoord is duplicate of original atoms coordinates for new supercell
        fcoord[i][j] = newcoord[i][j]		#replace only x, next loop only y, next loop only z
        for element in fcoord[i]:		#write to output file
            f.write(str(element) + ' ')
        f.write('\n')

    for i in xrange(0,atot):		#same as previous loop but replace only x+y or y+z or z+x
        fcoord = cp.deepcopy(newcoord)
        fcoord[i][j] = coordinates[i][j]
        for element in fcoord[i]:
            f.write(str(element) + ' ')
        f.write('\n')

for i in xrange(0,atot):		#add to end of all new coordinates, completely translated coordinates (every direction shifted)
    for element in newcoord[i]:
        f.write(str(element) + ' ')
    f.write('\n')

f.write('\n')				#blank line, necessary for CHGCAR format


ignore = infile.readline()		#MULTIPLY NUMBER OF CHARGES DEFINED IN EACH DIRECTION
line = infile.readline()

cnum = []
for element in line.split(): cnum.append(int(element)) #store number of defined points in x, y, z as cnum elements

chgnum = [int(element)*2 for element in line.split()]	#multiply each element for new number of defined points
for element in chgnum: f.write(str(element) + ' ')	#write out
f.write('\n')

CHG_i = infile.readlines()		#MAKE EXPANDED DEFINED CHARGES ARRAY
infile.close()

chgvec = [[float(digit) for digit in line.split()] for line in CHG_i[:]] #create float array, rest of lines in file
a = np.array(chgvec)			#make numpy array
charges = a.flatten() 			#flatten for 1D list

x = cnum[0]		#defined at this many x,y,z points originally
y = cnum[1]
z = cnum[2]

xlist = [charges[i:i+x] for i in xrange(0,len(charges),x)]	#split into x length sublists

j=0
for i in xrange(len(xlist)):		#insert duplicate of each sublist after itself
    xlist.insert(i+j+1,xlist[i+j])
    j=j+1

b = np.array(xlist)			#new array made out of list with duplicated chunks
charges = b.flatten()			#make 1D array of new array
ylist = [charges[i:i+(y*x*2)] for i in xrange(0,len(charges),y*x*2)]	#split into y length sublists

j=0
for i in xrange(len(ylist)):		#insert duplicate of each sublist after itself
    ylist.insert(i+j+1,ylist[i+j])
    j=j+1

ylist=ylist*2			#duplicate entire list
c = np.array(ylist)
charges = c.flatten()		#flatten into 1D array

final = [charges[i:i+5] for i in xrange(0,len(charges),5)]	#reshape to 5 element rows, CHGCAR format

np.savetxt('CHG_s.tmp',final)		#write out numpy array as string list
infile = open("CHG_s.tmp")		#read back in
charges = infile.read()
infile.close()

f.write(charges)			#write new defined charge points into final output file
f.close()
