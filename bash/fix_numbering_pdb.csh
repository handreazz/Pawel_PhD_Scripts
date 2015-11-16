#! /bin/csh

set ff = *.pdb.1
set fnam = $ff:r


set numfil = `ls -1 *.pdb.???? | wc -l`
if( $numfil != 0)then
  foreach fnam (*.pdb.????)
     set fr=$fnam:r
     set fnum=$fnam:e
     mv $fnam $fr.0$fnum
     echo $fnam $fr.0$fnum
  end
endif

set numfil = `ls -1 *.pdb.??? | wc -l`
if( $numfil != 0)then
  foreach fnam (*.pdb.???)
     set fr=$fnam:r
     set fnum=$fnam:e
     mv $fnam $fr.00$fnum
     echo $fnam $fr.00$fnum
  end
endif

set numfil = `ls -1 *.pdb.?? | wc -l`
if( $numfil != 0)then
  foreach fnam (*.pdb.??)
     set fr=$fnam:r
     set fnum=$fnam:e
     mv $fnam $fr.000$fnum
     echo $fnam $fr.000$fnum
  end
endif

set numfil = `ls -1 *.pdb.? | wc -l`
if( $numfil != 0)then
  foreach fnam (*.pdb.?)
     set fr=$fnam:r
     set fnum=$fnam:e
     mv $fnam $fr.0000$fnum
     echo $fnam $fr.0000$fnum
  end
endif



