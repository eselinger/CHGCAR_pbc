CHGCAR_pbc
===

This script converts an n x n size CHGCAR to a 2n x 2n CHGCAR for display purposes in VMD. This is useful to view with atoms given periodic boundary conditions, since pbcs cannot be applied to CHGCAR files in VMD. It does this by duplicating the original supercell on each positive edge to make the larger cell.

The script reads in the supercell size line by line and multiplies it by 2.

The number of each type of atom is multiplied by 8, and then original atom coordinates are shifted in x, y, z, xy, yz, zx directions for each of the new atoms. The total number of coordinates in the modified CHGCAR will by i*8, if i = total number of atoms regardless of element.

The CHGCAR then gives number of points with a defined charge density in each direction (x, y, z respectively). These are each multiplied by 2 for the modified CHGCAR.


