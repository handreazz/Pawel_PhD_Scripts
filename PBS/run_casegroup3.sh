# scriptID --> GPU
# 0:5, 1:2, 2:1, 3:0, 4:3, 5:4
# nvidia-smi

export CUDA_VISIBLE_DEVICES=0
export WD=/home/pjanowsk/ReRun2/RunM/

set -x
pmemd.cuda -O -i md.in -o ${WD}/md2.out -p ${WD}/amb_1rpgM_ff14.prmtop	-c ${WD}/md1.rst7 -r md2.rst7 -x md2.nc
