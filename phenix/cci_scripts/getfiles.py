import os, sys




o = open('files_to_get.txt','w')
with open('success_pdb.txt') as f:
  n=0
  for l in f:
    #if n ==100:
    #  break
    code = l.strip()
    code_mid = code[1:3]
    dir = '/net/chevy/raid1/nigel/amber/no_opt/%s/%s/' %(code_mid, code)

    #target = '%s/%s.pdb' %(dir, code)
    #if os.path.isfile(target):
    #  if os.path.islink(target):
    #    target = os.readlink(target)
    #  o.write('%s\n' %target.split('/net/chevy/raid1/nigel/amber/no_opt/')[1])
    #else:
    #  print "pdb not found: %s" %target

    #target = '%s/%s.mtz' %(dir, code)
    #if os.path.isfile(target):
    #  if os.path.islink(target):
    #    target = os.readlink(target)
    #  o.write('%s\n' %target.split('/net/chevy/raid1/nigel/amber/no_opt/')[1])
    #else:
    #  print "mtz not found: %s" %target

    for target in ['%s/%s_refine_001.log' %(dir,code),
                   '%s/%s_refine_003.log' %(dir,code),
                   '%s/%s_refine_004.log' %(dir,code),
                   '%s/%s_refine_005.log' %(dir,code),
                   '%s/%s_refine_001.pdb' %(dir,code),
                   '%s/%s_refine_003.pdb' %(dir,code),
                   '%s/%s_refine_004.pdb' %(dir,code),
                   '%s/%s_refine_005.pdb' %(dir,code)]:
      if os.path.isfile(target):
        o.write('%s\n' %target.split('/net/chevy/raid1/nigel/amber/no_opt/')[1])
      else:
        print "out not found: %s" %target
    n +=1
