#!/usr/bin/python

import numpy as np

#Read CHGCAR file
infile = open("CHGCAR")
CHG_i = infile.readlines()
infile.close()

#Copy supercell and Direct headers
CHG_sheader = CHG_i[0:2]
CHG_dheader = CHG_i[6:7]

#Multiply supercell + # of atoms
CHG_tmp = [0,0]
CHG_s = [0,0,0]

CHG_tmp[0] = CHG_i[2:5] 
mol = CHG_i[5:6]

if (float(digit) for digit in mol.split()): #read in if >1 atom type (if so, there is an extra line)
    CHG_tmp[1] = mol
    CHG_s[2] = 0
else:
    CHG_dheader = CHG_i[7:8]
    CHG_tmp[1] = CHG_i[6:7]
    CHG_s[2] = CHG_i[5:6]

for i in range (0,2): #multiplying supercell/atoms by 3
    outfile = open("CHGCAR_supercell.tmp","w")
    outfile.write(''.join(CHG_tmp[i]))
    outfile.close()

    with open('CHGCAR_supercell.tmp') as file:
        array = [[float(digit) for digit in line.split()] for line in file]

    array3x = 3*np.array(array)
    np.savetxt('CHG_s.tmp',array3x)

    infile = open("CHG_s.tmp")
    CHG_s[i] = infile.read()
    infile.close()

#Add molecule coordinates in each direction

#Write output modified CHGCAR
outfile = open("CHGCAR_mod","w")
if isinstance(mol, float):
    outfile.write(''.join(CHG_sheader) + CHG_s[0] + CHG_s[1] +''.join(CHG_dheader))
else:
    outfile.write(''.join(CHG_sheader) + CHG_s[0] + ''.join(CHG_s[2]) + CHG_s[1] +''.join(CHG_dheader))
