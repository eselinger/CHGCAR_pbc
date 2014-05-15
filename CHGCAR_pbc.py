#!/usr/bin/python

import numpy as np

#Read CHGCAR file
infile = open('CHGCAR','r')
f = open('out','w')

#write header out
sheader = infile.readline() + infile.readline()

f.write(sheader)

#multiply supercell and write out
supercell = []

for i in xrange(3):
    line = infile.readline()
    supercell = [2*float(element) for element in line.split()]
    for element in supercell:
        f.write(str(element) + ' ')
    f.write('\n')

#multiply number of atoms by 8
line = infile.readline()
atoms = [8*int(element) for element in line.split()]
for element in atoms:
    f.write(str(element))

#Add molecule coordinates in each direction

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
