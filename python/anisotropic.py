import sys
import os
import numpy as np

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
def MetricTensor(box):
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
def DotProduct(box,u,v):
  gmetr, gstar, V = MetricTensor(box)
  uv = 0
  for i in range(3):
    for j in range(3):
      uv += u[i]*v[j]*gmetr[i,j]
  return uv

#######################################################################
# Compute the reciprocal space unit cell parameters.                  #
# Arguments:                                                          #
#     box: 1x6 array of box vectors [a,b,c,alpha,beta,gamma]          #
#          Angles must be in degrees.								                  #
# Returns:                                                            #
#     recip_box: 1x6 array. Reciprocal unit cell box. Angles are in   #
#                degrees of real space unit cell.                     #
#######################################################################
def RecipBox(box):
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
def Adp2B(box, Uij):
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



if __name__ == "__main__":
  box = [27.240,31.870,34.230,88.52,108.53,111.89]
  Uij = [2066,1204,1269,44,126,191]

  box = [40.454,   87.420,   62.226,  90.00,  91.46,  90.00]
  Uij = [2610,   3636,   3359,     74,    877,    -47]

  box = np.array(box)
  Uij = np.array(Uij) * 1e-4
  B, Ueq = Adp2B(box, Uij)
  print B