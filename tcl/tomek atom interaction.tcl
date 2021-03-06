proc tomek {distort} {
# This script is 1) calculating which atoms are contact atoms for binding ubq to it's ligand for distances between ubq and ligand atom eq rvdW +dist +rvdW,
# where dist is equal to {0.5, 1.5, 3, 5, 7.5, 10, 15, 20} 
set chain G
set ubq [atomselect top "chain $chain"]
set int [atomselect top "protein and chain H"]
set carbon C
set nitrogen N
set oxygen O
set sulfur S
set distance {$distort}

foreach dist $distance {
$ubq set beta 0
$int set beta 0
set uj {} 
set intindex [$int get index]
foreach i $intindex {
set atom [atomselect top "index $i"]
set elem [$atom get element]
set crd [lindex [$atom get {x y z}] 0]
set x_rf [lindex $crd 0]
set y_rf [lindex $crd 1]
set z_rf [lindex $crd 2]
if {$elem == $carbon} {set rvdw 1.7}
if {$elem == $nitrogen} {set rvdw 1.55}
if {$elem == $oxygen} {set rvdw 1.52}
if {$elem == $sulfur} {set rvdw 1.85}
set test [atomselect top "chain $chain and ((x-$x_rf)*(x-$x_rf) + (y-$y_rf)*(y-$y_rf) +(z-$z_rf)*(z-$z_rf)) <= [expr ($rvdw + 1.7 + $dist)*($rvdw + 1.7 + $dist)] and element C"]
set cos [$test get index]
if {$cos != {}} {
$test set beta 100
lappend uj $cos
}
set test [atomselect top "chain $chain and ((x-$x_rf)*(x-$x_rf) + (y-$y_rf)*(y-$y_rf) +(z-$z_rf)*(z-$z_rf)) <= [expr ($rvdw + 1.55 + $dist)*($rvdw + 1.55 + $dist)] and element N"]
set cos [$test get index]
if {$cos != {}} {
$test set beta 100
lappend uj $cos
}
set test [atomselect top "chain $chain and ((x-$x_rf)*(x-$x_rf) + (y-$y_rf)*(y-$y_rf) +(z-$z_rf)*(z-$z_rf)) <= [expr ($rvdw + 1.52 + $dist)*($rvdw + 1.52 + $dist)] and element O"]
set cos [$test get index]
if {$cos != {}} {
$test set beta 100
lappend uj $cos
}
set test [atomselect top "chain $chain and ((x-$x_rf)*(x-$x_rf) + (y-$y_rf)*(y-$y_rf) +(z-$z_rf)*(z-$z_rf)) <= [expr ($rvdw + 1.85 + $dist)*($rvdw + 1.85 + $dist)] and element S"]
set cos [$test get index]
if {$cos != {}} {
$test set beta 100
lappend uj $cos
}
unset x_rf
unset y_rf
unset z_rf
unset crd
$atom delete
$test delete
unset elem
unset cos 
}
set lista {}
for {set j 0} {$j<= [llength $uj]} {incr j} {
set r [lindex $uj $j]
if {[llength $r] ==1} {
set www [lsearch $lista $r]
if {$www == -1 } {lappend lista $r}
} else {
for {set m 0} {$m<=[llength $r]} {incr m} {
set www [lsearch $lista [lindex $uj $j $m]]
if {$www == -1 } {lappend lista [lindex $uj $j $m]}
}
}
}
puts $lista
}

}
