should let the hydrogen atoms move because it is already shaked 
set beta and occupancy to 0.00

set all [atomselect top "all"] # all is just the name 
$all set beta 0.00
$all writepdb x.pdb

$all set occupancy 0.00
$all writepdb x.pdb

set protein [atomselect top "protein and noh"]
set substrate [atomselect top "nucleic and noh"]
$protein set beta 1.00
$protein set occupancy 1.00

$substrate set beta 1.00
$substrate set occupancy 1.00

$all writepdb x.pdb

