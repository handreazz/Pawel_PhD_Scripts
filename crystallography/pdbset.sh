#!/bin/sh -e

for i in solvpep_average.pdb solvpep_average_nowat.pdb
do

pdbset xyzin ${i} xyzout tmp.pdb <<eof
atrenumber
occupancy
chain ' '
renumber 1
eof

mv tmp.pdb ${i}
		
done



#~ for i in fav8_1x2x1.pdb  fav8_2x1x1.pdb  fav8_2x2x2.pdb  fav8_3x3x3.pdb;
#~ do
#~ 
#~ ./GetBfacsFromCif4SupCell.py fav8_1x1x1.pdb ${i}
#~ mv newfile.pdb ${i}
#~ 
#~ done
