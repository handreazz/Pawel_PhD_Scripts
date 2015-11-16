#! /usr/bin/env python

# Pawel Janowski, David Case Group, Rutgers U., Jan. 2015

#=====================================================================#
# Calculate TLS parameters given a PDB file with Uij or B-factors.    #
#                                                                     #
# Arguments:                                                          #
#     -i input pdb file (if ANISOU present will use that, otherwise   #
#        uses B-factors)                                              #
#     -o prefix of output files. Prints $prefix.pdb and $prefix.dat   #
# Example usage:                                                      #
#     adp2tls.py -i 4lzt.pdb -o tls1                                  #
#######################################################################

import sys, os
import numpy as np
from numpy import linalg
import argparse
from chemistry.structure import Structure, read_PDB, write_PDB


def MetricTensor(box):
  '''
  #######################################################################
  # Compute the metric tensor and reciprocal metric tensor from unit    #
  #   cell parameters. The metric tensor (or covariant metric tensor)   #
  #   converts reciprocal basis vectors to real space (covariant) basis #
  #   vectors. It also operates on real space vectors vectors           #
  #   (contravariant components) to produce reciprocal space vectors    #
  #   (covariant components). gstar is the reciprocal metric tensor (or #
  #   contravariant metric tensor). V is the volume of the real space   #
  #   unit cell.                                                        #
  # Arguments:                                                          #
  #     box: 1x6 array of box vectors [a,b,c,alpha,beta,gamma]          #
  #          Angles must be in degrees.								                  #
  # Returns:                                                            #
  #     gmetr: 3x3 array. Metric tensor.                                #
  #     gstar: 3x3 array. Reciprocal metric tensor.                     #
  #     V: float. Volume of real space unit cell.                       #
  #######################################################################
  '''
  box=box.astype(float)
  box[3:6]=np.radians(box[3:6])
  a,b,c,alpha,beta,gamma=box[0],box[1],box[2],box[3],box[4],box[5]
  gmetr = np.zeros((3,3))
  gmetr[0,0] = a*a
  gmetr[1,1] = b*b
  gmetr[2,2] = c*c
  gmetr[0,1] = gmetr[1,0] = a*b*np.cos(gamma)
  gmetr[0,2] = gmetr[2,0] = a*c*np.cos(beta)
  gmetr[1,2] = gmetr[2,1] = b*c*np.cos(alpha)
  gstar = np.linalg.inv(gmetr)
  V = np.sqrt(np.linalg.det(gmetr))
  return gmetr, gstar, V

def DotProduct(box,u,v):
  '''
  #######################################################################
  # Compute the dot product of two vectors in any basis (could be a non #
  #   orthogonal basis.                                                 #
  # Arguments:                                                          #
  #     box: 1x6 array of box vectors [a,b,c,alpha,beta,gamma]          #
  #          Angles must be in degrees.								                  #
  #     u: 1x3 array.                                                   #
  #     v: 1x3 array.                                                   #
  # Returns:                                                            #
  #     uv: float. Dot product of u and v in basis defined by box.      #
  #######################################################################
  '''
  gmetr, gstar, V = MetricTensor(box)
  uv = 0
  for i in range(3):
    for j in range(3):
      uv += u[i]*v[j]*gmetr[i,j]
  return uv


def RecipBox(box):
  '''
  #######################################################################
  # Compute the reciprocal space unit cell parameters.                  #
  # Arguments:                                                          #
  #     box: 1x6 array of box vectors [a,b,c,alpha,beta,gamma]          #
  #          Angles must be in degrees.								                  #
  # Returns:                                                            #
  #     recip_box: 1x6 array. Reciprocal unit cell box. Angles are in   #
  #                degrees of real space unit cell.                     #
  #######################################################################
  '''
  gmetr, gstar, V = MetricTensor(box)
  recip_box = np.zeros((6))
  recip_box[0] =      np.sqrt( DotProduct(box, gstar[0:3,0], gstar[0:3,0]) )
  recip_box[1] =      np.sqrt( DotProduct(box, gstar[0:3,1], gstar[0:3,1]) )
  recip_box[2] =      np.sqrt( DotProduct(box, gstar[0:3,2], gstar[0:3,2]) )
  recip_box[3] = np.arccos( DotProduct(box, gstar[0:3,1], gstar[0:3,2]) /
                            (recip_box[1]*recip_box[2]) ) * 180/np.pi
  recip_box[4] = np.arccos( DotProduct(box, gstar[0:3,0], gstar[0:3,2]) /
                            (recip_box[0]*recip_box[2]) ) * 180/np.pi
  recip_box[5] = np.arccos( DotProduct(box, gstar[0:3,0], gstar[0:3,1]) /
                            (recip_box[0]*recip_box[1]) ) * 180/np.pi
  return recip_box

def Adp2B(box, Uij):
  '''
  #######################################################################
  # Calculate the isotropic B-factor and isotropic U_equiv given  six   #
  #   anisotropic ADPs and the unit cell parameters.                    #
  # Arguments:                                                          #
  #     box: 1x6 array of box vectors [a,b,c,alpha,beta,gamma]          #
  #          Angles must be in degrees.								                  #
  #     Uij: 1x6 array of six anisotropic displacement parameters.      #
  #          These are the ANISOU numbers divided by 10000.             #
  # Returns:                                                            #
  #     B: isotropic B-factor                                           #
  #     Ueq: isotropic U_equiv                                          #
  #######################################################################
  '''
  recip_box = RecipBox(box)
  Ueq = Uij[0]*box[0]*box[0]*recip_box[0]*recip_box[0] + \
        Uij[1]*box[1]*box[1]*recip_box[1]*recip_box[1] + \
        Uij[2]*box[2]*box[2]*recip_box[2]*recip_box[2] + \
      2*Uij[5]*box[0]*box[1]*recip_box[0]*recip_box[1]*np.cos(box[5]*np.pi/180) + \
      2*Uij[4]*box[0]*box[2]*recip_box[0]*recip_box[2]*np.cos(box[4]*np.pi/180) + \
      2*Uij[3]*box[1]*box[2]*recip_box[1]*recip_box[2]*np.cos(box[3]*np.pi/180)
  Ueq /=3
  B = Ueq*8*np.pi*np.pi
  return B, Ueq

def B2Adp(Bfactor):
  Uij = np.zeros((6))
  U = Bfactor*3/8/np.pi/np.pi
  Uij[0:3] = np.array([U,U,U])
  return Uij

def set_A(pdb, covariance=None, w=1):
  '''
  A is a 6Nx20 matrix. For each atom, sets six rows of matrix A with
  the TLS coefficients for an atom located at position x,y,z with
  least-squares weight w. This is according to eq 5 in Winn et al.,
  "Use of TLS parameters...", Acta Cryst D, 2000. eq 1 in Painter and
  Merritt, "Optimal description of a protein structure...", Acta Cryst
  D, 2006
  '''
  # create zeros matrix
  natoms = len(pdb.atoms)
  A = np.zeros((natoms * 6, 20))

  ## use label indexing to avoid confusion!
  T11, T22, T33, T12, T13, T23, L11, L22, L33, L12, L13, L23, \
        S1133, S2211, S12, S13, S23, S21, S31, S32 = \
        (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)

  for i, atom in enumerate(pdb.atoms):
    # coordinates
    x, y, z,  = atom.xx, atom.xy, atom.xz
    xx = x*x
    yy = y*y
    zz = z*z
    xy = x*y
    xz = x*z
    yz = y*z

    ## indices of the components of U
    U11 = i*6
    U22 = i*6 + 1
    U33 = i*6 + 2
    U12 = i*6 + 3
    U13 = i*6 + 4
    U23 = i*6 + 5

    # populate A
    A[U11, T11] = w * 1.0
    A[U11, L22] = w *        zz
    A[U11, L33] = w *        yy
    A[U11, L23] = w * -2.0 * yz
    A[U11, S31] = w * -2.0 *  y
    A[U11, S21] = w *  2.0 *  z

    A[U22, T22] = w * 1.0
    A[U22, L11] = w *        zz
    A[U22, L33] = w *        xx
    A[U22, L13] = w * -2.0 * xz
    A[U22, S12] = w * -2.0 *  z
    A[U22, S32] = w *  2.0 *  x

    A[U33, T33] = w * 1.0
    A[U33, L11] = w *        yy
    A[U33, L22] = w *        xx
    A[U33, L12] = w * -2.0 * xy
    A[U33, S23] = w * -2.0 *  x
    A[U33, S13] = w *  2.0 *  y

    A[U12, T12]   = w * 1.0
    A[U12, L33]   = w * -xy
    A[U12, L23]   = w *  xz
    A[U12, L13]   = w *  yz
    A[U12, L12]   = w * -zz
    A[U12, S2211] = w *   z
    A[U12, S31]   = w *   x
    A[U12, S32]   = w *  -y

    A[U13, T13]   = w * 1.0
    A[U13, L22]   = w * -xz
    A[U13, L23]   = w *  xy
    A[U13, L13]   = w * -yy
    A[U13, L12]   = w *  yz
    A[U13, S1133] = w *   y
    A[U13, S23]   = w *   z
    A[U13, S21]   = w *  -x

    A[U23, T23]   = w * 1.0
    A[U23, L11]   = w * -yz
    A[U23, L23]   = w * -xx
    A[U23, L13]   = w *  xy
    A[U23, L12]   = w *  xz
    A[U23, S2211] = w *  -x
    A[U23, S1133] = w *  -x
    A[U23, S12]   = w *   y
    A[U23, S13]   = w *  -z
  return A

def set_B(pdb, covariance=None, w=1):
  """
  B is 6N*1. For each atom, sets the six rows of vector b with the
  experimental/target anisotropic ADP values U with weight w.
  """
  natoms = len(pdb.atoms)
  if covariance:
    exit(1)
  else:
    B = np.zeros((natoms*6))
    for i, atom in enumerate(pdb.atoms):
      if atom.anisou is None:
        atom.anisou = B2Adp(atom.bfactor)
      B[i*6:i*6+6] = atom.anisou
  return B

def solve_SVD(A,B):
    """Solve Ax=B for x."""
    ## solve by SVD
    U, W, Vt = np.linalg.svd(A, full_matrices=0)

    V  = np.transpose(Vt)
    Ut = np.transpose(U)

    ## analyze singular values and generate smallness cutoff
    cutoff = max(W) * 1E-10

    ## make W
    dim_W = len(W)
    Wi = np.zeros((dim_W, dim_W), float)

    for i in range(dim_W):
        if W[i]>cutoff:
            Wi[i,i] = 1.0 / W[i]
        else:
            #print "SVD: ill conditioned value %d=%f" % (i, W[i])
            Wi[i,i] = 0.0

    ## solve for x
    UtB  = np.dot(Ut, B)
    WUtB = np.dot(Wi, UtB)
    x    = np.dot(V, WUtB)
    return x

def write_TLS(x, prefix):
  ## use label indexing to avoid confusion!
  T11, T22, T33, T12, T13, T23, L11, L22, L33, L12, L13, L23, \
  S1133, S2211, S12, S13, S23, S21, S31, S32 = \
    (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)

  T = np.array([ [ X[T11], X[T12], X[T13] ],
                    [ X[T12], X[T22], X[T23] ],
                    [ X[T13], X[T23], X[T33] ] ])

  L = np.array([ [ X[L11], X[L12], X[L13] ],
                    [ X[L12], X[L22], X[L23] ],
                    [ X[L13], X[L23], X[L33] ] ])

  S22 = 2.0*X[S2211]/3.0 + X[S1133]/3.0
  S11 = S22 - X[S2211]
  S33 = S11 - X[S1133]
  S = np.array([ [    S11, X[S12], X[S13] ],
                    [ X[S21],    S22, X[S23] ],
                    [ X[S31], X[S32],    S33 ] ])

  f = open("%s.dat" %prefix, 'w')
  f.write('REFMAC\n\n')
  f.write('TLS\n')
  f.write('RANGE \'%s%4d.\' \'%s%4d.\' ALL\n' %(chain, resid1, chain, resid2))
  f.write('ORIGIN\n')
  f.write('T  %9.4f*6\n' %(T[1,1], T[2,2], T[3,3], T[1,2], T[1,3], T[2,3]))
  f.write('L  %9.4f*6\n' %(U[1,1], U[2,2], U[3,3], U[1,2], U[1,3], U[2,3]))
  f.write('S  %9.4f*9\n' %(S[1,1], S[1,2], S[1,3], S[2,1], S[2,2], S[2,3], S[3,1], S[3,2], S[3,3]))
  f.close()
  return 0

def calc_ADP_from_TLS(x,A,B):
  UTLS = np.dot(A, x)
  D = UTLS - B
  TLS_residual = np.dot(D, D)
  return UTLS,TLS_residual

def run(infile, prefix, covariance):
  # read in pdb file (parmed)
  pdb = read_PDB(infile)
  if covariance:
    A = set_A(pdb, covariance=covariance)
    # set B
    B = set_B(pdb, covariance=covariance)
  else:
    # set A
    A = set_A(pdb, covariance=covariance)
    # set B
    B = set_B(pdb, covariance=covariance)
  import code; code.interact(local=dict(globals(), **locals()))
  # solve Ax=B
  x = solve_SVD(A,B)
  # calc new ADP and residual and print residual
  UTLS, TLS_residual = calc_ADP_from_TLS(x,A,B)
  print "The ADP TLS residual is %6.4f." %TLS_residual
  # write tls file
  write_TLS(x, prefix)

  # write out pdb file(parmed) plug in UTLS
  out_pdb = pdb
  # for i,atom in enumerate(atomlist):
  #   for Uij in range(6):
  #   atom.UIJ[Uij] = UTLS[i*6+Uij]
  # calculate iso Bfactor from Uij (matlab)
  write_PDB(out_pdb, "%s.pdb" %prefix)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--infile", help="input PDB file (min 4 atoms).")
  parser.add_argument("-o", "--prefix", help="prefix for output .pdb and .dat files", default="out")
  parser.add_argument("-cov", "--covariance", help="full covariance matrix put out by ccptraj", default=None)
  args = parser.parse_args()
  if not args.infile:
    parser.print_help()
    sys.exit(1)
  assert os.path.isfile(args.infile), "ERROR: input PDB file not found!"
  if args.covariance:
    assert os.path.isfile(args.covariance), "ERROR: covariance matrix file file not found!"
  run(args.infile, args.prefix, args.covariance)

