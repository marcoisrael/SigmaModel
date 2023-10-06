#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt('output/data/therm.csv', delimiter=',')
y, yerr = data.transpose()
sweeps = np.arange(1,y.size+1)
plt.errorbar(sweeps, y, yerr=yerr, marker='.', ls='')
plt.plot(sweeps, np.zeros_like(y)+np.mean(y))
plt.xlabel('#sweeps')
plt.ylabel('Energy density')
plt.savefig('output/plot/therm.png')
