#!/bin/sh -e



cif2mtz HKLIN 1lzt-sf.cif HKLOUT 1lzt.mtz <<EOF
END
EOF



cad HKLIN1 1lzt.mtz HKLOUT 1lzt.mtz <<ENDD
LABIN FILE_NUMBER 1 ALL
#LABOUT
#CTYPIN
OUTLIM SPACEGROUP P1
TITLE sort 1lzt.mtz
END
ENDD
