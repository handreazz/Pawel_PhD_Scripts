#! /bin/bash
set -x

#----------------------------------------------------------------------#
#                                                                      #
# A preparation script to merge and strip of waters trajectory files   #
# before passing to FullAnalysis.sh from xtalutil/Analysis package     #
#                                                                      #
#----------------------------------------------------------------------#

#SET VARIABLES
WORKING_DIR=/home/pjanowsk/York/1rpg/ReRun1/analyzeM/
TRAJ_ROOT=/home/pjanowsk/York/1rpg/ReRun1/runM/RunEx/Trajectory/md
TRAJ_EXT=nc
TRAJ_START=1
TRAJ_END=12
OFFSET=10
STRIP_MASK=":255-9999"
SC_TOPO=/home/pjanowsk/York/1rpg/ReRun1/runM/amb_1rpgM.prmtop


########################################################################

cd ${WORKING_DIR}
rm -rf ctraj.merge.in merge_nowat.nc

# strip waters and mergetrajectory
echo -e '\n############################\nmerging trajectory\n####################'
echo "parm ${SC_TOPO}" >> ctraj.merge.in
for i in `seq ${TRAJ_START} ${TRAJ_END}`; do
	echo "trajin ${TRAJ_ROOT}${i}.${TRAJ_EXT} 1 -1 ${OFFSET}" >> ctraj.merge.in
done
echo "strip ${STRIP_MASK}" >> ctraj.merge.in
echo "center mass origin" >> ctraj.merge.in
echo "trajout merge_nowat.nc netcdf" >> ctraj.merge.in
cpptraj <ctraj.merge.in
