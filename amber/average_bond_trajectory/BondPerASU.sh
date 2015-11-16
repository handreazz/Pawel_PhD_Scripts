#! /bin/sh
#set -x

########################################################################
# A variation on BasicAnalysis.sh to get RevSyms of a coordinate file to 
# then run analysis on each one...
########################################################################

# location of the analysis scripts:
XTAL_ANALYSIS_PATH=/home/pjanowsk/amberSD/AmberTools/src/xtalutil/Analysis/

# location of the input trajectory and Amber files:
WORKING_DIR=/net/casegroup2/u2/pjanowsk/York/hairpin/FindBestp2p7eEquil

#  Amber files for the supercell (might have waters, etc stripped):
SC_PRMTOP=/home/pjanowsk/York/hairpin/p2p7e/analysisGPU_last50ns/p2p7eIa_nowat.prmtop            # supercell topology
SC_RST7=/home/pjanowsk/York/hairpin/p2p7e/analysisGPU_last50ns/p2p7eIa_crystalcoordfile.rst7                 # supercell with pdb (experimental) coords.
SC_TRAJECTORY=/home/pjanowsk/York/hairpin/rerun2_gordon/p2p7e_equil1/Restart/equil30.rst7 # trajectory to be analyzed

#  Amber files for the asymmetric unit:
ASU_RST7=/home/pjanowsk/York/hairpin/p2p7e/analysisGPU/UC_centonpdb.rst7                 # same coordinates as pdb!
ASU_PRMTOP=/home/pjanowsk/York/hairpin/p2p7e/analysisGPU/UC.prmtop
ASU_PDB=/home/pjanowsk/York/hairpin/p2p7e/analysisGPU/UC_centonpdb.pdb            # must contain SMTRY and CRYST1 records 
                                   # from original pdb

#   Information on how the supercell was constructed
PROP=(1 1 1)          # Propagation operations used to build supercell (a, b, c)
ASUS=12                # Number of ASU's in unit cell
UNITCELLS=1           # Number of unit cells in the supercell
RESIDUES=63          # Number of residues in the (stripped) ASU


#~ RM1=":1-756&!(@H=)&!(:SO4,CON)"              
#~ RM2=":1-756@O5',C5',C4',O4',C1',C3',C2',O2',O3'"
#~ RM3="(:5@P=,O=,C1',C2',C3',C4',C5',C1H,C2H,C3H,C4H,C5H&!@O6G)|(:49@N=,C8,C4,C5,C2,C6)|(:19@N=,C6,C2,C5,C4,C8,O6)"

########################################################################
cd ${WORKING_DIR}

function MakeRevSym {
echo
echo '##########################'
echo '# stripping trajectory #'
echo '##########################'
cat <<EOF > ctraj.strip.in
parm /net/casegroup2/u2/pjanowsk/York/hairpin/rerun/equil3x/p2p7eIa_ProdEquil/topo.prmtop
trajin ${SC_TRAJECTORY}
strip :WAT|:Na+|:Cl-
center mass origin
trajout nowat.nc netcdf 
EOF
cpptraj <ctraj.strip.in >ctraj.out


# translate trajectory so centers of mass aligned with pdb crystal
echo
echo '##########################'
echo '# translating trajectory #'
echo '##########################'
cat <<EOF > ctraj.translate.in
parm ${SC_PRMTOP}
trajin nowat.nc
trajout fit.nc netcdf
reference ${SC_RST7}
rmsd reference '!@H=' norotate 
go
EOF
cpptraj < ctraj.translate.in >ctraj.out
if [ $? -ne 0 ]; then
	exit
fi
rm ctraj.translate.in ctraj.out ctraj.strip.in

 

echo
echo '########################'
echo '# splitting trajectory #'
echo '########################'
rm -rf splittrajectories; mkdir splittrajectories; cd splittrajectories
${XTAL_ANALYSIS_PATH}/SplitTrajectory.py \
	-p ${SC_PRMTOP} -t ../fit.nc \
	-u ${UNITCELLS} -a ${ASUS} -r ${RESIDUES} 
cd ..

echo
echo '##########################################'
echo '# reverse symmetry on split trajectories #'
echo '##########################################'
rm -rf revsym; mkdir revsym; cd revsym
${XTAL_ANALYSIS_PATH}/RevSym_netcdf.py \
	-p ${ASU_PDB} -r ${SC_RST7} \
	-ix ${PROP[0]} -iy ${PROP[1]} -iz ${PROP[2]}
cd ..

rm -rf splittrajectories nowat.nc fit.nc 
}



MakeRevSym

for i in `ls revsym`; do
	cat <<EOF > ctraj_rmsd
parm ${ASU_PRMTOP}
reference ${ASU_PDB}
trajin revsym/${i}
rms reference mass out AvgCoord_rmsd_heavy.dat :1-756&!(@H=)&!(:SO4,CON) 
rms reference mass out AvgCoord_rmsd_bkbn.dat  :1-756@O5',C5',C4',O4',C1',C3',C2',O2',O3' 
rms reference mass out AvgCoord_rmsd_active.dat  (:5@P=,O=,C1',C2',C3',C4',C5',C1H,C2H,C3H,C4H,C5H&!@O6G)|(:49@N=,C8,C4,C5,C2,C6)|(:19@N=,C6,C2,C5,C4,C8,O6)
go
EOF
	cpptraj < ctraj_rmvi sd >ctraj.out

	cat <<EOF > ctraj_bond
parm ${ASU_PRMTOP}
trajin revsym/${i}
distance :49@N1 :5@O5H out Bond_A38N1_G1O5.dat
distance :49@H1 :5@O5H out Bond_A38H1_G1O5.dat 
go
EOF
	cpptraj < ctraj_bond >ctraj.out

	echo ${i}>tmp

	cat AvgCoord_rmsd_heavy.dat \
		AvgCoord_rmsd_bkbn.dat \
		AvgCoord_rmsd_active.dat \
		Bond_A38N1_G1O5.dat \
		Bond_A38H1_G1O5.dat \
		tmp  |\
	awk 'BEGIN{} \
		   NR==2{heavy=$2}\
		   NR==4{bkbn=$2}\
		   NR==6{active=$2}\
		   NR==8{n1=$2}\
		   NR==10{h1=$2}\
		   /^RevSym/{file=$1};
		  END{printf "%s %5.2f  %5.2f  %5.2f   %5.2f   %5.2f\n", file,heavy,bkbn,active,n1,h1}' |\
	cat >>PerASU_equil2.dat
done



	  
		  
