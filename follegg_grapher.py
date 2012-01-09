""""
********   ** FOLLEGG GRAPHING MODULE **   *********

Enables plotting and printing of results given calculated 
using the following modules

1.) Extended Learning Curve model -> lcurvemodel.py
2.) Cost model --> costmodel.py

""""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import costmodel as cmodel

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

fig = plt.figure()
ax = fig.add_subplot(111)

# the histogram of the data
n, bins, patches = ax.hist(x, 500, normed=1, facecolor='blue', alpha=0.75)


def plotMaintenenceCosts():

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Hours')
    ax.set_ylabel('Cost')
    #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    ax.set_xlim(40, 160)
    ax.set_ylim(0, 0.03)
    ax.grid(True)

#def plotEnergyCosts():

def plotStartCosts():
    return
# hist uses np.histogram under the hood to create 'n' and 'bins'.
# np.histogram returns the bin edges, so there will be 50 probability
# density values in n, 51 bin edges in bins and 50 patches.  To get
# everything lined up, we'll compute the bin centers
bincenters = 0.5*(bins[1:]+bins[:-1])
# add a 'best fit' line for the normal PDF
y = mlab.normpdf( bincenters, mu, sigma)

# T
l = ax.plot(bincenters, y, 'r--', linewidth=5)  

ax.set_xlabel('Smarts')
ax.set_ylabel('Probability')
#ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
ax.set_xlim(40, 160)
ax.set_ylim(0, 0.03)
ax.grid(True)

plt.show()
