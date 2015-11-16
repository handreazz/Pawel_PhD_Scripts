###Will calculate diffusion constant based on two frames
#give time in picoseconds
#source diffusion_constant.tcl
#ex: diffusion_constant 0 0 "name CA" 1 1000 2000

proc diffusion_constant {mol1 mol2 selection frame1 frame2 time} {
  # get the first coordinate set
  set sel1 [atomselect $mol1 "$selection" frame $frame1]
  set coords1 [$sel1 get {x y z}]
  # get the second coordinate set
  set sel2 [atomselect $mol2 "$selection" frame $frame2]
  set coords2 [$sel2 get {x y z}]
  # and compute the rmsd values
  set rmsd 0
  foreach coord1 $coords1 coord2 $coords2 {
    set rmsd [expr $rmsd + [veclength2 [vecsub $coord2 $coord1]]]
  }
  # divide by the number of atoms and return the result
  return [expr ($rmsd / ([$sel1 num] + 0.0))/$time*10/6]
}
