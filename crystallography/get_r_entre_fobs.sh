#!/bin/sh -e

cad hklin1 1d23-sf.mtz hklin2 1d23_filt1.mtz hklout tmp.mtz <<END >/dev/null
labin file 1 E1=FOBS E2=SIGFOBS
labin file 2 E1=FP E2=SIGFP
labo file 2 E1=FP E2=SIGFP
labo file 1 E1=FPH1 E2=SIGFPH1
END

scaleit hklin tmp.mtz hklout tmp2.mtz <<EOF >/dev/null
auto                           
refine                     
EOF

echo " " >tmp1.txt
sftools <<EOF | grep OVERALL | awk '{print "Rfactor: " $3}' >>tmp1.txt
read tmp2.mtz

select resol <1.0
correl col 1 3

select all
select resol > 1.0 < 1.5
correl col 1 3

select all
select resol > 1.5 < 2.0
correl col 1 3

select all
select resol > 2.0 < 2.5
correl col 1 3

select all
select resol > 2.5 < 3.0
correl col 1 3

select all
select resol > 3.0 < 3.5
correl col 1 3

select all
select resol > 3.5 < 4.0
correl col 1 3

select all
select resol > 4.0 < 4.5
correl col 1 3

select all
select resol > 4.5 < 5.0
correl col 1 3

select all
select resol > 5.0
correl col 1 3

stop
y
EOF

echo " " >tmp2.txt
sftools <<EOF | grep OVERALL | awk '{print "Rfactor: " $3}' >>tmp2.txt
read tmp2.mtz

select all
select resol > 0.0
correl col 1 3

select all
select resol > 1.0
correl col 1 3

select all
select resol > 2.0
correl col 1 3

select all
select resol > 3.0
correl col 1 3

select all
select resol > 4.0
correl col 1 3

select all
select resol > 5.0
correl col 1 3

stop
y
EOF


cat > tmp3.txt <<EOF
UpToResolution	
All
1.0
2.0
3.0
4.0
5.0

EOF

paste tmp3.txt tmp2.txt >tmp4.txt

cat > tmp3.txt <<EOF
ByBin
<1.0
1.0-1.5
1.5-2.0
2.0-2.5
2.5-3.0
3.0-3.5
3.5-4.0
4.0-4.5
4.5-5.0
>5.0

EOF

paste tmp3.txt tmp1.txt >tmp5.txt

cat tmp4.txt tmp5.txt > R_Fsim_Fobs.txt
