source /net/cottus/u2/cliu/note/script/pbcbox/porcplot.tcl


package require pbctools

proc set_celldims {} {
  molinfo top set a 91.8
  molinfo top set b 81.4
  molinfo top set c 90.3
}

proc define_adjacent_monomers {molid keyseg cutoff {drawmol -1}} {
# look for a set of adjacent monomers within cutoff of keyseg
# for each of those monomers, in order, we identify the com vec between the
# center monomer and the monomer in question
# the proc returns a list of such vectors, which can be used by other procs
# to consistently identify neighboring monomers
# note that frame 0 is used for all such calculations
  set keysel [atomselect $molid "protein and segname $keyseg" frame 0]
  pbc wrap -first 0 -last 0 -center com -centersel "protein and segname $keyseg" -compound segid -molid $molid
  #set allsel [atomselect top all]
  #$allsel moveby [vecscale -1 [measure center $keysel weight mass]]
  #pbc wrap -first 0 -last 0 -center "protein and segname $keyseg" -compound chain 

  set neighbors [atomselect $molid "protein and (not segname $keyseg) and (pbwithin $cutoff of segname $keyseg)" frame 0]
  set neighborsegnames [lsort -unique [$neighbors get segname]]
  $neighbors delete

  set comvecs [list]
  foreach neighborseg $neighborsegnames {
    #puts "working on $neighborseg"
    set neighborsel [atomselect $molid "protein and segname $neighborseg" frame 0]
    correct_wrapping $keysel $neighborsel {91.8 81.4 90.3}
    set comvec [vecsub [measure center $keysel weight mass] [measure center $neighborsel weight mass]]
    lappend comvecs $comvec

    if {$drawmol > -1} {
      drawarrow [measure center $keysel weight mass] [measure center $neighborsel weight mass] $drawmol
    }

    $neighborsel delete

  }

  $keysel delete
  return $comvecs
}

proc identify_adjacent_monomers {molid keyseg comvecs cutoff origkeyseg} {
# For a given segment, find the adjacent monomers in frame 0 which best
# match the specifying center of mass vectors (returned by define_adjacent_monomers)
# Return an ordered list of segment names matching each of the vectors

  animate goto 0
  set celldims [list 91.8 81.4 90.3]


  set keysel [atomselect $molid "protein and segname $keyseg" frame 0]
  set allsel [atomselect $molid all]
  $allsel moveby [vecscale -1 [measure center $keysel]]
  pbc wrap -molid $molid -first 0 -last 0 -center com -centersel "protein and segname $keyseg" -compound segid
  #set allsel [atomselect top all]
  #$allsel moveby [vecscale -1 [measure center $keysel weight mass]]
  #pbc wrap -first 0 -last 0 -center "protein and segname $keyseg" -compound chain

  # we need to properly rotate the system so that it matches the frame of referenc
  # used to calculate comvecs

  set keyselca [atomselect $molid "alpha and segname $keyseg"]
  set refkeyselca [atomselect $molid "alpha and segname $origkeyseg"]
  set forwardM [measure fit $keyselca $refkeyselca]
  set reverseM [measure fit $refkeyselca $keyselca]

  set allsel [atomselect $molid all]

  set neighbors [atomselect $molid "protein and (not segname $keyseg) and (pbwithin $cutoff of segname $keyseg)" frame 0]
  set neighborsegnames [lsort -unique [$neighbors get segname]]
  $neighbors delete

  set my_comvecs [list]
  #puts $neighborsegnames
  foreach neighborseg $neighborsegnames {
    #puts "Working on $neighborseg..."
    set neighborsel [atomselect $molid "protein and segname $neighborseg" frame 0]
    correct_wrapping $keysel $neighborsel $celldims
    $allsel move $forwardM
    set comvec [vecsub [measure center $keysel weight mass] [measure center $neighborsel weight mass]]
    $allsel move $reverseM
    lappend my_comvecs $comvec
    $neighborsel delete
  }

  set neighbor_matchlist [list]
  foreach targetvec $comvecs {
    set minmag 100
    set currneighbor "0"
    foreach neighbor $neighborsegnames neighborvec $my_comvecs {
      set test_dist [veclength [vecsub $targetvec $neighborvec]]
      if {$test_dist < $minmag} {
        set minmag $test_dist
        set currneighbor $neighbor
      }
    }
    lappend neighbor_matchlist $currneighbor
  }

  if {[llength [lsort -unique $neighbor_matchlist]] != [llength $neighbor_matchlist]} {
    puts "WARNING: neighbor list $neighbor_matchlist is not unique!"
  }

  $keysel delete
  $keyselca delete
  $refkeyselca delete
  $allsel delete
  return $neighbor_matchlist
}

proc calc_avg_lattice_vectors {molid outprefix} {
# For each timestep in a trajectory, calculate the average distance along
# each vector in the lattice, and its standard deviation, and write them
# to files

  set allprot [atomselect $molid protein]
  set allprotsegs [lsort -unique [$allprot get segname]]
  $allprot delete

  set neighbor_keyvecs [define_adjacent_monomers $molid P18 10]

  set orientations [classify_all_monomers $molid]

  set protsegs_neighborsegs [list]
  foreach seg $allprotsegs {
    #puts "Working on $seg"
    lappend protsegs_neighborsegs [identify_adjacent_monomers $molid $seg $neighbor_keyvecs 10 P18]
  }

  # now set up an m x n x t array to hold all of the distances
  # m is the number of monomers, n the neighbors per monomer,
  # and t the number of timesteps
  array set datarray {}
  set m [llength $protsegs_neighborsegs]
  set n [llength $neighbor_keyvecs]
  set t [molinfo $molid get numframes]
  for {set i 0} {$i < $m} {incr i} {
    set seg [lindex $allprotsegs $i]
    for {set j 0} {$j < $n} {incr j} {
      set oseg [lindex $protsegs_neighborsegs $i $j]
      set vecdat [calc_comvec_vs_t $molid $seg $oseg]
      for {set k 0} {$k < $t} {incr k} {
        array set datarray [list "$i $j $k" [lindex $vecdat $k]]
      }
    }
  }

  set ofile [open "${outprefix}_avgdists.dat" w]
  set ostd [open "${outprefix}_stdevs.dat" w]
  set ofilea [open "${outprefix}_A_avgdists.dat" w]
  set ostda [open "${outprefix}_A_stdevs.dat" w]
  set ofileb [open "${outprefix}_B_avgdists.dat" w]
  set ostdb [open "${outprefix}_B_stdevs.dat" w]
  set ofilec [open "${outprefix}_C_avgdists.dat" w]
  set ostdc [open "${outprefix}_C_stdevs.dat" w]
  set ofiled [open "${outprefix}_D_avgdists.dat" w]
  set ostdd [open "${outprefix}_D_stdevs.dat" w]

  set header "# ([lindex $allprotsegs 0]) [lindex $protsegs_neighborsegs 0]"
  puts $ofile $header
  puts $ostd $header

  for {set k 0} {$k < $t} {incr k} {
    for {set j 0} {$j < $n} {incr j} {
      set dists_for_monomer [list]
      set dists_A [list]
      set dists_B [list]
      set dists_C [list]
      set dists_D [list]
      for {set i 0} {$i < $m} {incr i} {
        #puts [array get datarray "$i $j $k"]
        set mydist [lindex [array get datarray "$i $j $k"] 1]
        #puts $mydist
        #puts $mydist
        lappend dists_for_monomer [veclength $mydist]
        set myorientation [lindex $orientations $i]
        lappend "dists_${myorientation}" [veclength $mydist]
      }
      #puts "For monomer $j at time $k"
      #puts $dists_for_monomer
      #puts " "
      set meandist [calc_mean $dists_for_monomer]
      set stdev [calc_std $dists_for_monomer]
      set meana [calc_mean $dists_A]
      set stda [calc_std $dists_A]
      set meanb [calc_mean $dists_B]
      set stdb [calc_std $dists_B]
      set meanc [calc_mean $dists_C]
      set stdc [calc_std $dists_C]
      set meand [calc_mean $dists_D]
      set stdd [calc_std $dists_D]


      puts -nonewline $ofile "$meandist "
      puts -nonewline $ostd "$stdev "
      puts -nonewline $ofilea "$meana "
      puts -nonewline $ostda "$stda "
      puts -nonewline $ofileb "$meanb "
      puts -nonewline $ostdb "$stdb "
      puts -nonewline $ofilec "$meanc "
      puts -nonewline $ostdc "$stdc "
      puts -nonewline $ofiled "$meand "
      puts -nonewline $ostdd "$stdd "
    }

    puts $ofile ""
    puts $ostd ""
    puts $ofilea ""
    puts $ostda ""
    puts $ofileb ""
    puts $ostdb ""
    puts $ofilec ""
    puts $ostdc ""
    puts $ofiled ""
    puts $ostdd ""
  }


  close $ofile
  close $ostd
  close $ofilea
  close $ostda
  close $ofileb
  close $ostdb
  close $ofilec
  close $ostdc
  close $ofiled
  close $ostdd

  #return [array get datarray]
}

proc calc_mean {input} {
  set numelem [llength $input]
  set sum 0
  foreach elem $input {
    set sum [expr $sum + $elem]
  }

  return [expr $sum / $numelem]
}

proc calc_std {input} {
  set numelem [llength $input]
  set mean [calc_mean $input]
  set sumdev 0
  foreach elem $input {
    set dev [expr ( ($elem - $mean) * ($elem - $mean) )]
    set sumdev [expr $sumdev + $dev]
  }

  set std [expr $sumdev / $numelem]
  return $std
}

proc correct_wrapping {centersel othersel celldims} {
# make sure that othersel has been wrapped so that it is centered in the 
# same unit cell as centersel
# if not, translate it until it is

  set comvec [vecsub [measure center $centersel] [measure center $othersel]]

  set dx [lindex $comvec 0]
  set dy [lindex $comvec 1]
  set dz [lindex $comvec 2]
  set xv [lindex $celldims 0]
  set yv [lindex $celldims 1]
  set zv [lindex $celldims 2]
  set xvh [expr [lindex $celldims 0] / 2.0]
  set yvh [expr [lindex $celldims 1] / 2.0]
  set zvh [expr [lindex $celldims 2] / 2.0]
 #puts "initial dx/dy/dz is $dx $dy $dz"

  while {$dx > $xvh} {
    $othersel moveby [list $xv 0 0]
    set dx [lindex [vecsub [measure center $centersel] [measure center $othersel]] 0]
  }
  while {$dx < [expr -1 * $xvh]} {
    $othersel moveby [list [expr -1 * $xv] 0 0]
    set dx [lindex [vecsub [measure center $centersel] [measure center $othersel]] 0]
  }
  
  while {$dy > $yvh} {
    $othersel moveby [list 0 $yv 0]
    set dy [lindex [vecsub [measure center $centersel] [measure center $othersel]] 1]
  }
  while {$dy < [expr -1 * $yvh]} {
    $othersel moveby [list 0 [expr -1 * $yv] 0]
    set dy [lindex [vecsub [measure center $centersel] [measure center $othersel]] 1]
  }

  while {$dz > $zvh} {
    $othersel moveby [list 0 0 $zv]
    set dz [lindex [vecsub [measure center $centersel] [measure center $othersel]] 2]
  }
  while {$dz < [expr -1 * $zvh]} {
    $othersel moveby [list 0 0 [expr -1 * $zv]]
    set dz [lindex [vecsub [measure center $centersel] [measure center $othersel]] 2]
  }
 #puts "final dx/dy/dz is $dx $dy $dz"

}

proc calc_comvec_vs_t {mymolid censeg oseg} {
# given a pair of segment names, return the center of mass vector at 
# each timepoint between them
# We alter the components as necessary to enforce proper wrapping

  pbc wrap -allframes -center com -centersel "protein and segname $censeg" -compound segid -molid $mymolid

  set retvec [list]

  set censel [atomselect $mymolid "segname $censeg"]
  set osel [atomselect $mymolid "segname $oseg"]

  for {set t 0} {$t < [molinfo $mymolid get numframes]} {incr t} {
    $censel frame $t
    $osel frame $t
    set xdim [molinfo $mymolid get a frame $t]
    set ydim [molinfo $mymolid get b frame $t]
    set zdim [molinfo $mymolid get c frame $t]
    correct_wrapping $censel $osel [list $xdim $ydim $zdim]
    lappend retvec [vecsub [measure center $censel weight mass] [measure center $osel weight mass]]
  }

  $censel delete
  $osel delete

  return $retvec
}

proc identify_contact_residues {molid framenum cutoff seg1 seg2} {
# Identify pairs of residues in contact with each other, given a cutoff and pair of segnames
# Returns a list of resid-resid pairs for residue ids from seg1 and seg2

  set sel1 [atomselect $molid "noh and segname $seg1 and pbwithin $cutoff of segname $seg2" frame $framenum]
  set sel2 [atomselect $molid "noh and segname $seg2 and pbwithin $cutoff of segname $seg1" frame $framenum]

  set all1 [atomselect $molid "segname $seg1" frame $framenum]
  set all2 [atomselect $molid "segname $seg2" frame $framenum]

  puts "A"
  # do the necessary wrapping
  set xdim [molinfo $molid get a frame $framenum]
  set ydim [molinfo $molid get b frame $framenum]
  set zdim [molinfo $molid get c frame $framenum]
  correct_wrapping $all1 $all2 [list $xdim $ydim $zdim]
  puts "B"

  $sel1 update
  $sel2 update

  puts "C"
  set residlist1 [lsort -unique [$sel1 get resid]]
  set residlist2 [lsort -unique [$sel2 get resid]]

  puts $residlist1
  puts $residlist2

  #puts "contact results: [measure contacts $cutoff $sel1 $sel2]"
  #foreach {indexlist1 indexlist2} [measure contacts $cutoff $sel1 $sel2] {
  #  if {$indexlist1 == {}} {
  #    return [list]
  #  }
  #  echo "$indexlist1 $indexlist2"
  #  set contactsel1 [atomselect $molid "index $indexlist1"]
  #  set contactsel2 [atomselect $molid "index $indexlist2"]
  #}

  set residpairs [list]

  foreach resid1 $residlist1 {
    foreach resid2 $residlist2 {

      set contactsel [atomselect $molid "segname $seg1 and noh and resid $resid1 and pbwithin $cutoff of (segname $seg2 and noh and resid $resid2)"]

      if {[$contactsel num] > 0} {
        lappend residpairs [list $resid1 $resid2]
      }

      $contactsel delete
    }
  }

  $sel1 delete
  $sel2 delete


  return [lsort -unique -increasing $residpairs]

}

proc build_contact_matrices {molid outprefix cutoff} {
# build a contact map for each of the 14 crystallographic contacts
# for each timestep in the trajectory, and write it to $outprefix_conmap.dat


  set allprot [atomselect $molid protein]
  set allprotsegs [lsort -unique [$allprot get segname]]
  $allprot delete

  set neighbor_keyvecs [define_adjacent_monomers $molid P18 10]

  set protsegs_neighborsegs [list]
  foreach seg $allprotsegs {
    #puts "Working on $seg"
    lappend protsegs_neighborsegs [identify_adjacent_monomers $molid $seg $neighbor_keyvecs 10 P18]
  }

  # The contact maps are stored in a sparse m x m x n array
  # m is the number of residues per monomer, n the neighbors per monomer,
  # and t the number of timesteps
  # Each element contains a count of the number of monomers for which a
  # given contact is formed
  # we build the array one timestep at a time, and write each timestep to a file

  # First build up the array
  array set datarray {}

  set tmpseg [atomselect $molid "segname P1 and alpha"]
  set m [llength [$tmpseg get resid]]
  $tmpseg delete

  set n [llength $neighbor_keyvecs]
  set t [molinfo $molid get numframes]

  
  set ostr [open ${outprefix}_conmap.dat w]
  #puts $ostr "# $m x $m x $n x $t"
  puts $ostr "# $m x $m x $n x 2"

  # Now go through the frames and increment entries as needed
  #for {set k 0} {$k < $t} {incr k} {}
  foreach k [list 0 [expr $t - 1]] {
    if {$k % 100 == 0} {
      puts "Working on frame $k of $t..."
    }
    array unset datarray
    array set datarray {}
    for {set j 0} {$j < $n} {incr j} {
      for {set seg 0} {$seg < [llength $allprotsegs]} {incr seg} {

        set donekeys [list]

        # do necessay wrapping for this frame/segment pair
        pbc wrap -first $k -last $k -center com -centersel "protein and segname [lindex $allprotsegs $seg]" -compound segid -molid $molid
        set xdim [molinfo $molid get a frame $k]
        set ydim [molinfo $molid get b frame $k]
        set zdim [molinfo $molid get c frame $k]
        set sel1 [atomselect $molid "segname [lindex $allprotsegs $seg]" frame $k]
        set sel2 [atomselect $molid "segname [lindex $protsegs_neighborsegs $seg $j]" frame $k]
        correct_wrapping $sel1 $sel2 [list $xdim $ydim $zdim]
        puts "Working on seg $seg"
        puts [$sel1 num]
        puts [$sel2 num]
        set mycon [measure contacts $cutoff $sel1 $sel2]
        $sel1 delete
        $sel2 delete
        set inds1 [lindex $mycon 0]
        set inds2 [lindex $mycon 1]
        foreach ind1 $inds1 ind2 $inds2 {
          set atom1 [atomselect $molid "index $ind1"]
          set atom2 [atomselect $molid "index $ind2"]
          set res1 [join [$atom1 get resid]]
          set res2 [join [$atom2 get resid]]
          $atom1 delete
          $atom2 delete
          set key "$res1 $res2 $j"
          if {[lsearch $donekeys $key] >= 0} {
            continue
          }

          lappend donekeys $key

          puts "Working on $key"
          if {[array get datarray $key] == {}} {
            #puts "Found a contact for residues $res1 $res2 for segs [lindex $allprotsegs $seg] [lindex $protsegs_neighborsegs $seg $j]] (key $key)"
            array set datarray [list $key 1]
          } else {
            set currval [lindex [array get datarray $key] 1]
            set newval [expr $currval + 1]
            #puts "New value is $newval for $key"
            array set datarray [list $key $newval]
          }
        }
#        foreach {residpair} [identify_contact_residues $molid $k $cutoff [lindex $allprotsegs $seg] [lindex $protsegs_neighborsegs $seg $j]] {
#          set res1 [lindex $residpair 0]
#          set res2 [lindex $residpair 1]
#          set key "$res1 $res2 $j"
#          puts "Working on $key"
#          if {[array get datarray $key] == {}} {
#            #puts "Found a contact for residues $res1 $res2 for segs [lindex $allprotsegs $seg] [lindex $protsegs_neighborsegs $seg $j]] (key $key)"
#            array set datarray [list $key 1]
#          } else {
#            set currval [lindex [array get datarray $key] 1]
#            set newval [expr $currval + 1]
#            #puts "New value is $newval for $key"
#            array set datarray [list $key $newval]
#          }
#        }
      }
    }

    for {set j 0} {$j < $n} {incr j} {
      for {set res1 1} {$res1 <= $m} {incr res1} {
        for {set res2 1} {$res2 <= $m} {incr res2} {
          set key "$res1 $res2 $j"
          puts "Looking for key |$key|"
          if {[array get datarray $key] == {}} {
            set count 0
          } else {
            set count [lindex [array get datarray $key] 1]
          }
          if {$count > 0} {
            puts "Non-zero count $count for $key"
          }
          puts -nonewline $ostr "[expr $count / double([llength $allprotsegs])] "
        }
      }
    }
    puts $ostr ""

  }

  close $ostr
}

proc do_all_analysis {pdbfile dcdfile outprefix {step 1000}} {
  set mymol [mol new $pdbfile waitfor all]
  molinfo top set a 91.8
  molinfo top set b 81.4
  molinfo top set c 90.3
  mol addfile $dcdfile step $step waitfor all
  build_contact_matrices $mymol $outprefix 5.0
  #calc_avg_lattice_vectors $mymol $outprefix
}

proc draw_arrow_for_contact {molid centerseg interaction drawmol color} {
  source /net/cottus/u2/cliu/note/script/pbcbox/porcplot.tcl

  set allsel [atomselect $molid protein]
  set refpos [$allsel get {x y z}]
  set allsegs [lsort -unique [$allsel get segname]]

  graphics $drawmol color $color

  set neighbor_keyvecs [define_adjacent_monomers $molid P18 10]
  set protsegs_neighborsegs [list]
  foreach seg $allsegs {
    #puts "Working on $seg"
    lappend protsegs_neighborsegs [identify_adjacent_monomers $molid $seg $neighbor_keyvecs 10 P18]
  }

  set myneighbor [lindex $protsegs_neighborsegs $centerseg $interaction]

  set mysel [atomselect $molid "segname P[expr $centerseg + 1]"]
  set neighborsel [atomselect $molid "segname $myneighbor"]

  puts [$mysel num]
  puts [$neighborsel num]

  drawarrow [measure center $neighborsel weight mass] [measure center $mysel weight mass] $drawmol

  $allsel set {x y z} $refpos
  $allsel delete
}

proc get_vectors_for_contacts {molid drawmol outfile} {
# for each contact class, return a list of vectors for that contact

  set arrowpairs [list {0 7} {1 6} {2 5} {3 10} {4 13} {8 12} {9 11} ]

  set ostr [open $outfile "w"]
  puts $ostr "# centermonomer othermonomer inttype distance"

  set allsel [atomselect $molid protein]
  set refpos [$allsel get {x y z}]
  set allsegs [lsort -unique [$allsel get segname]]

  set neighbor_keyvecs [define_adjacent_monomers $molid P18 10]
  set protsegs_neighborsegs [list]
  foreach seg $allsegs {
    puts "Working on $seg"
    lappend protsegs_neighborsegs [identify_adjacent_monomers $molid $seg $neighbor_keyvecs 10 P18]
  }

  for {set i 0} {$i < 48} {incr i} {
    set centerseg [lindex $allsegs $i]

    set mysel [atomselect $molid "segname $centerseg"]
    pbc wrap -first 0 -last 0 -center com -centersel "protein and segname $centerseg" -compound segid -molid $molid

    for {set j 0} {$j < 7} {incr j} {
      set ints [lindex $arrowpairs $j] 
      set a [lindex $ints 0]
      set b [lindex $ints 1]

      set myneighbor [lindex $protsegs_neighborsegs $i $b]
      set neighborsel [atomselect $molid "segname $myneighbor"]
      correct_wrapping $mysel $neighborsel [list 91.8 81.4 90.3]
      set myvec [vecsub [measure center $neighborsel weight mass] [measure center $mysel weight mass]]
      puts $ostr "$centerseg $myneighbor $ints $myvec"
      $neighborsel delete

    }
    $allsel set {x y z} $refpos
  }

  $allsel delete
  close $ostr
}

proc draw_arrows_for_contacts {molid drawmol} {
  source /net/cottus/u2/cliu/note/script/pbcbox/porcplot.tcl

  set arrowpairs [list {0 7} {1 6} {2 5} {3 10} {4 13} {8 12} {9 11} ]

  set allsel [atomselect $molid protein]
  set refpos [$allsel get {x y z}]
  set allsegs [lsort -unique [$allsel get segname]]

  set neighbor_keyvecs [define_adjacent_monomers $molid P18 10]
  set protsegs_neighborsegs [list]
  foreach seg $allsegs {
    #puts "Working on $seg"
    lappend protsegs_neighborsegs [identify_adjacent_monomers $molid $seg $neighbor_keyvecs 10 P18]
  }

  for {set i 0} {$i < 1} {incr i} {
    set centerseg $i

    set mysel [atomselect $molid "segname P[expr $centerseg + 1]"]
    pbc wrap -first 0 -last 0 -center com -centersel "protein and segname P[expr $centerseg + 1]" -compound segid -molid $molid

    for {set j 0} {$j < 7} {incr j} {
      set ints [lindex $arrowpairs $j] 
      set a [lindex $ints 0]
      set b [lindex $ints 1]

      graphics $drawmol color $j

      set myneighbor [lindex $protsegs_neighborsegs $centerseg $a]
      set neighborsel [atomselect $molid "segname $myneighbor"]
      correct_wrapping $mysel $neighborsel [list 91.8 81.4 90.3]
      drawarrow [measure center $neighborsel weight mass] [measure center $mysel weight mass] $drawmol
      $neighborsel delete

      set myneighbor [lindex $protsegs_neighborsegs $centerseg $b]
      set neighborsel [atomselect $molid "segname $myneighbor"]
      correct_wrapping $mysel $neighborsel [list 91.8 81.4 90.3]
      drawarrow [measure center $mysel weight mass] [measure center $neighborsel weight mass] $drawmol
      $neighborsel delete
    }
    $allsel set {x y z} $refpos
  }

  $allsel delete
}




proc classify_all_monomers {molid} {
  # identify which of a set of unique orientations each monomer belongs to
  # this is done based on interaction I
  # the canonical distances are in the variable examplar_orientations

  set exemplar_orientations [list {6.66147255897522 -20.349518939852715 -13.809362411499023} {-6.663661956787109 20.350919723510742 -13.820815086364746} {-6.661714971065521 -20.349956512451172 13.809578195214272} {6.666782379150391 20.34816598892212 13.81952977180481}]

  set allsel [atomselect $molid protein]
  set allsegs [lsort -unique [$allsel get segname]]
  $allsel delete

  set neighbor_keyvecs [define_adjacent_monomers $molid P18 10]
  set protsegs_neighborsegs [list]
  foreach seg $allsegs {
    #puts "Working on $seg"
    lappend protsegs_neighborsegs [identify_adjacent_monomers $molid $seg $neighbor_keyvecs 10 P18]
  }

  set retlist [list]

  foreach censeg $allsegs neighborsegs $protsegs_neighborsegs {
    set neighbor1 [lindex $neighborsegs 0]
    set censel [atomselect $molid "segname $censeg" frame 0]
    set osel [atomselect $molid "segname $neighbor1" frame 0]

    set xdim [molinfo $molid get a frame 0]
    set ydim [molinfo $molid get b frame 0]
    set zdim [molinfo $molid get c frame 0]

    correct_wrapping $censel $osel [list $xdim $ydim $zdim]
    set myvec [vecsub [measure center $osel weight mass] [measure center $censel weight mass]]

    set mindist 1000.0
    set bestclass 0

    foreach exemplar $exemplar_orientations class {A B C D} {
      set tmpdist [veclength [vecsub $exemplar $myvec]]
      if {$tmpdist < $mindist} {
        set mindist $tmpdist
        set bestclass $class
      }
    }

    lappend retlist $bestclass
  }

  return $retlist
}
