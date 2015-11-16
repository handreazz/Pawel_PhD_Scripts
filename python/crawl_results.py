import os,sys

dir='/net/chevy/raid1/nigel/amber/no_opt'

def is_valid_log_file(logfile):
  if os.path.isfile(logfile) and os.path.getsize(logfile) > 0:
    with open(logfile, 'r') as f:
      lines = f.readlines()
      # import code; code.interact(local=dict(globals(), **locals()))
      if len(lines) >7 and lines[-7] == "=========================== phenix.refine: finished ===========================\n":
        return 0
      else:
        return 1
  else:
    return 2

#haha2 = []

if __name__ == '__main__':
  good = open('success_pdb.txt','w')
  bad = open('failed_pdb.txt','w')

  i=0
  for element in os.walk(dir):
    subdir = element[0]
    pdbcode = subdir.split('/')[-1]
    if len(pdbcode) != 4:
      continue
    if 'old' in subdir:
      continue
    i +=1
    print i, pdbcode
    logfile_status_sum = 0
    for logfile in ['/%s_refine_001.log' %pdbcode, '/%s_refine_003.log' %pdbcode,
                    '/%s_refine_004.log' %pdbcode, '/%s_refine_005.log' %pdbcode]:
      logfile_status_sum += is_valid_log_file(subdir+logfile)
    #  if pdbcode == '1scz':
    #   haha2.append( [subdir+logfile, logfile_status_sum])
    if logfile_status_sum == 0:
      good.write("%s\n" %pdbcode)
    elif logfile_status_sum <8:
      bad.write("%s\n" %pdbcode)
    #if pdbcode == '1scz':
    #  haha = logfile_status_sum
  good.close()
  bad.close()
#print haha
#print haha2
