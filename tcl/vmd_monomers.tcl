set sel1 [atomselect 0 "resid 1 to 63"]
set sel2 [atomselect 0 "resid 64 to 126"]
set sel3 [atomselect 0 "resid 127 to 189"]
set sel4 [atomselect 0 "resid 190 to 252"]
set sel5 [atomselect 0 "resid 253 to 315"]
set sel6 [atomselect 0 "resid 316 to 378"]
set sel7 [atomselect 0 "resid 379 to 441"]
set sel8 [atomselect 0 "resid 442 to 504"]
set sel9 [atomselect 0 "resid 505 to 567"]
set sel10 [atomselect 0 "resid 568 to 630"]
set sel11 [atomselect 0 "resid 631 to 693"]
set sel12 [atomselect 0 "resid 694 to 756"]

mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0

mol modselect 0 0 "[$sel1 text]"
mol modselect 1 0 "[$sel2 text]"
mol modselect 2 0 "[$sel3 text]"
mol modselect 3 0 "[$sel4 text]"
mol modselect 4 0 "[$sel5 text]"
mol modselect 5 0 "[$sel6 text]"
mol modselect 6 0 "[$sel7 text]"
mol modselect 7 0 "[$sel8 text]"
mol modselect 8 0 "[$sel9 text]"
mol modselect 9 0 "[$sel10 text]"
mol modselect 10 0 "[$sel11 text]"
mol modselect 11 0 "[$sel12 text]"

mol modcolor 0 0 ColorID 1
mol modcolor 1 0 ColorID 2
mol modcolor 2 0 ColorID 3
mol modcolor 3 0 ColorID 4
mol modcolor 4 0 ColorID 5
mol modcolor 5 0 ColorID 6
mol modcolor 6 0 ColorID 7
mol modcolor 7 0 ColorID 8
mol modcolor 8 0 ColorID 9
mol modcolor 9 0 ColorID 10
mol modcolor 10 0 ColorID 11
mol modcolor 11 0 ColorID 12

