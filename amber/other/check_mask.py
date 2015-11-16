from chemistry.amber.mask import AmberMask
from chemistry.amber.readparm import AmberParm
l = AmberParm('asu.prmtop')
k = AmberMask(l, ':12,41,119,125,126')
sel = k.Selected()
sel2 = k.Selection()
print sum(sel2)
for i in sel:
    print 'Selected atom %d: %s' % (i+1, l.atoms[i])

at = l.atoms[0]
at.residue
at.residue.name
at.residue.number
at.residue.idx
at.atomic_number
at.name
at.type

