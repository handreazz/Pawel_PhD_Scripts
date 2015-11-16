#!/bin/sh -e


INPUTpdb=solvpep_average_nowat.pdb
OUTPUT=solvpep_average_nowat


sfall XYZIN ${INPUTpdb} HKLOUT ${OUTPUT}.mtz <<eof-sfall >sfall.log
title Structure Factors for 1x1x1
name PROJ uc1x1x1 CRYST fav8nat DATA fav8nat
mode sfcalc xyzin
#labin  FP=FP SIGFP=SIGFP
labout FC=FC PHIC=PHIC
symm 1
#grid 132 180 216
resolution 1 1000
end
eof-sfall


mtz2various hklin ${OUTPUT}.mtz hklout ${OUTPUT}.dat << END >mtz2various.log
output USER '(1x,3i4,2x,2f10.2)'
labin FP=FC PHIC=PHIC
END
