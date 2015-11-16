#! /usr/bin/env python
import os
import string
from Bio import AlignIO
from Bio import SeqIO
import Bio.SubsMat.MatrixInfo as BM
from numpy import *
import pylab
from itertools import product
import multiprocessing
import subprocess

def NeedlemanWunsch(s1,s2,g,costFn,rs):
    # M and N are the lengths of s1 and s2 respectively
    M = len(s1)
    N = len(s2)

    # Create two (M+1)x(N+1) matricies. Adding an extra row to the M and N will allow for the case
    # where one of the strings is all insertions or deletions
    #   M is s1, with it's characters as rows
    #   N is s2, with it's characters as columns
    score     = zeros((M+1,N+1))
    traceback = zeros((M+1,N+1))

    # From the homework, it is possible to set the boundaries of the graph to multiples of the gap
    # function. This allows the algorithm to start at (1,1) and progress to (M+1,N+1). Also, setting
    # the traceback matrix to up for the right column and left for the upper row will ensure that the
    # algorithm finds it's way to [0,0] where done (4) is acheived.
    for m in range(M+1):
        score[m,0]     = m*g
        traceback[m,0] = 1
    for n in range(N+1):
        score[0,n]     = n*g
        traceback[0,n] = 2
    traceback[0,0] = 4

    cellScore = zeros(3)
    # Starting at (1,1) and progressing to (M+1,N+1), the algorithm computes the scores of it's three
    # neighbors, the cell diagonal (0), up (1), and to the left (2).
    for m in range(1,M+1):
        for n in range(1,N+1):
            try:
                cellScore[0] = score[m-1,n-1] + costFn[s1[m-1],s2[n-1]]
            except:
                cellScore[0] = score[m-1,n-1] + costFn[s2[n-1],s1[m-1]]
            cellScore[1] = score[m-1,n  ] + g
            cellScore[2] = score[m  ,n-1] + g
            
            # direction can be 0, 1, 2 depending on which score is largest. 
            # partialSum is used in scoring matrix as the cell's score.
            direction  = cellScore.argmax()
            partialSum = max(cellScore)
            
            traceback[m,n] = direction
            score[m,n]     = partialSum

    if rs == 1: return score[m,n]
    # Now that the algorithm has produced the traceback matrix, now it must walk back from it's
    # lower lefthand corner to the "done" in the top right corner. align1 and align2 are strings
    # containing the optimized sequence alignments. 
    m = M
    n = N
    align1 = ''
    align2 = ''
    while (traceback[m,n] != 4):
        # 0 is a match, go diagonal
        if traceback[m,n] == 0:
            align1 += s1[m-1]
            align2 += s2[n-1]
            m -= 1
            n -= 1
        # 1 is an insertion in s1, go upwards
        if traceback[m,n] == 1:
            align1 += s1[m-1]
            align2 += '_'
            m -= 1
        # 2 is an deletion in s1, go leftwards
        if traceback[m,n] == 2:
            align1 += '_'
            align2 += s2[n-1]
            n -= 1

    # Since the algorithm began at the ending letters and incrementing upwards, flipping the
    # strings will give the correct alignment and direction.
    align1 = align1[::-1]
    align2 = align2[::-1]
    
    #print align1
    #print align2
    return (align1, align2, score[M,N])

def SmithWaterman(s1,s2,g,costFn,rs):
    # M and N are the lengths of s1 and s2 respectively
    M = len(s1)
    N = len(s2)

    # Create two (M+1)x(N+1) matricies. Adding an extra row to the M and N will allow for the case
    # where one of the strings is all insertions or deletions
    #   M is s1, with it's characters as rows
    #   N is s2, with it's characters as columns
    score     = zeros((M+1,N+1))
    traceback = zeros((M+1,N+1))

    # From the homework, it is possible to set the boundaries of the graph to zero all around with
    # "done"'s in the traceback since extraneous characters are not counted
    for m in range(M+1):
        score[m,0]     = 0
        traceback[m,0] = 4
    for n in range(N+1):
        score[0,n]     = 0
        traceback[0,n] = 4

    cellScore = zeros(3)
    maxScore = -1
    # Starting at (1,1) and progressing to (M+1,N+1), the algorithm computes the scores of it's three
    # neighbors, the cell diagonal (0), up (1), and to the left (2).
    for m in range(1,M+1):
        for n in range(1,N+1):
            try:
                cellScore[0] = score[m-1,n-1] + costFn[s1[m-1],s2[n-1]]
            except:
                cellScore[0] = score[m-1,n-1] + costFn[s2[n-1],s1[m-1]]
            cellScore[1] = score[m-1,n  ] + g
            cellScore[2] = score[m  ,n-1] + g
            
            # direction can be 0, 1, 2 depending on which score is largest. 
            # partialSum is used in scoring matrix as the cell's score.
            direction  = cellScore.argmax()
            partialSum = max(cellScore)
            
            # Special to the Smith-Waterman Algorithm is the fact that if the score goes
            # beneath zero, it is reset to zero and a "done" is entered into the traceback
            if partialSum < 0:
                score[m,n]     = 0
                traceback[m,n] = 4
            else:
                traceback[m,n] = direction
                score[m,n]     = partialSum
                
            # The algorithm begins where the score is the largest, so maxScore and maxLoc
            # will store that information
            if partialSum > maxScore:
                maxScore = partialSum
                maxLoc   = m, n

    if rs == 1: return maxScore
    # Now that the algorithm has produced the traceback matrix, now it must walk back from it's
    # lower lefthand corner to the "done" in the top right corner. align1 and align2 are strings
    # containing the optimized sequence alignments. 
    m = maxLoc[0]
    n = maxLoc[1]
    align1 = ''
    align2 = ''
    while (traceback[m,n] != 4):
        # 0 is a match, go diagonal
        if traceback[m,n] == 0:
            align1 += s1[m-1]
            align2 += s2[n-1]
            m -= 1
            n -= 1
        # 1 is an insertion in s1, go upwards
        if traceback[m,n] == 1:
            align1 += s1[m-1]
            align2 += '_'
            m -= 1
        # 2 is an deletion in s1, go leftwards
        if traceback[m,n] == 2:
            align1 += '_'
            align2 += s2[n-1]
            n -= 1

    # Since the algorithm began at the ending letters and incrementing upwards, flipping the
    # strings will give the correct alignment and direction.
    align1 = align1[::-1]
    align2 = align2[::-1]
    #print align1
    #print align2
    #print maxScore
    return (align1, align2, maxScore)

#------------------------------------------------------------------------------


#Create list of 27 query sequences
f=open('query.fasta', 'r')
seqio=list(SeqIO.parse(f,'fasta'))
f.close()
s1list=[]
for i in range(len(seqio)):
	s1=seqio[i].seq.tostring().upper()
	s1list.append(s1)

#calculate hmmlikelihood from profile
import ghmm
m=ghmm.HMMOpen('protfam.hmm')
sigma=ghmm.AminoAcids
hmmscores=[]
alignments=[]
j=0
f = open('viterbiout','w')
j=1
for i in s1list:
	seq=ghmm.EmissionSequence(sigma,list(i))
	a=m.viterbi(seq)
#	print a[1]
#	p=m.loglikelihood(seq)
	f.write('seq'+ str(j)+': ')
	f.write(str(a[1])+'\n')
	j=j+1
f.close()
