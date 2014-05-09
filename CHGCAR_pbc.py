#!/usr/bin/python

import numpy as np

# Read CHGCAR file
infile = open("CHGCAR")
CHG_i = infile.readlines()
infile.close()

CHG_f = CHG_i[2:5]

# Write CHGCAR_mod file
outfile = open("CHGCAR_supercell","w")
outfile.write(''.join(CHG_f))
outfile.close()

with open('CHGCAR_supercell') as file:
    array = [[float(digit) for digit in line.split()] for line in file]

# Duplicate charge density lattice in each direction

array3x = 3*np.array(array)

np.savetxt('CHG_f',array3x)


