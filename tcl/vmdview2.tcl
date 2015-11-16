
mol new ../rmsf/1UnitCellPrmtop/pep1cell.prmtop
mol addfile average_RevSymm.mdcrd 0
mol new ../rmsf/1UnitCellPrmtop/pep1cell.pdb


set sel11 [atomselect 0 "(not hydrogen and not water and not name C N O)"]
set sel12 [atomselect 0 "backbone"]
set sel13 [atomselect 0 "resid 9 10 19 20 and not name N and not hydrogen"]
set sel14 [atomselect 0 "(resid 2 12 and not hydrogen and not name C O) or resid 1 11 and not hydrogen"]

set sel1 [atomselect 1 "(not hydrogen and not water and not name C N O)"]
set sel2 [atomselect 1 "backbone"]
set sel3 [atomselect 1 "resid 9 10 19 20 and not name N and not hydrogen"]
set sel4 [atomselect 1 "(resid 2 12 and not hydrogen and not name C O) or resid 1 11 and not hydrogen"]

mol addrep 0
mol addrep 0
mol addrep 0

mol addrep 1
mol addrep 1
mol addrep 1

color Display Background 8

###vmd is stupid and for showrep you give the molnumber first and repnumber second
mol showrep 1 0 on
mol showrep 1 1 on
mol showrep 1 2 on
mol showrep 1 3 on
mol showrep 0 0 on
mol showrep 0 1 on
mol showrep 0 2 on
mol showrep 0 3 on

#mol selupdate 2 0 on

###for modselect, etc. give repnumber first and molnumber second
mol modselect 0 0 "[$sel11 text]"
mol modselect 1 0 "[$sel12 text]"
mol modselect 2 0 "[$sel13 text]"
mol modselect 3 0 "[$sel14 text]"

mol modselect 0 1 "[$sel1 text]"
mol modselect 1 1 "[$sel2 text]"
mol modselect 2 1 "[$sel3 text]"
mol modselect 3 1 "[$sel4 text]"


mol modcolor 0 0 ColorID 16
mol modcolor 1 0 ColorID 16
mol modcolor 2 0 ColorID 16
mol modcolor 3 0 ColorID 16

mol modcolor 0 1 ColorID 3
mol modcolor 1 1 ColorID 3
mol modcolor 2 1 ColorID 3
mol modcolor 3 1 ColorID 3

mol modstyle 0 0 Licorice
mol modstyle 1 0 NewRibbons
mol modstyle 2 0 Licorice
mol modstyle 3 0 Licorice

mol modstyle 0 1 Licorice
mol modstyle 1 1 NewRibbons
mol modstyle 2 1 Licorice
mol modstyle 3 1 Licorice
