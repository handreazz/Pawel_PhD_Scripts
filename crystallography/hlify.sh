#! /bin/bash

chltofom -mtzin md_avg_nowat_952.mtz -mtzout hlified.mtz -colin-phifom '/*/*/[PHI,]' 

sftools << EOF
read hlified.mtz
set labels
FP
SIGFP
PHI
FOM
HLA
HLB
HLC
HLD
write md_avg_nowat_95_HL.mtz col FP SIGFP PHIC FOM HLA HLB HLC HLD
quit
EOF
