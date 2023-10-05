#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt('output/data/therm.csv')
plt.plot(data)
plt.xlabel('#sweeps')
plt.ylabel('Energy density')
plt.savefig('output/plot/therm.png')