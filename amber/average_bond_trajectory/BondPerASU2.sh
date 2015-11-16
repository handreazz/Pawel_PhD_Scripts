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

UC=1
for i in `ls /home/pjanowsk/York/hairpin/p2p7e/analysisGPU_last50ns/revsym/RevSym*nc`; do
	cat <<EOF > ctraj_AvgCoord
parm ${ASU_PRMTOP}
reference ${ASU_PDB}
trajin ${i}
rms reference mass :1-756@O5',C5',C4',O4',C1',C3',C2',O2',O3'
average AvgCoord.rst7 restart 
go 
EOF
	cpptraj< ctraj_AvgCoord >ctraj.out
mv 	AvgCoord.rst7.1 AvgCoord.rst7
	cat <<EOF > ctraj_rmsd
parm ${ASU_PRMTOP}
reference ${ASU_PDB}
#trajin revsym/${i}
trajin AvgCoord.rst7
rms reference mass out AvgCoord_rmsd_heavy.dat :1-756&!(@H=)&!(:SO4,CON) 
rms reference mass out AvgCoord_rmsd_bkbn.dat  :1-756@O5',C5',C4',O4',C1',C3',C2',O2',O3' 
rms reference mass out AvgCoord_rmsd_active.dat  (:5@P=,O=,C1',C2',C3',C4',C5',C1H,C2H,C3H,C4H,C5H&!@O6G)|(:49@N=,C8,C4,C5,C2,C6)|(:19@N=,C6,C2,C5,C4,C8,O6)
go
EOF
	cpptraj < ctraj_rmsd >ctraj.out

	cat <<EOF > ctraj_bond
parm ${ASU_PRMTOP}
#trajin revsym/${i}
trajin AvgCoord.rst7
distance :49@H1 :5@O5H out Bond_A38H1_G1O5.dat
distance :49@N1 :5@O5H out Bond_A38N1_G1O5.dat
angle :49@N1 :49@H1 :5@O5H out Angle_A38N1_A38H1_G1O5.dat
distance :19@H1 :5@O2' out Bond_G8H1_G1O2.dat
distance :19@N1 :5@O2' out Bond_G8N1_G1O2.dat
angle :19@N1 :19@H1 :5@O2' out Angle_G8N1_G8H1_G1O2.dat
distance :5@O5H :5@PX out Bond_G1O5_G1PX.dat
go
EOF
	cpptraj < ctraj_bond >ctraj.out

	printf "UC_%02d\n" "$UC">tmp
	let UC=UC+1

	cat AvgCoord_rmsd_heavy.dat \
		AvgCoord_rmsd_active.dat \
		Bond_A38H1_G1O5.dat \
		Bond_A38N1_G1O5.dat \
		Angle_A38N1_A38H1_G1O5.dat \
		Bond_G8H1_G1O2.dat \
		Bond_G8N1_G1O2.dat \
		Angle_G8N1_G8H1_G1O2.dat \
		Bond_G1O5_G1PX.dat \
		tmp  |\
	awk 'BEGIN{} \
		   NR==2{heavy=$2}\
		   NR==4{active=$2}\
		   NR==6{h1=$2}\
		   NR==8{n1=$2}\
		   NR==10{a1=$2}\
		   NR==12{h2=$2}\
		   NR==14{n2=$2}\
		   NR==16{a2=$2}\
		   NR==18{p1=$2}\
		   /UC/{file=$1};
		  END{printf "%s\t\t%5.3f\t\t%5.3f\t\t%5.3f\t%5.3f\t%5.3f\t\t\t%5.3f\t%5.3f\t%5.3f\t%5.3f\n", file,heavy,active,h1,n1,a1,h2,n2,a2,p1}' |\
	cat >>output6.dat
done



	  
		  
