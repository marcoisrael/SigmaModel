#!/bin/bash/python3
import matplotlib.pyplot as plt 
import numpy as np


fig, ax = plt.subplots() 
x = np.linspace(0.5,1)
y = 0.5*x+x**2
ax.plot(x, y, color="blue")
x = np.linspace(1, 1.4)
y = 0.5+np.exp(x)
ax.plot(x, y, color="blue")

plt.show()


