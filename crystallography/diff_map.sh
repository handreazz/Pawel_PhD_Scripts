#! /bin/bash



cad hklin1 ../../refme_4sigcut.mtz hklin2 ../md_avg_sigcut.mtz hklin3 ../md_avg.mtz hklout tmp.mtz <<END >/dev/null
labin file 1 E1=F E2=SIGF
labin file 2 E1=FP E2=SIGFP 
labin fil3 3 E1=PHI
labo file 1 E1=FPH1 E2=SIGFPH1
labo file 2 E1=FP E2=SIGFP 
labo file 3 E1=PHI
END

scaleit hklin tmp.mtz hklout tmp2.mtz <<EOF >/dev/null
auto                         
refine                     
EOF


fft hklin tmp2.mtz mapout diff_map.map.ccp4 <<EOF >/dev/null
labin F1=FPH1 SIG1=SIGFPH1 F2=FP SIG2=SIGFP PHI=PHI
EOF

sfall mapin diff_map.map.ccp4 hklout diff_map.mtz << EOF > /dev/null
MODE SFCALC MAPIN
RESOLUTION 0.9
EOF
