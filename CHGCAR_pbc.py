#!/usr/bin/python

import numpy as np

# Read CHGCAR file
infile = open("CHGCAR")
CHG_i = infile.readlines()
infile.close()

a = CHG_i[2:5]
# Duplicate charge density lattice in each direction
CHG_f = 3*np.array(a)

# Write CHGCAR_mod file
outfile = open("CHGCAR_mod","w")
outfile.write(''.join(CHG_f))
outfile.close()
