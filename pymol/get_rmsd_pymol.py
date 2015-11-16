from numpy import *

codes = ['1lzn','1v7s', '1v7t', '1lzt', '2lzt', '3lzt', '4lzt' ]

f=open('pymol_rmsd_results.txt', 'w')

rmsd = zeros((7,7))
f.write('backbone\n')
for i in range(7):
  for j in range(i+1,7):
    # f.write('%s %s ' %(codes[i], codes[j]))
    cmd.delete('all')
    cmd.load('%s.pdb' %codes[i].upper(), codes[i])
    cmd.load('%s.pdb' %codes[j].upper(), codes[j])
    x = cmd.align('%s and name ca+c+n+o' %codes[i],'%s and name ca+c+n+o' %codes[j])
    # f.write('%.4f\n' %(x[0]) )
    rmsd[i,j] = x[0]
f.write('\n      1v7s   1v7t   1lzt   2lzt   3lzt   4lzt\n')
for i in range(6):
  f.write('%s ' %codes[i])
  for j in range(1,7):
    if j>i:
      f.write('%5.4f ' %rmsd[i,j])
    else:
      f.write('       ')
  f.write('\n')
mean_rmsd = sum(rmsd)/20
f.write('mean: %5.4f\n' %mean_rmsd)
f.write('\n')



rmsd = zeros((7,7))
f.write('heavy\n')
for i in range(7):
  for j in range(i+1,7):
    # f.write('%s %s ' %(codes[i], codes[j]))
    cmd.delete('all')
    cmd.load('%s.pdb' %codes[i].upper(), codes[i])
    cmd.load('%s.pdb' %codes[j].upper(), codes[j])
    x = cmd.align('%s and polymer and not resn hoh' %codes[i],'%s and polymer and not resn hoh' %codes[j])
    # f.write('%.4f\n' %(x[0]) )
    rmsd[i,j] = x[0]
f.write('\n      1v7s   1v7t   1lzt   2lzt   3lzt   4lzt\n')
for i in range(6):
  f.write('%s ' %codes[i])
  for j in range(1,7):
    if j>i:
      f.write('%5.4f ' %rmsd[i,j])
    else:
      f.write('       ')
  f.write('\n')
mean_rmsd = sum(rmsd)/20
f.write('mean: %5.4f\n' %mean_rmsd)
f.write('\n')

f.close()