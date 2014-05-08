#!/usr/bin/python

# Read file
infile = open("CHGCAR", "r+")
CHG_i = infile.read()
infile.close()

CHG_f = CHG_i

# Write file
outfile = open("CHGCAR_mod","w")
outfile.write(CHG_f)
outfile.close()
