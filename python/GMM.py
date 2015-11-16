#! /usr/bin/python

import pylab as pl
import matplotlib as mpl
import numpy as np

from sklearn import datasets
from sklearn.cross_validation import StratifiedKFold
from sklearn.mixture import GMM


residues=[14,15,16,37,46,47,48,49,67,68,70,71,72,85,86,87,101,102,103,117,118,119]
atoms=[206,230,248,562,703,717,731,743,1022,1029,1075,1081,1088,1282,1293,1304,1510,1522,1529,1759,1766,1780]
atoms=[494, 1207]
residues=[33, 79]
dictionary=dict(zip(atoms,residues))
atom=1207
coords=np.genfromtxt("CartArray_:%d@%d.dat" %(dictionary[atom],atom))
N=coords.shape[0]
coords0=coords-np.mean(coords,axis=0)

from sklearn.decomposition import PCA
pca=PCA(n_components=2)
tr_coords=pca.fit_transform(coords0)
####
tr_coords=coords


X_train=tr_coords

def make_ellipses(gmm, ax, components):
	colors=['r', 'g', 'b', 'c', 'm', 'y']
	for n in range(components):  #change to number of classes
		v, w = np.linalg.eigh(gmm._get_covars()[n][:2, :2])
		u = w[0] / np.linalg.norm(w[0])
		angle = np.arctan2(u[1], u[0])
		angle = 180 * angle / np.pi  # convert to degrees
		v *= 9
		ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],180 + angle, color=colors[n])
		ell.set_clip_box(ax.bbox)
		ell.set_alpha(0.5)
		ax.add_artist(ell)

#~ #FOUR GMM PLOTS


#~ n_classes = 3
#~ classifiers = dict((covar_type, GMM(n_components=n_classes,
                    #~ covariance_type=covar_type, init_params='wmc', n_iter=20))
                   #~ for covar_type in ['spherical', 'diag', 'tied', 'full'])
#~ n_classifiers = len(classifiers)
#~ 
#~ pl.figure(figsize=(3 * n_classifiers / 2, 6))
#~ pl.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
                   #~ left=.01, right=.99)
#~ 
#~ for index, (name, classifier) in enumerate(classifiers.iteritems()):
    #~ classifier.fit(X_train)
    #~ pred=classifier.predict(X_train)
    #~ h = pl.subplot(2, n_classifiers / 2, index + 1)
    #~ make_ellipses(classifier, h,3)
    #~ for n, color in enumerate('rgb'): #change to number of classes
        #~ data = X_train[pred == n]
        #~ pl.scatter(data[:, 0], data[:, 1], 0.8, color=color)
    #~ pl.xticks(())
    #~ pl.yticks(())
    #~ pl.title(name)
#~ pl.legend(loc='lower right', prop=dict(size=12))
#~ pl.show()


import itertools
from scipy import linalg
X=tr_coords
#PLOT INFORMATION CRITERION
lowest_bic = np.infty
bic = []
n_components_range = range(1, 7)
cv_types = ['spherical', 'tied', 'diag', 'full']
cv_types = ['full']
for cv_type in cv_types:
    for n_components in n_components_range:
        # Fit a mixture of gaussians with EM
        gmm = GMM(n_components=n_components, covariance_type=cv_type)
        gmm.fit(X)
        bic.append(gmm.bic(X))
        if bic[-1] < lowest_bic:
            lowest_bic = bic[-1]
            best_gmm = gmm
            best_type=cv_type
            best_n=n_components

print best_type
print best_n
bic = np.array(bic)
color_iter = itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y'])
clf = best_gmm
bars = []

# Plot the BIC scores
spl = pl.subplot(2, 1, 1)
for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
    xpos = np.array(n_components_range) + .2 * (i - 2)
    bars.append(pl.bar(xpos, bic[i * len(n_components_range):
                                 (i + 1) * len(n_components_range)],
                       width=.2, color=color))
pl.xticks(n_components_range)
pl.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
pl.title('BIC score per model')
xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
    .2 * np.floor(bic.argmin() / len(n_components_range))
pl.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
spl.set_xlabel('Number of components')
spl.legend([b[0] for b in bars], cv_types)
#~ import code; code.interact(local=locals())
# Plot the winner
splot = pl.subplot(2, 1, 2)
Y_ = clf.predict(X)
#~ for i, (mean, covar, color) in enumerate(zip(clf.means_, clf.covars_, color_iter)):
colors=['r', 'g', 'b', 'c', 'm', 'y']
for i in range(best_n):
    #~ v, w = linalg.eigh(covar)
    if not np.any(Y_ == i):
        continue
    make_ellipses(clf,splot, best_n)    
    pl.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=colors[i])

    #~ # Plot an ellipse to show the Gaussian component
    #~ angle = np.arctan2(w[0][1], w[0][0])
    #~ angle = 180 * angle / np.pi  # convert to degrees
    #~ v *= 4
    #~ ell = mpl.patches.Ellipse(mean, v[0], v[1], 180 + angle, color=color)
    #~ ell.set_clip_box(splot.bbox)
    #~ ell.set_alpha(.5)
    #~ splot.add_artist(ell)

#~ pl.xlim(-10, 10)
#~ pl.ylim(-3, 6)
pl.xticks(())
pl.yticks(())
#~ pl.title('Selected GMM: full model, 2 components')
pl.subplots_adjust(hspace=.35, bottom=.02)
pl.show()
