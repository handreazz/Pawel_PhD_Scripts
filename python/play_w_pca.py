#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
print "\n"

#======================================================================#
#                                                                      #
#  Three different ways of doing PCA.                                  #
#                                                                      #
#======================================================================#

#LOAD DATA and ZERO MEAN
coords=genfromtxt("FracArray.dat")
coords=coords[0:100,:] #so svd doesn't crash
coords=coords-mean(coords,axis=0)
N=coords.shape[0]

#SCIKIT LEARN
print "USING SCIKIT-LEARN."
from sklearn.decomposition import PCA
pca=PCA(n_components=3)
tr_coords=pca.fit_transform(coords)
print "The explained variance:"
print pca.explained_variance_ratio_
print "The principle components:"  #by row
print pca.components_
print "The projection of the first three data points onto 1st component"
print tr_coords[0:3,0]
print "\n\n"

#DIAGONALIZE COVARIANCE
print "USING THE EIGENVALUE DECOMPOSITION OF THE COVARIANCE MATRIX"
# I scale XtX by (N-1) so that it corresponds to the normalized covariance
# matrix. But this does not affect the results here.
XtX = dot(coords.T,coords)/(N-1) #same as cov(coords.T)
print "The explained variance:"
print (linalg.eig(XtX)[0])/sum(linalg.eig(XtX)[0])
print "The principle components:" 
print linalg.eig(XtX)[1].T
print "The projection of the first three data points onto 1st component"
pc1=linalg.eig(XtX)[1][:,0]
print dot(pc1,coords[0,:]), dot(pc1, coords[1,:]), dot(pc1, coords[2,:])
#To transform all the coordinates: z.T=W.T*x.T
#tr_coords=dot(linalg.eig(XtX)[1].T,coords.T).T
#   tr_coords=dot(linalg.eig(XtX)[1].T,coords.T).T[0:3,0] will give the proje
#     of the first three data points on the 1st component
print "\n\n"






import code; code.interact(local=locals())

#SVD DATA MATRIX
print "USING THE SVD OF THE SCALED FEATURE MATRIX"
# I use coords/sqrt(N-1) which is scaled to correspond to the formula of the 
# covariance matrix (X'*X)/(N-1). This scaling does not affect U or V but only
# S. Thus to get the correct projections I need to scale S*sqrt(n-1) below.
#~ import code; code.interact(local=locals())
Y=coords / sqrt(N-1) #dot(Y.T,Y) = XtX
u,s,v=linalg.svd(Y)
print "The explained variance:"
print s[0]**2/sum(s**2), s[1]**2/sum(s**2), s[2]**2/sum(s**2)
print "The principle components:"
print v
print "The projection of the first three data points onto 1st component"
print u[0:3,0]*s[0]*sqrt(N-1)
#~ import code; code.interact(local=locals())
