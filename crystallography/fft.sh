#!/bin/sh -e


fft HKLIN fav8.hkl.mmcif_refmac.mtz MAPOUT fav8.map <<END
fftspacegroup P1
title  fav8 map
XYZLIM ASU
LABIN F1=FP SIG1=SIGFP F2=FWT PHI=PHWT
END
