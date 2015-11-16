#!/bin/sh -e
INPUTpdb=newfile.pdb
INPUThkl=1lzt.mtz
OUTPUT=Crystal
SYMM=SymmetryHeader.txt

##Make sure occupancy is set to 1.00 and add symmetry header
#~ ./ChangeColumn.py ${INPUTpdb}
cat ${SYMM} ${INPUTpdb} > tmp.txt
mv tmp.txt ${INPUTpdb}

#~ #### with hklin (compare to observed structure factors, calculate Rfactor)
#~ 
sfall XYZIN ${INPUTpdb} \
      HKLIN ${INPUThkl} \
      HKLOUT ${OUTPUT}.mtz <<eof-sfall >sfall.log
title Generate structure factors for average of averages structure
mode sfcalc xyzin hklin
labin  FP=FP SIGFP=SIGFP
labout FC=FC PHIC=PHIC
noscale
#grid 600 600 600
end
eof-sfall

#~ mtz2cif HKLIN ${OUTPUT}.mtz hklout ${OUTPUT}.cif <<EOF >mtzcif.log
#~ labin FP=FP SIGFP=SIGFP FC=FC PHIC=PHIC
#~ datablock data_avgofavges_sf1
#~ end
#~ EOF


mtzdmp ${OUTPUT}.mtz -n 20 | grep -A 10 'LIST'
grep -A 30 'Rfactor' sfall.log

#~ mtz2various hklin ${OUTPUT}.mtz hklout ${OUTPUT}.dat << END >mtzvarious.log
#~ output USER '(1x,3i4,2x,4f10.2)'
#~ labin FP=FP SIGFP=SIGFP FC=FC PHIC=PHIC
#~ END



##Without hklin(create new mtz with just the calculated structure factors)
#~ 
#~ sfall XYZIN ${INPUTpdb} \
      #~ HKLIN ${INPUThkl} \
      #~ HKLOUT ${OUTPUT}.mtz <<eof-sfall
#~ title Generate structure factors from coordinates
#~ mode sfcalc xyzin
#~ #labin  FP=FP SIGFP=SIGFP
#~ labout FC=FC PHIC=PHIC
#~ #noscale
#~ symm 1
#~ name PROJ avgofavges_sf CRYST fav8nat DATA fav8nat
#~ end
#~ eof-sfall
#~ 
#~ mtzdmp ${OUTPUT}.mtz -n 20 | grep -A 10 'LIST'
#~ 
#~ 
#~ mtz2various hklin ${OUTPUT}.mtz hklout ${OUTPUT}.dat << END >mtzvarious.log
#~ output USER '(1x,3i4,2x,2f10.2)'
#~ labin FP=FC PHIC=PHIC
#~ END
