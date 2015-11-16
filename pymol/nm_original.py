from ctypes import *
from numpy import linalg,sqrt,dot,zeros,double,real,pi,sin,argsort,real
from pymol import cmd, stored
from pickle import dump
 
#~ cdll.LoadLibrary('/usr/lib64/libgmx_d.so.6')
#~ gmx_mtxio_read = CDLL('/usr/lib64/libgmx_d.so.6').gmx_mtxio_read
 #~ 
#~ def loadmtx(mtx):
  #~ nrow = c_int(0)
  #~ ncol = c_int(0)
  #~ hess = POINTER(c_double)()
#~ #  hess = POINTER(c_float)()
  #~ gmx_sparsematrix = POINTER(c_byte)()
  #~ gmx_mtxio_read(mtx, byref(nrow), byref(ncol), byref(hess), byref(gmx_sparsematrix))
  #~ ahess = zeros((nrow.value, ncol.value), dtype=double)
  #~ for i in range(nrow.value):
    #~ for j in range(ncol.value):
      #~ ahess[i,j] = hess[i*ncol.value+j]
  #~ return ahess
 
def nmgen(obj, nmid, mtx=None, amp=1., nframes=20, dump_file=False):
  """
nmgen - generate normal mode 
my reworking of an internet file that used gromacs hessian.
  """
  print "1hello there"
  nmid = int(nmid)
  amp = float(amp)
  newobj = "%s-nm_%d" % (obj, nmid)
  genwv = 0
  cmd.delete(newobj)
 
  try:
    stored.NMA[obj]
  except AttributeError:
    stored.NMA = {}
    genwv = 1
  except KeyError:
    genwv = 1
 
  if genwv or mtx:
    if not mtx:
      print "Please specify cpptraj covariance matrix file"
      return 0
    mwcvmatrix=genfromtxt(mtx)
    w2,v = linalg.eig(mwcvmatrix)
    w = sqrt(w2)*1.e12
    stored.NMA[obj] = {}
    stored.NMA[obj]['hess'] = hess
    stored.NMA[obj]['w'] = w
    stored.NMA[obj]['v'] = v
    if dump_file:
      f=open(dump_file, 'w')
      dump((mwcvmatrix,w,v), f)
      f.close()
  else:
    w = stored.NMA[obj]['w']
    v = stored.NMA[obj]['v']
 
  #~ si=argsort(w)
  #~ print "%7s%20s%20s" % ('NMID', 'f Hz', 'f cm^-1')
  #~ for i in range(w.size):
    #~ print "%7d%20.5e\t%20.0f" % (i, w[si[i]]/2./pi, w[si[i]]*5.30884e-12),
    #~ if i == nmid:
      #~ print "*"
    #~ else:
      #~ print ""
  #~ nm = real(v[:,si[nmid]])
  #~ nm *= amp/sqrt((nm**2).sum())
  #~ for ifr in range(nframes):
    #~ cmd.create(newobj, obj, 1, ifr+1)
    #~ stored.nm = nm*sin(2.*pi*ifr/nframes)
    #~ cmd.alter_state(ifr+1, newobj, "x,y,z = x+stored.nm[(ID-1)*3], y+stored.nm[(ID-1)*3+1], z+stored.nm[(ID-1)*3+2]")
#~ cmd.extend("nmgen", nmgen)
