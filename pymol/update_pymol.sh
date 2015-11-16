#! /bin/bash

cd $HOME/c/bin/
rm pymol_tmp

svn co svn://svn.code.sf.net/p/pymol/code/trunk/pymol pymol_tmp
cd pymol_tmp

prefix=$HOME/c/bin/pymol-svn
modules=$prefix/modules
 
python setup.py build install \
    --home=$prefix \
    --install-lib=$modules \
    --install-scripts=$prefix
    
ln -s $HOME/c/bin/pymol-svn/pymol $HOME/c/bin/pymol
rm $HOME/c/bin/pymol_tmp     
