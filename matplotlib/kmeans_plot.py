#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pylab as pl


from sklearn import datasets
from sklearn.cross_validation import StratifiedKFold
from sklearn.mixture import GMM

residues=[14,15,16,37,46,47,48,49,67,68,70,71,72,85,86,87,101,102,103,117,118,119]
atoms=[206,230,248,562,703,717,731,743,1022,1029,1075,1081,1088,1282,1293,1304,1510,1522,1529,1759,1766,1780]

# all residues not on high b-factor
#~ residues=[8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21,
 #~ 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40,
 #~ 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
 #~ 63, 64, 65, 66, 69, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 88,
 #~ 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 104, 105, 106, 107, 
 #~ 108, 109, 110, 111, 112, 113, 114, 115, 116]
 #~ 
 #~ 
#~ atoms=[118, 137, 147, 157, 167, 184, 255, 
 #~ 274, 286, 300, 321, 345, 352, 373, 384, 403, 410, 424, 448, 464, 474, 
 #~ 484, 494, 516, 536, 551, 576, 596, 610, 624, 641, 651, 665, 679, 750, 
 #~ 761, 775, 787, 808, 815, 834, 853, 870, 889, 903, 914, 938, 962, 986, 
 #~ 996, 1010, 1053, 1099, 1123, 1137, 1156, 1166, 1180, 1207, 1213, 1223, 
 #~ 1234, 1244, 1263, 1316, 1335, 1349, 1359, 1370, 1386, 1400, 1410, 1420, 
 #~ 1442, 1464, 1483, 1499, 1543, 1550, 1567, 1581, 1591, 1615, 1631, 1641, 
 #~ 1665, 1689, 1703, 1727, 1737]
#~ 
#~ residues=[103]
#~ atoms=[1529]
residues=[8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21]
atoms=[118, 137, 147, 157, 167, 184, 255, 274, 286, 300, 321]

dictionary=dict(zip(atoms,residues))

for atom in atoms:
	coords=genfromtxt("CartArray_:%d@%d.dat" %(dictionary[atom],atom))
	#~ coords=genfromtxt("FracArray.dat")
	coords=coords[::10,:] #filter every tenth frame
	from sklearn.decomposition import PCA
	pca=PCA(n_components=3)
	coords=pca.fit_transform(coords)
	pc1=pca.components_[0]
	pc2=pca.components_[1]
	#~ pc3=pca.components_[2]
	var1=pca.explained_variance_ratio_[0]
	var2=pca.explained_variance_ratio_[1]
	#~ var3=pca.explained_variance_ratio_[2]

	from scipy.cluster import vq
	white_coords=vq.whiten(coords)
	centroids,dist = vq.kmeans(white_coords,2)
	code, tmp = vq.vq(white_coords,centroids)
	cluster1=coords[code==0]
	cluster2=coords[code==1]
	means=vstack([mean(cluster1,axis=0), mean(cluster2,axis=0)])


	centroids3,dist3 = vq.kmeans(white_coords,3)
	code, tmp = vq.vq(white_coords,centroids3)
	cluster31=coords[code==0]
	cluster32=coords[code==1]
	cluster33=coords[code==2]
	means3=vstack([mean(cluster31,axis=0), mean(cluster32,axis=0),mean(cluster33,axis=0)])


	#####################################
	# GENERAL PLOT SETTINGS             #
	#####################################
	from matplotlib.font_manager import fontManager, FontProperties
	font=FontProperties(size=10)
	plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
	plt.rc('axes',linewidth=4)
	plt.rc('legend', fontsize=20)
	colors=['#F86606',\
	 '#CC0000', \
	 '#F3EF02', \
	 '#5DF304', \
	 '#4E9A06', \
	 '#C4A000', \
	 '#729FCF', \
	 '#0618F4', \
	 '#06EFF4', \
	 '#A406F4', \
	 '#F4069D', \
	 '#936F70']  
	 
	 
	########################################################################
	###                                                                  ###
	### 2D and 3D scatter plots of com shifts relative to crystal        ###
	### Different color for each ASU                                     ###
	###                                                                  ###
	########################################################################
	fig=plt.figure(figsize=(16, 12))
	fig.suptitle('4lzt :%d@%d spatial clustering' %(dictionary[atom],atom), fontsize=16)
	fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)

	ax = fig.add_subplot(2,2,1)
	ax.scatter(coords[:,0],coords[:,1],marker='o', alpha=.99, facecolor='r', s=2, edgecolors='none')
	plt.xlim(( mean(coords,axis=0)[0]-3.0, mean(coords,axis=0)[0]+3.0 ))
	plt.ylim(( mean(coords,axis=0)[1]-3.0, mean(coords,axis=0)[1]+3.0 ))
	plt.xlabel('1st PC (%4.2f, %4.2f, %4.2f) (%2d%% of variance)' %(pc1[0], pc1[1], pc1[2], int(var1*100)),labelpad=5)
	plt.ylabel('2nd PC (%4.2f, %4.2f, %4.2f) (%2d%% of variance)' %(pc2[0], pc2[1], pc2[2], int(var2*100)),labelpad=5)
	ax.grid(True)
	font=FontProperties(size=12)


	ax = fig.add_subplot(2,2,2)
	ax.scatter(cluster1[:,0],cluster1[:,1],c=colors[0],marker='o',s=2,edgecolors='none',label="centroid (%5.2f %5.2f ). Size %d" %(means[0,0], means[0,1], cluster1.shape[0]) )
	ax.scatter(cluster2[:,0],cluster2[:,1],c=colors[9],marker='o',s=2,edgecolors='none',label="centroid (%5.2f %5.2f ). Size %d" %(means[1,0], means[1,1], cluster2.shape[0]) )
	ax.scatter(means[:,0],   means[:,1],   c='k', marker='*', s=60, edgecolors='k', label=None)
	plt.xlabel('1st PC',labelpad=5)
	plt.ylabel('2nd PC',labelpad=5)
	plt.xlim(( mean(coords,axis=0)[0]-3.0, mean(coords,axis=0)[0]+3.0 ))
	plt.ylim(( mean(coords,axis=0)[1]-3.0, mean(coords,axis=0)[1]+3.0 ))
	ax.grid(True)
	font=FontProperties(size=14)
	plt.legend(bbox_to_anchor=(0, 0, .99, .99),prop=font,ncol=1)
	
	
	def make_ellipses(gmm, ax, components):
		colors=['r', 'g', 'b', 'c', 'm', 'y']
		for n in range(components):  #change to number of classes
			v, w = linalg.eigh(gmm._get_covars()[n][:2, :2])
			u = w[0] / linalg.norm(w[0])
			angle = arctan2(u[1], u[0])
			angle = 180 * angle / pi  # convert to degrees
			v *= 9
			ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],180 + angle, color=colors[n])
			ell.set_clip_box(ax.bbox)
			ell.set_alpha(0.3)
			ax.add_artist(ell)
		
	import itertools
	from scipy import linalg
	X=coords
	#PLOT INFORMATION CRITERION
	lowest_bic = infty
	bic = []
	n_components_range = range(1, 7)
	cv_types = ['spherical', 'tied', 'diag', 'full']
	cv_types = ['spherical']
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
	print atom, dictionary[atom]
	#~ print best_type
	print best_n
	bic = array(bic)
	color_iter = itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y'])
	clf = best_gmm
	bars = []

	# Plot the BIC scores
	spl = fig.add_subplot(2, 2, 3)
	for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
		xpos = array(n_components_range) + .2 * (i - 2)
		bars.append(pl.bar(xpos, bic[i * len(n_components_range):
									 (i + 1) * len(n_components_range)],
						   width=.2, color=color))
	pl.xticks(n_components_range)
	pl.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
	pl.title('BIC score per model')
	xpos = mod(bic.argmin(), len(n_components_range)) + .65 +\
		.2 * floor(bic.argmin() / len(n_components_range))
	pl.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
	spl.set_xlabel('Number of components',labelpad=5)
	#~ spl.legend([b[0] for b in bars], cv_types)
	#~ import code; code.interact(local=locals())
	
	
	# Plot the winner
	splot = fig.add_subplot(2, 2, 4)
	Y_ = clf.predict(X)
	#~ for i, (mean, covar, color) in enumerate(zip(clf.means_, clf.covars_, color_iter)):
	colors=['r', 'g', 'b', 'c', 'm', 'y']
	for i in range(best_n):
		#~ v, w = linalg.eigh(covar)
		if not any(Y_ == i):
			continue
		make_ellipses(clf,splot, best_n)    
		pl.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=colors[i],label="Cent.=(%5.2f %5.2f %5.2f) N=%d" %(clf.means_[i,0], clf.means_[i,1],clf.means_[i,2], Y_[Y_==i].shape[0]) )
	plt.legend(bbox_to_anchor=(0, 0, .99, .99),fontsize=11,ncol=2)
	plt.xlim(( mean(coords,axis=0)[0]-3.0, mean(coords,axis=0)[0]+3.0 ))
	plt.ylim(( mean(coords,axis=0)[1]-3.0, mean(coords,axis=0)[1]+3.0 ))
    #~ # Plot an ellipse to show the Gaussian component
    #~ angle = arctan2(w[0][1], w[0][0])
    #~ angle = 180 * angle / pi  # convert to degrees
    #~ v *= 4
    #~ ell = mpl.patches.Ellipse(mean, v[0], v[1], 180 + angle, color=color)
    #~ ell.set_clip_box(splotclf.bbox)
    #~ ell.set_alpha(.5)
    #~ splot.add_artist(ell)

	#~ pl.xlim(-10, 10)
	#~ pl.ylim(-3, 6)
	#~ pl.xticks(())
	#~ pl.yticks(())
	#~ pl.title('Selected GMM: full model, 2 components')
	pl.subplots_adjust(hspace=.15)
	#~ pl.show()	

	#~ ax = fig.add_subplot(2,2,3)
	#~ ax.scatter(cluster31[:,0],cluster31[:,1],c=colors[0],marker='o',s=2,edgecolors='none',label="centroid (%5.2f %5.2f ). Size %d" %(means3[0,0], means3[0,1], cluster31.shape[0]))
	#~ ax.scatter(cluster32[:,0],cluster32[:,1],c=colors[9],marker='o',s=2,edgecolors='none',label="centroid (%5.2f %5.2f ). Size %d" %(means3[1,0], means3[1,1], cluster32.shape[0]))
	#~ ax.scatter(cluster33[:,0],cluster33[:,1],c=colors[4],marker='o',s=2,edgecolors='none',label="centroid (%5.2f %5.2f ). Size %d" %(means3[2,0], means3[2,1], cluster33.shape[0]))
	#~ ax.scatter(means3[:,0],   means3[:,1],   c='k', marker='*', s=60, edgecolors='k', label=None)
	#~ plt.xlabel('x')
	#~ plt.ylabel('y')
	#~ plt.xlim(( mean(coords,axis=0)[0]-3.0, mean(coords,axis=0)[0]+3.0 ))
	#~ plt.ylim(( mean(coords,axis=0)[1]-3.0, mean(coords,axis=0)[1]+3.0 ))
	#~ plt.legend(bbox_to_anchor=(0, 0, .99, .99),prop=font,ncol=1)
	#~ ax.grid(True)

	#ax = fig.add_subplot(2,2,4)
	#ax.scatter(cluster1[:,1],cluster1[:,2],c=colors[0],marker='o',s=2,edgecolors='none',label="centroid 1")
	#ax.scatter(cluster2[:,1],cluster2[:,2],c=colors[9],marker='o',s=2,edgecolors='none',label="centroid 2")
	#ax.scatter(means[:,1],   means[:,2],   c='k', marker='*', s=60, edgecolors='k', label=None)
	#plt.xlabel('y')
	#plt.ylabel('z')
	##~ plt.xlim(( mean(coords,axis=0)[1]-5.0, mean(coords,axis=0)[1]+5.0 ))
	##~ plt.ylim(( mean(coords,axis=0)[2]-5.0, mean(coords,axis=0)[2]+5.0 ))
	#ax.grid(True)

	#from mpl_toolkits.mplot3d import Axes3D
	#ax = fig.add_subplot(224, projection='3d')
	#ax.view_init(20,-45)
	#ax.scatter(cluster1[:,0],cluster1[:,1],cluster1[:,2],s=2,c=colors[0],edgecolors='none')
	#ax.scatter(cluster2[:,0],cluster2[:,1],cluster2[:,2],s=2,c=colors[9],edgecolors='none')
	##~ ax.scatter(means[:,0],   means[:,1],   means[:,2],   c='k', marker='*', s=100, edgecolors='k', label=None)
	#ax.set_xlabel('x vector')
	#ax.set_ylabel('y vector')
	#ax.set_zlabel('z vector')
	#ax.set_zlim3d(( mean(coords,axis=0)[2]-5.0, mean(coords,axis=0)[2]+5.0 ))
	#ax.set_ylim3d(( mean(coords,axis=0)[1]-5.0, mean(coords,axis=0)[1]+5.0 ))
	#ax.set_xlim3d(( mean(coords,axis=0)[0]-5.0, mean(coords,axis=0)[0]+5.0 ))

	#~ plt.show()
	plt.savefig('low_spherical/CartClust_PCA_:%d@%d.png' %(dictionary[atom],atom)) 
