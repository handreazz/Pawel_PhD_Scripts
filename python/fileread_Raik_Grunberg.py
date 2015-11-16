#!/usr/bin/env python
import sys
import glob

## input files

f_in = glob.glob('*mol2')[0]
f_out = f_in + '.corrected'

if len( sys.argv ) > 1:
    f_in = sys.argv[1]
if len( sys.argv ) > 2:
    f_out = sys.argv[2]

print "checking ", f_in


## first pass, sum up charges
r = 0

for l in open(f_in).readlines():
    try:
        cols = l.split()
        if len(cols) == 9:
            q = cols[-1]
            r += float(q)
    except:
        pass

correction = abs(round(r) / r)
print "total charge: %8.6f" % r
print "correction factor of %8.6f will be applied" % correction

## second pass, correct charges
r = 0

f = open(f_out,'w')

for l in open(f_in).readlines():
    try:
        cols = l.split()
        if len(cols) == 9:
            q_str = cols[-1]
            q = float(q_str) * correction
            r += q
            q_new = '%8.6f' % q
            q_new = q_new.strip()

            l_new = l.replace(q_str, q_new)
            f.write(l_new)
        else:
            f.write(l)
    except:
        f.write(l)

f.close()

print "corrected mol2 file written to: ", f_out
print "total charge after correction: %8.6f" % r
