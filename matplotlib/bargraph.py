#! /usr/bin/python
import sys
import os
from numpy import *
import Scientific.IO.NetCDF
from Numeric import * 
from Scientific.IO import NetCDF as Net
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

d = {1: 155, 2: 29439, 3: 133609, 4: 146832, 5: 101235, 6: 37629, 7: 5241, 8: 178, 9: 2}
x=d.keys()
y=d.values()


fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.bar(x,y,align='center')

fig.suptitle('Histogram of \'waters per unitcell\'', fontsize=16)
ax.set_xlabel('number of waters')
ax.set_ylabel('count (# of times a unit cell had that many waters in its volume')

#two ways to center tick marks
# I
#~ z=array(x) 
#~ plt.xticks(z+1/2)

# II
plt.xticks(arange(1,10,1))

#~ plt.show()
plt.savefig("watersPerCell.png")
