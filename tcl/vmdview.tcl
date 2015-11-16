set cell 23

set last [expr $cell*20]

set sel11 [atomselect 0 "resid [expr $last-20] to [expr $last] or resid [expr $last-200] to [expr $last-180]"]
set sel12 [atomselect 0 "resid [expr $last-9] [expr $last-8] and not hydrogen"]
set sel13 [atomselect 0 "water and not hydrogen and within 10 of resid [expr $last-1]"]

set sel1 [atomselect 1 "resid [expr $last-20] to [expr $last] or resid [expr $last-200] to [expr $last-180]"]
#set sel1 [atomselect 1 "resid [expr $last-20] to [expr $last]"]
set sel2 [atomselect 1 "resid [expr $last-9] [expr $last-8] and not hydrogen or resid [expr $last-12] [expr $last-12] and not hydrogen"]
set sel3 [atomselect 1 "water and not hydrogen and within 10 of resid [expr $last-1]"]

#mol addrep 0
#mol addrep 0

#mol addrep 1r
#mol addrep 1

mol modselect 0 0 "[$sel11 text]"
mol modselect 1 0 "[$sel12 text]"
mol modselect 2 0 "[$sel13 text]"

mol modselect 0 1 "[$sel1 text]"
mol modselect 1 1 "[$sel2 text]"
mol modselect 2 1 "[$sel3 text]"

mol modcolor 0 0 Name
mol modcolor 1 0 ColorID 1
mol modcolor 2 0 ResName

mol modcolor 0 1 ColorID 0
mol modcolor 1 1 ColorID 3
mol modcolor 2 1 ColorID 4

mol modstyle 0 0 Trace
mol modstyle 1 0 CPK
mol modstyle 2 0 CPK

mol modstyle 0 1 Trace
mol modstyle 1 1 CPK
mol modstyle 2 1 CPK
