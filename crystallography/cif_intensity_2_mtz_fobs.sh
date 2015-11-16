#!/bin/sh -e

#======================================================================#
#                                                                      #
# Convert cif intensity file to Fobs mtz file                          #
#                                                                      #
#======================================================================#


ciffile='4lzt-sf.cif'
pdbfile='4lzt.pdb'


### CONVERT CIF TO MTZ

# USING CCP4
#~ cif2mtz HKLIN ${cif}.cif HKLOUT ${pdbcode}.mtz <<EOF
#~ END
#~ EOF

#~ cad HKLIN1 ${pdbcode}.mtz HKLOUT ${pdbcode}.mtz <<ENDD
#~ LABIN FILE_NUMBER 1 ALL
#~ #LABOUT
#~ #CTYPIN
#~ OUTLIM SPACEGROUP 1
#~ TITLE sort ${pdbcode}.mtz
#~ END
#~ ENDD

# USING PHENIX WHICH READS CELL INFO FROM PDB FILE
phenix.cif_as_mtz_1.8.2-1309 ${ciffile} --use-model=${pdbfile}


truncate hklin 4lzt-sf.mtz hklout 4lzt-sf-truncated.mtz <<EOF
title 4lzt
truncate yes
nresidue 130
labin IMEAN=IOBS_X SIGIMEAN=SIGIOBS_X 
labout  F=FOBS SIGF=SIGFOBS
EOF

# OPTIONAL CLEANUP
# order the hkl's and make sure the correct ones are selected for sfall (l>=0 for P1 for example)
cad HKLIN1 4lzt-sf-truncated.mtz HKLOUT 4lzt-sf-truncated.mtz <<ENDD
LABIN FILE_NUMBER 1 ALL
OUTLIM SPACEGROUP 1
TITLE sort 4lzt-sf-truncated.mtz
END
ENDD

