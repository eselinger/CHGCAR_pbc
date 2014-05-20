CHGCAR_pbc
===

This script converts an n x n size CHGCAR to a 2n x 2n CHGCAR for display purposes in VMD. This is useful to view with atoms given periodic boundary conditions, since pbcs cannot be applied to CHGCAR files in VMD. It does this by duplicating the original supercell on each positive edge to make the larger cell.

The script reads in the supercell size line by line and multiplies it by 2. 

The number of each type of atom is multiplied by 8, and then original atom coordinates are shifted in x, y, z, xy, yz, zx directions for each of the new atoms. The total number of coordinates in the modified CHGCAR will by i*8, if i = total number of atoms regardless of element.

The CHGCAR file then gives number of points with a defined charge density in each direction (x, y, z respectively). These are each multiplied by 2 for the modified CHGCAR.

Each following number in the original CHGCAR is a charge density defined at a point in the supercell grid. This grid is printed to the CHGCAR with the x axis as the inner loop, and the z axis as the outer loop. This means the points are defined along the x axis, increasing in y until all are defined, and then increase one in z and continue defining points in this pattern.

Using the number of defined x,y,z points this script takes the first x number of points and repeats this block of numbers immediately after itself. Then the next x numbers of point is copied and repeated. This continues for the length of defined points until the loop reaches the augmentation values. The same is then done with y*2 length blocks of points, and then the entire new list of defined points is repeated once. This gives a replica of defined charge densities for the new 2n x 2n cube size.
