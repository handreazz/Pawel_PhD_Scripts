load 4LZT.pdb, 4lzt
load 3LZT.pdb, 3lzt
align 4lzt and name ca+c+o+n, 3lzt and name ca+o+c+n
align 3lzt and polymer, 4lzt and polymer
select polymer, 4lzt
delete polymer
select p, 4lzt and polymer
hide all
show p
show sticks, p
