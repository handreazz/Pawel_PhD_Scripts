#! /bin/bash
set -x
cd /media/Expansion\ Drive/Case/pepsim/
rsync -azvu /home/pjanowsk/Case/pepsim/RunCase_II .
rsync -azvu /home/pjanowsk/Case/pepsim/RunCase_IV .
rsync -azvu /home/pjanowsk/Case/pepsim/RunCase_III .
rsync -azvu --include '*/' --include '*.nc' --exclude '*' /home/pjanowsk/Case/pepsim/CaseAnalysis .

mkdir -p /media/Expansion\ Drive/York/
mkdir -p /media/Expansion\ Drive/York/1rpg/
mkdir -p /media/Expansion\ Drive/York/1rpg/ReRun1/
cd /media/Expansion\ Drive/York/1rpg/ReRun1/
rsync -azvu /home/pjanowsk/York/1rpg/ReRun1/runN .
rsync -azvu /home/pjanowsk/York/1rpg/ReRun1/runM .
rsync -azvu /home/pjanowsk/York/1rpg/ReRun1/runM_2 .

cd ../../hairpin/
rsync -azvu /home/pjanowsk/York/hairpin/p2p7e_GPU .
rsync -azvu /home/pjanowsk/York/hairpin/rerun .
