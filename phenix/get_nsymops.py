
import os, sys

pdbs_c = []
pdbs = []
with open('mtz.txt', 'r') as f:
  for line in f.readlines():
    pdbs_c.append(line.strip()[0:4])

for pdb in pdbs_c:
  os.chdir(pdb)
  if os.path.isfile('Summary_%s.dat' %pdb):
    with open('Summary_%s.dat' %pdb) as f:
      lines = f.readlines()
      if len(lines) == 21:
        pdbs.append(pdb)
  os.chdir('..')
print "Total complete refines:\n  %d\n" %len(pdbs)


of = open('nsymops.dat', 'w')
for pdb in pdbs:
  os.chdir(pdb)
  with open('%s.pdb' %pdb, 'r') as f:
    for line in f.readlines():
      if line.startswith('CRYST'):
        symop_name = line[55:68].strip()
        break
  print symop_name
  from cctbx.sgtbx import space_group_info
  i=space_group_info(symop_name)
  space_group=i.group()
  assert (space_group.n_smx() == len(list(space_group.smx())))
  of.write('%s %2d\n' %(pdb, space_group.n_smx()))
  # import code ; code.interact(local=dict(globals(), **locals()))
  os.chdir('..')
of.close()