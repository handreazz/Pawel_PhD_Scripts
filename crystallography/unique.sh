#!/bin/sh -e

OUTPUT=test




unique hklout ${OUTPUT}.mtz <<EOF >tmp.tmp
cell 11 16 18 90 90 90
SYMM 1
RESO 1
DEFAULT 1
EOF

#mtzdump hklin ${OUTPUT}.mtz <<eof | grep -A 3 'LIST' |tail -1 | awk '{print 0.5/sqrt($4/4),$4}'
#mtzdump hklin ${OUTPUT}.mtz <<eof | grep -A 20 'LIST'  | awk '/ 0   0   9 /{print 0.5/sqrt($4/4),$4}'
#mtzdump hklin ${OUTPUT}.mtz <<eof | grep -A 20 'LIST' | awk '/ 2   3   4 /{print 1/sqrt($4),$0}'
#nref 20
#lreso
#starthkl 0 -8 0
#eof

mtz2various hklin ${OUTPUT}.mtz hklout ${OUTPUT}.dat << END >mtz2various.log
output USER '(1x,3i4,2x,2f10.2)'
labin FP=F 
END
