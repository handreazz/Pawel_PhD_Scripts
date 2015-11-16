#! /usr/bin/env python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, os

data = pd.read_csv('data.csv', index_col=0)
data = data.drop(data.columns[7], axis=1)
# data.where(data != '--', -1)
data [data == '--'] = -1
data = data[data.columns].astype(float)
#~ data = data.transpose()

plt.rc('axes',linewidth=2)
fig=plt.figure(figsize=(8, 18))
ax = fig.add_subplot(111)
# ax.set_frame_on(False)

heatmap = ax.pcolor(data, cmap=plt.cm.Blues, alpha=1)

ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
ax.set_ylim([0, 129])
ax.invert_yaxis()
ax.xaxis.tick_top()

from matplotlib.font_manager import FontProperties
xticks=[i for i in data.columns]
xticks[4]='ff14SB\nsolv'
ticks_font = FontProperties(family='monospace', size=10)
ax.set_xticklabels(xticks, minor=False, fontsize=18)
ax.set_yticklabels(data.index, minor=False, fontproperties=ticks_font)

plt.xticks(rotation=45)
# ax.grid(False)
for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

fig.tight_layout()
plt.savefig('heatmap.pdf')
plt.savefig('heatmap.png')
# import code ; code.interact(local=dict(globals(), **locals()))
