#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt('output/file/therm.csv')
plt.plot(data)
plt.savefig('output/plot/therm.png')