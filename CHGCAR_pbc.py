#!/usr/bin/python

import numpy as np

#Read CHGCAR file
infile = open("CHGCAR1")
CHG_i = infile.readlines()
infile.close()

#Copy supercell and Direct headers
CHG_sheader = CHG_i[0:2]
CHG_dheader = CHG_i[6:16]

#Multiply supercell + # of atoms
CHG_tmp = [0,0,0]
CHG_s = [0,0,0,0]

CHG_tmp[0] = CHG_i[2:5] 
mol = CHG_i[5:6]

if [[float(digit) for digit in i.split()] for i in mol]: #read in if >1 atom type (if so, there is an extra line)
    CHG_tmp[1] = CHG_i[5:6]
    CHG_s[2] = 0
    CHG_tmp[2] = CHG_i[16:17]
else:
    CHG_dheader = CHG_i[7:17]
    CHG_tmp[1] = CHG_i[6:7]
    CHG_tmp[2] = CHG_i[17:18]
    CHG_s[3] = CHG_i[5:6]

for i in range (0,3): #multiplying supercell/atoms by 3
    array = [[float(digit) for digit in line.split()] for line in CHG_tmp[i]]

    array3x = 2*np.array(array)
    np.savetxt('CHG_s.tmp',array3x)

    infile = open("CHG_s.tmp")
    CHG_s[i] = infile.read()
    infile.close()

#Add molecule coordinates in each direction

#Defined charges array
array = [[float(digit) for digit in line.split()] for line in CHG_i[17:]]
x = np.array(array)
charges = x.flatten()

x=1
y=2
z=3

def chunks(list,n):
   for i in xrange(0, len(list), n):
       yield list[i:i+n]

everyz = [charges[i:i+z] for i in xrange(0,x*y*z,z)]
iz = list(everyz)

print iz

np.savetxt('CHG_s.tmp',zlist)
infile = open("CHG_s.tmp")
charges = infile.read()
infile.close()

#Write output modified CHGCAR
outfile = open("CHGCAR_mod","w")
if [[float(digit) for digit in i.split()] for i in mol]:
    outfile.write(''.join(CHG_sheader) + CHG_s[0] + CHG_s[1] +''.join(CHG_dheader)+ CHG_s[2] +charges)
else:
    outfile.write(''.join(CHG_sheader) + CHG_s[0] + ''.join(CHG_s[3]) + CHG_s[1] +''.join(CHG_dheader))
