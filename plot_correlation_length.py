import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
LENGTH = 64
temp = 1.0
path = f"output/correlation_length/L{LENGTH}/lexic_metropolis/{temp}.csv"
data = np.loadtxt(path, delimiter=",", skiprows=1)

fig, ax = plt.subplots()
ax.errorbar(data[:,0],data[:,1],yerr=data[:,2], fmt='o', capsize=1, elinewidth=1, markersize=1)
xfit = fit(data[:,0],data[:,1],data[:,2])
f = lambda i, a, b: a*np.cosh((i-LENGTH/2)/b)
xfit.fiting(f, args={"bounds":((0,np.inf))})
x = np.linspace(0,LENGTH,100)
ax.plot(x, f(x,*xfit.opt),linewidth=0.8)
plt.show()