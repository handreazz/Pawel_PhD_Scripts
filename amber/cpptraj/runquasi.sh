#! /bin/bash


#matrix mwcovar name mwcvmat out mwcvmat.dat :1-129 start 1 stop 61932 offset 1
#diagmatrix mwcvmat out evecs.dat vecs 1961
#modes fluct out rmsfluct.dat name evecs beg 1 end 3
#modes displ out resdispl.dat name evecs beg 1 end 3
#projection modes evecs.dat out project.dat beg 1 end 2

#~ #100ns
#~ echo "run1"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 500 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat1.dat :1-129 
#~ diagmatrix mwcvmat out evecs1.dat vecs 5883 thermo outthermo thermo1.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log1
#~ 
#~ #250ns
#~ echo "run2"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 1250 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 1250 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat2.dat :1-129 
#~ diagmatrix mwcvmat out evecs2.dat vecs 5883 thermo outthermo thermo2.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log2
#~ 
#~ #500ns
#~ echo "run3"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 2500 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 2500 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat3.dat :1-129 
#~ diagmatrix mwcvmat out evecs3.dat vecs 5883 thermo outthermo thermo3.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log3
#~ 
#~ #750ns
#~ echo "run4"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 3750 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 3750 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat4.dat :1-129 
#~ diagmatrix mwcvmat out evecs4.dat vecs 5883 thermo outthermo thermo4.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log4
#~ 
#~ #1000ns
#~ echo "run5"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 5000 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat5.dat :1-129 
#~ diagmatrix mwcvmat out evecs5.dat vecs 5883 thermo outthermo thermo5.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log5
#~ 
#~ #500-1000ns
#~ echo "run6"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 2500 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 2500 5000 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat6.dat :1-129 
#~ diagmatrix mwcvmat out evecs6.dat vecs 5883 thermo outthermo thermo6.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log6
#~ 
#~ #375_625ns
#~ echo "run7"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1875 3125 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1875 3125 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat7.dat :1-129
#~ diagmatrix mwcvmat out evecs7.dat vecs 5883 thermo outthermo thermo7.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log7
#~ 
#~ #750_100ns
#~ echo "run8"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 3750 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 3750 5000 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat8.dat :1-129
#~ diagmatrix mwcvmat out evecs8.dat vecs 5883 thermo outthermo thermo8.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log8
#~ 
#~ 
#~ #1000ns, no fitting (preserve supercell libration/translation)
#~ echo "run9"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 5000 1
#~ matrix mwcovar name mwcvmat out mwcvmat9.dat :1-129 
#~ diagmatrix mwcvmat out evecs9.dat vecs 5883 thermo outthermo thermo9.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log9

#~ #1000ns, no fitting (preserve supercell libration/translation), no terminal residues
#~ echo "run10"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 5000 1
#~ matrix mwcovar name mwcvmat out mwcvmat10.dat :5-124 
#~ diagmatrix mwcvmat out evecs10.dat vecs 5883 thermo outthermo thermo10.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log10
#~ 
#~ #1000ns, no terminal residues
#~ echo "run11"
#~ rm -rf ctraj_quasi
#~ cat >ctraj_quasi <<EOF
#~ parm /home/pjanowsk/c/Case/4lzt/RunSi/4lztUC.prmtop
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_01_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_02_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_03_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_04_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_05_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_06_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_07_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_08_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_09_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_10_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_11_01.nc 1 5000 1
#~ trajin /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/RevSym_12_01.nc 1 5000 1
#~ reference /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/AvgCoord_asu.rst7.1
#~ rms reference mass :3-127&!(@H=)
#~ matrix mwcovar name mwcvmat out mwcvmat11.dat :5-124 
#~ diagmatrix mwcvmat out evecs11.dat vecs 5883 thermo outthermo thermo11.dat
#~ EOF
#~ cpptraj -i ctraj_quasi >log11


