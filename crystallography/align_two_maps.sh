#! /bin/bash



function AlignMaps {
	####################################################################
	#																   #
	# ALIGN TWO ED MAPS BY CONVOLUTION IN RECIPROCAL SPACE			   #
	#																   #
	####################################################################

	# The optimal x y z shift will be stored in $shift environmental variable

	# input variables
	right_map=$1 						# reference map (usually experimental)
	wrong_map=$2						# map to be shifted
	tempfile="$(mktemp -u tempXXXX_)"   # tempfile prefix

	# calculate SF from experimental map
	sfall mapin $right_map hklout ${tempfile}right.mtz << EOF > /dev/null
mode sfcalc mapin
resolution $reso
EOF


	# calculate SF from simulation map
	sfall mapin $wrong_map hklout ${tempfile}wrong.mtz << EOF > /dev/null
mode sfcalc mapin
resolution $reso
EOF

	# use deconvolution to find optimal shift
	# calculate Fexp/Fsim which are the SF's of the correlation function
	rm -f ${tempfile}del.mtz
	sftools << EOF > /dev/null
read ${tempfile}right.mtz
read ${tempfile}wrong.mtz
set labels
Fright
PHIright
Fwrong
PHIwrong
calc ( COL Fq PHIdel ) = ( COL Fright PHIright ) ( COL Fwrong PHIwrong ) /
calc COL W = COL Fq
select COL Fq > 1
calc COL W = 1 COL Fq /
select all
calc F COL Fdel = COL W 0.5 **
write ${tempfile}del.mtz col Fdel PHIdel
y
stop
EOF

	#calculate correlation map from correlation SF's
	fft hklin ${tempfile}del.mtz mapout ${tempfile}del.map << EOF > ${tempfile}.log
labin F1=Fdel PHI=PHIdel
reso $reso
EOF

	# make sure that we define "sigma" for the unmasked map
	echo "scale sigma 1 0" |\
	mapmask mapin ${tempfile}del.map mapout ${tempfile}zscore.map  > /dev/null

	#find highest peak on correlation map
	peakmax mapin ${tempfile}zscore.map xyzout ${tempfile}peak.pdb << EOF > ${tempfile}.log
numpeaks 10
EOF

	#print results
	cat ${tempfile}peak.pdb | awk '/^ATOM/{\
	 print substr($0,31,8),substr($0,39,8),substr($0,47,8),"   ",substr($0,61)+0}' |\
	 awk 'NR==1{max=$4} $4>max/3' | cat > ${tempfile}best_shift.txt
	zscore=`awk '{print $4;exit}' ${tempfile}best_shift.txt`
	echo "z-score: $zscore"
	shift=`awk '{print $1,$2,$3;exit}' ${tempfile}best_shift.txt`

	#clean
	rm -f ${tempfile}best_shift.txt
	rm -f ${tempfile}zscore.map
	rm -f ${tempfile}peak.pdb
	rm -f ${tempfile}del.map
	rm -f ${tempfile}.log
	rm -f ${tempfile}right.mtz
	rm -f ${tempfile}wrong.mtz
	rm -f ${tempfile}del.mtz
}

function MakeMap {
	####################################################################
	#                                                                  #
	# CALCULATE ED MAP                                                 #
	#                                                                  #
	####################################################################

	#INPUT VARIABLES
	local pdb2map=$1 				#input pdb file name
	local mapname=$2				#output map name

	# MAKE PARAMETER FILE
	cat << EOF > params.txt
MDMULT ${MD_mult[*]}
SHIFT ${shift}
SCALE 1 1 1
BFAC $B
EOF
	# REFORMAT PDB FILE (unit cell cryst and space group, applied shift and scale to
	#          coordinates, set b-factore, set occupancy=1, reformat atom
	#          names so there is no chance SFALL could confuse hydrogen with mercury)
	cat params.txt $pdb2map |\
	awk 'BEGIN{sx=sy=sz=1;B=20} \
		   /^MDMULT/{na=$2;nb=$3;nc=$4;next}\
		   /^SHIFT/{dx=$2;dy=$3;dz=$4;next}\
		   /^SCALE/ && $2*$3*$4>0{sx=$2;sy=$3;sz=$4;next}\
		   /^BFAC/{B=$2;next}\
		   /^CRYST/{a=$2/na*sx;b=$3/nb*sy;c=$4/nc*sz;al=$5;be=$6;ga=$7;sg=(substr($0,56,15));\
			 printf "CRYST1%9.3f%9.3f%9.3f%7.2f%7.2f%7.2f %15s\n",a,b,c,al,be,ga,sg}\
		  /^ATOM/{\
			RES= substr($0, 18, 9);\
			X = (substr($0, 31, 8)+dx)*sx;\
			Y = (substr($0, 39, 8)+dy)*sy;\
			Z = (substr($0, 47, 8)+dz)*sz;\
			Ee = $NF;\
		printf("ATOM %6d %2s   %9s    %8.3f%8.3f%8.3f  1.00%6.2f%12s\n",++n,Ee,RES,X,Y,Z,B,Ee);}\
		END{print "END"}' |\
		cat > sfallme.pdb

	# GET UNIT CELL PARAMETERS
	pcell=( `head -1 sfallme.pdb | awk '{print $2,$3,$4,$5,$6,$7}'` )
	echo cell is ${pcell[*]}

	# ADD PDB SCALE MATRIX INFORMATION
	pdbset xyzin sfallme.pdb xyzout new.pdb << EOF > /dev/null
SPACE "$SG"
CELL ${pcell[*]}
EOF
	mv new.pdb sfallme.pdb


	# CALCULATE MAP
	sfall xyzin sfallme.pdb mapout ${mapname} << EOF > /dev/null
mode atmmap
CELL ${pcell[*]}
SYMM $SG
FORMFAC NGAUSS 5
$GRID
EOF
	#CLEAN
	rm -f params.txt
	rm -f new.xyz
	rm -f sfallme.xyz
	#~ rm -f sfallme.pdb
}


MD_mult=( 4 3 3 )			                            #supercell multiplicity (x y z)
SG="P1"					                                  #ccp4 space group symbol, no spaces
GRID=GRID="GRID 200 200 200"		                    #grid spacing for SFALL map
B=15                                              #flat B-factor added to frames to avoid singularity in SFALL map calculation
reso=0.9
right_map=$1
wrong_map=$2
out_map=$3
symops=`awk -v SG=$SG '$4==SG{print $2;exit}' ${CLIBD}/symop.lib` #no. of sym operations
shift=" 0 0 0 "


AlignMaps $right_map $wrong_map
echo "SHIFT: $shift" | awk '{printf("%-15s  %10s  %10s  %10s\n",$1,$2,$3,$4) }'
# shift printed. How to shift the map?
