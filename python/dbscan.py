residues=[14,15,16,37,46,47,48,49,67,68,70,71,72,85,86,87,101,102,103,117,118,119]
atoms=[206,230,248,562,703,717,731,743,1022,1029,1075,1081,1088,1282,1293,1304,1510,1522,1529,1759,1766,1780]
dictionary=dict(zip(atoms,residues))
atom=1759
coords=np.genfromtxt("CartArray_:%d@%d.dat" %(dictionary[atom],atom))
N=coords.shape[0]
coords0=coords-np.mean(coords,axis=0)


from sklearn.decomposition import PCA
pca=PCA(n_components=2)
tr_coords=pca.fit_transform(coords0)
X=tr_coords

##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.1, min_samples=100).fit(X)
core_samples = db.core_sample_indices_
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


#print ("Silhouette Coefficient: %0.3f" %
#       metrics.silhouette_score(D, labels, metric='precomputed'))

##############################################################################
# Plot result
import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()

# Black removed and is used for noise instead.
colors = cycle('bgrcmybgrcmybgrcmybgrcmy')
for k, col in zip(set(labels), colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        markersize = 6
    class_members = [index[0] for index in np.argwhere(labels == k)]
    cluster_core_samples = [index for index in core_samples
                            if labels[index] == k]
    for index in class_members:
        x = X[index]
        if index in core_samples and k != -1:
            markersize = 14
        else:
            markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=markersize)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()
