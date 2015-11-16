#! /usr/bin/env python
from numpy import *
import sys, math




###Initial conditions##########################
#How many clusters:
k = int(raw_input("How many clusters do you want? "))
#How many iterations:
itera=int(raw_input("How many iterations? "))


#Read data:
data = genfromtxt("data.txt")

for i in range(5):
    #create initial centroids randomly
    mini=min(data.min(axis=0))
    maxi=max(data.max(axis=0))
    l=data.shape[1]
    centroids=((maxi-mini)*random.random((k,l)))+mini





    ###FUNCTIONS######################################
    #distance function to measure distance of a point a to a centroid b 
    def distancef(a,b):
        ret = 0.0
        for i in range(l):
            ret = ret+pow((a[i]-b[i]), 2)
            dist= math.sqrt(ret)
        return dist

    #one time iteration of measure distance, select min and assign to clusters
    #clusters is a list which for each vector in order gives the cluster it belongs to
    def clusterf(centroids,data):
        clusters=[]
        for i in data:
      #      print i
            dss=[]
            for j in centroids:
                dss.append(distancef(i,j))
      #      print dss
            clusters.append(argmin(dss))
      #  print clusters
        return clusters

    #bluster is a list of lists, each list containing the vectors which belong to that cluster
    def blusterf(k,clusters):
        bluster=[]
        for i in range(k):
            a=[]
            for j in range(len(clusters)):
                if clusters[j]==i:
                    a.append(j)
            bluster.append(a)
        return bluster

    #calculate new centroids:
    def centroidsf(k,l,bluster,centroids):
        for i in range(k):
            for j in range(l):
                a=0
                for ii in bluster[i]:
                    a=a+data[ii][j]
                if len(bluster[i])==0:
                    b=0
                else:
                    b=a/len(bluster[i])
                centroids[i,j]=b
        return centroids




    ####RUN ALGORITHM##########################
    for i in range(itera):
        clusters=clusterf(centroids,data)
        bluster=blusterf(k,clusters)
        centroids=centroidsf(k,l,bluster,centroids)



    print bluster

