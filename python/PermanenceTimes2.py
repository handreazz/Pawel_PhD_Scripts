#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

####
#Get and plot average permanence times with a sliding window
###

smooth=3  #define the sliding window length (how many times a state must not recur for the streak to end)



f=genfromtxt('waterdistribution') #name of file produced by watersPerCell.py, matrix of states at frame and cell
cells=f.shape[1] #no cells
frames=f.shape[0] #no frames
streaks={} #dictionary which will store a list of streak lengths for each state
events=0 #variable to store the number of changes between states

for cell in range(cells):
	#cell=cell+32  #for debugging you can select just one cell
	Prev1Frame=-1
	streak=1 #current streak length
	fault=0 #current number of faults (if fault reaches smooth, you have a streak end)
	for frame in range(frames):
		CurrFrame=f[frame,cell]
		#print frame, Prev1Frame, CurrFrame, streak
		if Prev1Frame<0:   #necessary for the first frame where no previous state to compare to
			Prev1Frame=CurrFrame
		elif Prev1Frame==CurrFrame:  #if the same, rename Prev1Frame and reset faults to 0
			streak+=1
			Prev1Frame=CurrFrame
			fault=0
		else:  				#if not the same increase fault by one and don't rename Prev1Frame
			fault+=1
			streak+=1
		if fault==smooth:  		#if no of faults equals smooth (window)
			streak=streak-smooth	#the streak is minus what you added checking the window
			events+=1		#record an event
			if Prev1Frame in streaks:  #add to streaks dictionary
				streaks[Prev1Frame].append(streak)
			else:
				streaks[Prev1Frame]=[streak]
			
			fault=0    		#reset fault and streak
			streak=1
			Prev1Frame=f[frame-smooth+1,cell]   #now we need to check what happended within the window
			#print Prev1Frame
			for i in range(smooth-1):   	#the window is smooth-1 long
				CurrFrame=f[frame-smooth+1+i+1,cell]   #get value at the beginning of the window
				if Prev1Frame==CurrFrame:      #compare to the next values in the window to end up with a streak and fault value for that window. The fault will never equal smooth because the window is smooth-1 long.
					streak+=1
					Prev1Frame=CurrFrame
					fault=0
				else:
					fault+=1
					streak+=1
			
	if Prev1Frame in streaks:  #take care of streak when you reach last frame
		streaks[Prev1Frame].append(streak)
	else:
		streaks[Prev1Frame]=[streak]		

#record average streak length for each state in this file
p=open('PermanenceTimes_smooth'+str(smooth),'w')
#print streaks	
for x in streaks:
	print average(streaks[x])
	p.write('%2i %5.2f \n' %(x, average(streaks[x])) )
p.close()


#make bar graph		
f=genfromtxt('PermanenceTimes_smooth'+str(smooth))
x=f[:,0]
y=f[:,1]

fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.bar(x[0:],y[0:],align='center')

fig.suptitle('Water State Residence Times', fontsize=28, y=.93)
ax.set_xlabel('State (waters in unit cell)',fontsize=24, labelpad=10)
ax.set_ylabel('Average Residence Time (ns)', fontsize=24, labelpad=10)
#center tickmarks
z=array(x) 
plt.xticks(z+1/2)
ax.set_xlim((-1,10))
#tick location
ax.set_yticks([200,400,600,800,1000,1200])
#tick label
ax.set_yticklabels([4,8,12,16,20,24])
#tick label font size
for label in ax.get_xticklabels() + ax.get_yticklabels():
	label.set_fontsize(24)
#tick marks size
for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markeredgewidth(3)
    line.set_markersize(10)

#plt.show()
plt.savefig('PermanenceTimes_smooth'+str(smooth)+'.png')
#~ plt.savefig('test3.png')
#add the number of events to the average streak length file
p=open('PermanenceTimes_smooth'+str(smooth),'a')
p.write('\n the number of events was %d \n' %events)	
p.close()
