##################################################################################
#                                                                                #		
#                              Ruben Zubac                                       #
#            Mediterranean institute for Life Sciences (MedILS)                  #
#                                Croatia                                         #
#                                                                                #
#      Script for calculating S2 from pdb using emperical model from             #
#    Ming, D. & Bruschweiler, R. (2004) J. Mol. Biomol. NMR 29, 363-368          #
#                                                                                #
##################################################################################
 
# Use this script in the VMD TkConsole after loading your pdb file into VMD.
# The occupancies of the atoms with the highest occupancies in the pdb should 
# be set to 1.00 (of course also remove the atoms with the lower occupancies).

# The script outputs two files S2output.txt and S2output_plot.txt. The first
# contains more information but the second is easier to plot using i.e. gnuplot.

# selects all C alpha atoms in the protein
set ChA [atomselect top "chain A and alpha"]
set ResNum [$ChA num]

# constants used in the emperical model
set Reff 3.4
set a 0.26
set b 2.2
set c 0.125

# generate output files
set file [open "S2output.txt" w]
set f [open "S2output_plot.txt" w]
puts $file "ResNum	ResTyp	Methgrp	S2 "

# set function to calculate distance between two atoms
proc Distance { Mxyz Ex Ey Ez } {
  
  set dx [expr [lindex $Mxyz 0] - $Ex]
  set dy [expr [lindex $Mxyz 1] - $Ey]
  set dz [expr [lindex $Mxyz 2] - $Ez]
  
  set dist [expr sqrt($dx*$dx + $dy*$dy + $dz*$dz)]
  
  return $dist
}

# loop over all residues in the protein
for {set x 0} {$x < $ResNum} {incr x} {
  set Res [atomselect top "residue $x and alpha"]
  set ResName [$Res get resname]
  
  # select the correct approach for each sort of residue with an methyl group
  if {$ResName == "ILE"} {
	
	# select all heavy atoms from ligands, cofactors and the protein (except 
	# the atoms of the residue currently looked at)  
	set Prot [atomselect top "not water and {not residue $x}"]
	
	# making list of x, y and z coordinates for each selected atom
	set xProt [$Prot get {x}]
	set yProt [$Prot get {y}]
	set zProt [$Prot get {z}]
	
	# amount of atoms from which the distance has to be calculated from the methyl group
	set lengthProt [llength $xProt]
	
	# ILE has two methyl groups. The carbon atom of each is selected.
	set Meth1 [atomselect top "residue $x and name CD1"]
	set cor1 [list [$Meth1 get {x}] [$Meth1 get {y}] [$Meth1 get {z}] ]
	set Meth2 [atomselect top "residue $x and name CG2"]
	set cor2 [list [$Meth2 get {x}] [$Meth2 get {y}] [$Meth2 get {z}] ]
	
	set contsum1 0.
	set contsum2 0.
	
	# loop over all atoms from which the distance has to be calculated form the methyl group
	for {set i 0} {$i < $lengthProt} {incr i} {
	
	  # the x, y and z coordinate from the atom currently looked at is put in a variable
	  set ElseX [lindex $xProt $i]
	  set ElseY [lindex $yProt $i]
	  set ElseZ [lindex $zProt $i]
	
	  # distance from the methyl group carbon calculated  
	  set dist1 [Distance $cor1 $ElseX $ElseY $ElseZ] 
	  set dist2 [Distance $cor2 $ElseX $ElseY $ElseZ]
	  
	  # contact sum calculated for each methyl group carbon
	  set contsum1 [expr $contsum1 + exp( -1 * $dist1 / $Reff )]
	  set contsum2 [expr $contsum2 + exp( -1 * $dist2 / $Reff )]	
	}
	
	# S2 calculated from the emperical model
	set S2_1 [expr tanh( $a * $contsum1 / pow(3,$b) ) - $c]
	set S2_2 [expr tanh( $a * $contsum2 / pow(2,$b) ) - $c]
	
	# data outputted to files
	set h [expr $x + 1]
	puts $file "$h 		$ResName 	CD1		$S2_1 "
	puts $file "$h 		$ResName 	CG2		$S2_2 "
	puts $f "$h		$S2_1"
	puts $f "$h		$S2_2"
	$Prot delete
	$Meth1 delete
	$Meth2 delete
  }
  if {$ResName == "LEU"} {
	set Prot [atomselect top "not water and {not residue $x}"]
	set xProt [$Prot get {x}]
	set yProt [$Prot get {y}]
	set zProt [$Prot get {z}]
	set lengthProt [llength $xProt]
	set Meth1 [atomselect top "residue $x and name CD1"]
	set cor1 [list [$Meth1 get {x}] [$Meth1 get {y}] [$Meth1 get {z}] ]
	set Meth2 [atomselect top "residue $x and name CD2"]
	set cor2 [list [$Meth2 get {x}] [$Meth2 get {y}] [$Meth2 get {z}] ]
	
	set contsum1 0.
	set contsum2 0.
	
	for {set i 0} {$i < $lengthProt} {incr i} {
	  set ElseX [lindex $xProt $i]
	  set ElseY [lindex $yProt $i]
	  set ElseZ [lindex $zProt $i]
	  
	  set dist1 [Distance $cor1 $ElseX $ElseY $ElseZ] 
	  set dist2 [Distance $cor2 $ElseX $ElseY $ElseZ]
	  
	  set contsum1 [expr $contsum1 + exp( -1 * $dist1 / $Reff )]
	  set contsum2 [expr $contsum2 + exp( -1 * $dist2 / $Reff )]
	  
	}
	set S2_1 [expr tanh( $a * $contsum1 / pow(3,$b) ) - $c]
	set S2_2 [expr tanh( $a * $contsum2 / pow(3,$b) ) - $c]

	set h [expr $x + 1]
	puts $file "$h 		$ResName 	CD1		$S2_1 "
	puts $file "$h 		$ResName 	CD2		$S2_2 "
	puts $f "$h		$S2_1"
	puts $f "$h		$S2_2"
	$Prot delete
	$Meth1 delete
	$Meth2 delete
  }
  if {$ResName == "MET" || $ResName == "MSE" } {
	set Prot [atomselect top "not water and {not residue $x}"]
	set xProt [$Prot get {x}]
	set yProt [$Prot get {y}]
	set zProt [$Prot get {z}]
	set lengthProt [llength $xProt]
	set Meth1 [atomselect top "residue $x and name CE"]
	set cor1 [list [$Meth1 get {x}] [$Meth1 get {y}] [$Meth1 get {z}] ]
	
	set contsum1 0.
	set contsum2 0.
	
	for {set i 0} {$i < $lengthProt} {incr i} {
	  set ElseX [lindex $xProt $i]
	  set ElseY [lindex $yProt $i]
	  set ElseZ [lindex $zProt $i]
	  
	  set dist1 [Distance $cor1 $ElseX $ElseY $ElseZ] 
	  
	  set contsum1 [expr $contsum1 + exp( -1 * $dist1 / $Reff )]
	}
	set S2_1 [expr tanh( $a * $contsum1 / pow(4,$b) ) - $c]
	
	set h [expr $x + 1]
	puts $file "$h 		$ResName 	CE 		$S2_1 "
	puts $f "$h		$S2_1"
	$Prot delete
	$Meth1 delete
  }
  if {$ResName == "THR"} {
  	set Prot [atomselect top "not water and {not residue $x}"]
	set xProt [$Prot get {x}]
	set yProt [$Prot get {y}]
	set zProt [$Prot get {z}]
	set lengthProt [llength $xProt]
	set Meth1 [atomselect top "residue $x and name CG2"]
	set cor1 [list [$Meth1 get {x}] [$Meth1 get {y}] [$Meth1 get {z}] ]
	
	set contsum1 0.
	set contsum2 0.
	
	for {set i 0} {$i < $lengthProt} {incr i} {
	  set ElseX [lindex $xProt $i]
	  set ElseY [lindex $yProt $i]
	  set ElseZ [lindex $zProt $i]
	  
	  set dist1 [Distance $cor1 $ElseX $ElseY $ElseZ] 
	    
	  set contsum1 [expr $contsum1 + exp( -1 * $dist1 / $Reff )]
	}
	set S2_1 [expr tanh( $a * $contsum1 / pow(2,$b) ) - $c]
	
	set h [expr $x + 1]
	puts $file "$h 		$ResName 	CG2		$S2_1 "
	puts $f "$h		$S2_1"
	$Prot delete
	$Meth1 delete
  }
  if {$ResName == "VAL"} {
  	set Prot [atomselect top "not water and {not residue $x}"]
	set xProt [$Prot get {x}]
	set yProt [$Prot get {y}]
	set zProt [$Prot get {z}]
	set lengthProt [llength $xProt]
	set Meth1 [atomselect top "residue $x and name CG1"]
	set cor1 [list [$Meth1 get {x}] [$Meth1 get {y}] [$Meth1 get {z}] ]
	set Meth2 [atomselect top "residue $x and name CG2"]
	set cor2 [list [$Meth2 get {x}] [$Meth2 get {y}] [$Meth2 get {z}] ]
	
	set contsum1 0.
	set contsum2 0.
	
	for {set i 0} {$i < $lengthProt} {incr i} {
	  set ElseX [lindex $xProt $i]
	  set ElseY [lindex $yProt $i]
	  set ElseZ [lindex $zProt $i]
	  
	  set dist1 [Distance $cor1 $ElseX $ElseY $ElseZ] 
	  set dist2 [Distance $cor2 $ElseX $ElseY $ElseZ]
	  
	  set contsum1 [expr $contsum1 + exp( -1 * $dist1 / $Reff )]
	  set contsum2 [expr $contsum2 + exp( -1 * $dist2 / $Reff )]
	}
	set S2_1 [expr tanh( $a * $contsum1 / pow(2,$b) ) - $c]
	set S2_2 [expr tanh( $a * $contsum2 / pow(2,$b) ) - $c]

	set h [expr $x + 1]
	puts $file "$h 		$ResName 	CG1		$S2_1 "
	puts $file "$h 		$ResName 	CG2		$S2_2 "
	puts $f "$h		$S2_1"
	puts $f "$h		$S2_2"
	$Prot delete
	$Meth1 delete
	$Meth2 delete
  }
  if {$ResName == "ALA"} {
  	set Prot [atomselect top "not water and {not residue $x}"]
	set xProt [$Prot get {x}]
	set yProt [$Prot get {y}]
	set zProt [$Prot get {z}]
	set lengthProt [llength $xProt]
	set Meth1 [atomselect top "residue $x and name CB"]
	set cor1 [list [$Meth1 get {x}] [$Meth1 get {y}] [$Meth1 get {z}] ]
	
	set contsum1 0.
	set contsum2 0.
	
	for {set i 0} {$i < $lengthProt} {incr i} {
	  set ElseX [lindex $xProt $i]
	  set ElseY [lindex $yProt $i]
	  set ElseZ [lindex $zProt $i]
	  
	  set dist1 [Distance $cor1 $ElseX $ElseY $ElseZ]
	    
	  set contsum1 [expr $contsum1 + exp( -1 * $dist1 / $Reff )]
	}
	set S2_1 [expr tanh( $a * $contsum1 / pow(1,$b) ) - $c]

	set h [expr $x + 1]	
	puts $file "$h 		$ResName 	CB 		$S2_1 "
	puts $f "$h		$S2_1"
	$Prot delete
	$Meth1 delete
  }
}
# close the filled files
close $file
close $f
