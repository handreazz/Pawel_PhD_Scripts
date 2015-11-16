#!/bin/sh -e

cad hklin1 out2.mtz hklin2 md_avg_95_rfree.mtz hklout tmp.mtz <<END >/dev/null
labin file 1 E1=FP E2=SIGFP
labin file 2 E1=FP E2=SIGFP
labo file 2 E1=FP E2=SIGFP
labo file 1 E1=FPH1 E2=SIGFPH1
END

scaleit hklin tmp.mtz hklout tmp2.mtz <<EOF >/dev/null
auto                         
refine                     
EOF


sftools <<EOF | grep "OVERALL STATISTICS"
read tmp2.mtz
read protein_noH.mtz
select col 5 = 0
correl col 1 3
select all
select col 5 >0
correl col 1 3
EOF
