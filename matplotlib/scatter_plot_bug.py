#!/usr/bin/env python

from matplotlib import pyplot as plt

x = [1,2,3,4,5,6]
y = [1e-2, 2e-3, 6e-3, 7e-3, 4e-3, 3e-3]

plt.plot(x,y,color='red')
plt.scatter(x,y,color='orange')
print x
print y
plt.yscale('log')
plt.show()

x = [1,2,3,4,5,6]
y = [1e-2, 2e-3, 0, -3, 4e-3, 3e-3]

plt.plot(x,y,color='red')
plt.scatter(x,y,color='orange')
print x
print y
plt.yscale('log')
plt.show()
