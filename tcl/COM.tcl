
########################################################################
# Find center of mass of a pdb structure                               #
# Usage:                                                               #
#  vmd -dispdev text -e COM.tcl -args 1rpg.pdb                         #
########################################################################

mol new [lindex $argv 0]
if { $argc == 3 } {
	mol addfile [lindex $argv 1]
}
set sel1 [atomselect top "resid 2 to 12 and not hydrogen"]
set cent [measure center $sel1 weight mass]
set f [open COM.txt w]
puts $f $cent
puts $cent
#puts $f [$sel1 num]
close $f
quit
