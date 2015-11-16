#!/bin/csh 


#########################created 2009-01-25################################
#  This script is to use multi-programs to calculate statistics (such as
#  R_work, Rfree, real space R factors, density correlation, maps ...)
#  Below are program used
#  1. sf_convert: to convert SF file from mmCIF to mtz format
#  2. refmac: to do unrestrained refinement for ZERO cycle.
#     It generates Fc & weighted 2Fo-Fc & phase information stored in new MTZ.
#  3. fft: to generate Fc and 2Fo-Fc maps using the new MTZ file
#  4. mapmask: to cover the volume of a model (radius = 4.1 angstrom)
#  5. lx_mapman: calculate real space R factors & density correlation
#     It also converts map format from CCP4 to BRIX/DSN6 (O type maps)
#  6. cad:  sort all reflection in asymmetric unit.
#  7. cif2mtz: convert cif to mtz format 
#
############################### Usage ######################################
#  
#  density_eds.csh   pdbfile  sffile
#  
#  The following options (as below) can be added:
#  -noed :  do not calculate real_space_R & dcc.  
#  -map :  output maps  (2Fo-Fc & Fo-Fc) in dns6 formats.
#  -map_ccp4 : output maps (2Fo-Fc & Fo-Fc) in CCP4 formats.
#  -twin :  do twin validation.
#  -tls :  use refmac + TLS (tls info extracted from pdb)
#  -scale :  use all the defaults for scale/bulk by refmac.
#            If not given,  use 'SCALe type BULK  LSSC  ANISO  EXPE'
#############################################################################

if( $#argv < 1 ) then
    echo "Please input a PDB file and a SF file in mmcif format. "
    echo "Usage: ./density_eds.csh  pdbfile  sffile "
    echo "If add (-noed), do not calculate real_space_R & dcc "
    echo "If add (-map), output maps (2Fo-Fc & Fo-Fc) in dns6  formats"
    echo "If add (-map_ccp4), output maps (2Fo-Fc & Fo-Fc) in CCP4 formats"
    echo "If add (-twin), do twin validation"
    echo "If add (-tls), include tls (obtained by tlsextract"
    echo "If add (-scale), use all default for scale/bulk by refmac"
    exit()
endif


if ( $#argv >= 2 ) then
    set tmp = `grep "^CRYST1" -m 1 $1 |wc -w`
    if ($tmp >= 6) then
        set pdbfile = $1
        set sffile  = $2
    else
        set pdbfile = $2
        set sffile  = $1
    endif
else
    echo "Too few arguments"
    exit()
endif    


set map=0 
set map_ccp4=0 
set noed=0 
set twin=0 
set tls=0  
set scale=0  
foreach arg  ($argv)
    if ( "$arg" == "-map" ) then
        set map=1
    else if ( "$arg" == "-noed" ) then
        set noed=1
    else if ( "$arg" == "-map_ccp4" ) then
        set map_ccp4=1
    else if ( "$arg" == "-twin" ) then
        set twin=1
    else if ( "$arg" == "-tls" ) then
        set tls=1
    else if ( "$arg" == "-scale" ) then
        set scale=1
    endif
end


#echo "The input SF=$sffile; The input PDB=$pdbfile"

##################### set output files #################
set map_fc = "${pdbfile}_fc.map"
set map_fofc = "${pdbfile}_fofc.map"
set map_2fofc = "${pdbfile}_2fofc.map"
set map_fofc_dsn6 = "${pdbfile}_fofc_dsn6.map"
set map_2fofc_dsn6 = "${pdbfile}_2fofc_dsn6.map"
set refmac_mtz_out="${pdbfile}_refmac.mtz"
set eds_outtmp="${pdbfile}_eds_out"

##################### convert mmcif to mtz #################
# If sf_convert is not installed, try mtz2cif
#
set sfmtz = "${sffile}.mtz"

echo "Converting mmcif to MTZ format ..."
sf_convert -o mtz -pdb $pdbfile -sf $sffile -out $sfmtz >/dev/null

set mtzsize=`wc -c $sfmtz | awk '{print $1}'`
if( ! -e $sfmtz || $mtzsize < 1000 ) then 
    set cel = `grep "^CRYST1 " -m 1 $pdbfile | cut -c 8-54`
    set sym = `grep "^CRYST1 " -m 1 $pdbfile | cut -c 55-65`
    set tmp_mtz = "${sffile}__tmp"

cif2mtz HKLIN $sffile HKLOUT $tmp_mtz << end > /dev/null 
TITLE testing 
symmetry '$sym'
cell $cel
PNAME mtz2cif
DNAME data_1
XNAME cryst_1
end

cad  HKLIN1 $tmp_mtz HKLOUT  $sfmtz <<end > /dev/null 
TITLE Sorting HKL with cad 
monitor BRIEF
labin file 1 ALL
sort H K L
end
    
if( -e  $tmp_mtz ) rm -f $tmp_mtz

    set mtzsize1 = `wc -c $sfmtz | awk '{print $1}'`
    if( ! -e $sfmtz || $mtzsize1 < 2000 ) then  # mtz2cif failed. 
        echo "Error! SF ($sffile) can not be converted to mtz format."; 
        exit()
    endif        
endif

############################ Run REFMAC5  ########################## 
# This script is to do unrestrained refinement for ZERO cycles.
# The purpose is to generate Fc and weighted 2Fo-Fc (FWT).
# A new MTZ file contains FWT and phase information.
# default: refi resi MLKF meth CGMAT reso all
###################################################### 
#
set tmp = `grep "ANISOU" -m 10 $pdbfile |wc -l`
set anis = ""
if($tmp>5) set anis="bref ANIS"

set twin_inp = ""
if($twin>0) set twin_inp="twin"

set scale_inp=""
if($scale>0) set scale_inp="# "

set tls_info = ""
if($tls>0) then
#extract tls from PDB
set tls_inp = "${pdbfile}_tls.inp"
tlsextract XYZIN $pdbfile TLSOUT $tls_inp >/dev/null
set size=`wc -l $tls_inp  | awk '{print $1}'`
if( -e $tls_inp ||  $size > 6 ) set tls_info = "TLSIN $tls_inp "
endif

echo "Doing REFMAC calculation ..."

set refmac_pdb_out="refmac5_0cyc.pdb"
refmac5 XYZIN  $pdbfile XYZOUT ${pdbfile}_refmac0 HKLIN  $sfmtz $tls_info HKLOUT  $refmac_mtz_out  << end > ${pdbfile}_refmac0_log
MAKE CHECK NONE
MAKE HYDRogens YES
MAKE HOUT YES
labin  FP=FP SIGFP=SIGFP  FREE=FREE 
labout  FC=FC FWT=FWT PHIC=PHIC PHWT=PHWT DELFWT=DELFWT PHDELWT=PHDELWT FOM=FOM
BLIM 0.05 1000
REFI TYPE UNREstrained  RESI MLKF  $anis
#reso 100 2
$scale_inp  SCALe     type BULK    LSSC   ANISO   EXPE
#WEIGHT MATRIX 0.35
#SCALe LSSC FIXBulk BBULk 200
#SCALe TYPE SIMP
#SPHEricity 2.0
#mapcalculate shar # regularised map sharpening, v5.6
#ncsr local       # automatic and local ncs  v5.6
#ridg dist sigm 0.05 # jelly body restraints  v5.6
#solvent NO
NCYC 0
$twin_inp
PNAME TEMP
DNAME NATIVE
RSIZE 80
USECWD
end

# check for success
set mtzsize=`wc -c $refmac_mtz_out | awk '{print $1}'`
if( ! -e $refmac_mtz_out || $mtzsize < 1000 ) then
    echo "Error! REFMAC failed! (pdb=$pdbfile) !"; 
    exit()
endif

if(-e $sfmtz) rm -f  $sfmtz
if($noed>0) then  #do not calculate maps
    rm -f $refmac_mtz_out 
    exit() 
endif

#####################generate FC map #####################
set tmp_map = "${pdbfile}_maptmp"

echo "Calculating Fc map using FC/PHIC by REFMAC ..."
fft  HKLIN  $refmac_mtz_out  MAPOUT  $tmp_map <<end >/dev/null 
title FC
 labin F1=FC PHI=PHIC
end

# Extend the FC map to cover the volume of a model (about 4.1A)
mapmask MAPIN  $tmp_map MAPOUT $map_fc XYZIN  $pdbfile <<end >/dev/null 
BORDER 4.1
end

rm -f $tmp_map 

#####################generate 2Fo-Fc map #####################
echo "Calculating 2Fo-Fc map using FWT/PHWT by REFMAC ..."
fft  HKLIN  $refmac_mtz_out   MAPOUT $tmp_map <<end >/dev/null 
title 2FO-1FC
 labin F1=FWT  PHI=PHWT
end


# Extend the 2Fo-Fc map to cover the volume of a model
mapmask MAPIN  $tmp_map MAPOUT $map_2fofc XYZIN  $pdbfile <<end >/dev/null 
BORDER 4.1
end

rm -f $tmp_map 


#################################################################

set size1=`wc -c $map_fc | awk '{print $1}'`
set size2=`wc -c $map_2fofc | awk '{print $1}'`
if( ! -e $map_fc || ! -e $map_2fofc || $size1 < 1000 || $size2 < 1000 ) then
    echo "Error! map generation was not successful! (check size)"; 
    exit()
endif

rm -f $tmp_map 

############## Doing EDS calculation############
echo "Calculating density correlation and real space R factors by mapman ..."

set resh=`grep "REMARK   2 RESOLUTION.*ANGSTROMS"  -m 1 $pdbfile | awk '{print $4}'`

set test=`echo "$resh > 0.001" | bc`
if( $test ) then
    set resh=`grep "REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) :"  -m 1 $pdbfile | awk '{print $8}'`
else 
    set resh=1.5
endif

set radius = ` echo $resh |  awk '{ if( $resh < 0.6 ) { print 0.7} else if ($resh>3.0) {print $resh/2.0} else { print 0.7 + ($resh - 0.6)/3.0}}'`

#echo " resolution=$resh ;  radius=$radius "

# start to run
setenv MAPSIZE 80000000
lx_mapman -b  <<EOF >& /dev/null
Read m1 $map_fc ccp4
Read m2 $map_2fofc ccp4
rsfit m1 m2 $pdbfile  $eds_outtmp  $radius
quit
EOF

set size1=`wc -c  $eds_outtmp | awk '{print $1}'`
if( ! -e $eds_outtmp || $size1 < 1000 ) then
    echo "Error! EDS calculation was not successful!"; 
    exit()
endif

################################################
if ( $map == 0 && $map_ccp4 == 0) then
    rm -f $map_fc $map_2fofc   $refmac_mtz_out
    exit()
endif


#####################generate Fo-Fc map #####################
#echo "Calculating Fo-Fc map using FWT/PHWT by REFMAC ..."
fft  HKLIN  $refmac_mtz_out   MAPOUT  $tmp_map  <<end >/dev/null 
title FO-FC
 labin F1=DELFWT  PHI=PHDELWT
end


# Extend the Fo-Fc map to cover the volume of a model
mapmask MAPIN  $tmp_map MAPOUT $map_fofc XYZIN  $pdbfile <<end >/dev/null 
BORDER 4.1
end

################################################
if ( $map_ccp4 == 1 ) then
    rm -f $tmp_map  $map_fc    $refmac_mtz_out
    exit()
endif
    

#############Convert CCP4 map to O style (BRIX/DSN6) ############
setenv MAPSIZE 80000000
setenv NUMMAP 1
lx_mapman -b << EOF >& /dev/null
Read m1 $map_fofc CCP4
Write m1 $map_fofc_dsn6  DSN6
quit
EOF

lx_mapman -b << EOF >& /dev/null
Read m1 $map_2fofc CCP4
Write m1 $map_2fofc_dsn6  DSN6
quit
EOF

set size2=`wc -c $map_2fofc_dsn6 | awk '{print $1}'`
if( ! -e $map_2fofc_dsn6 ||  $size2 < 2000 ) then
    echo "Error! map conversion to DSN6 was not successful! (check size)"; 
    exit()
endif

rm -f $tmp_map  $map_fc $map_fofc  $map_2fofc    $refmac_mtz_out
gzip -f  $map_fofc_dsn6  $map_2fofc_dsn6

############## End of script ############

