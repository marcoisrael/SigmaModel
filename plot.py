#!/usr/bin/python3
import numpy as np
from plotClass import *
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())

startTemp = 4
endTemp = 0
path = f"output/cooling/jkL64/{startTemp}-{endTemp}"
dest = f"output/plot/jkL64/{startTemp}-{endTemp}"
alg = "lexic_metropolis"
qmax = []
qmaxErr = []
fig, ax = plt.subplots(dpi=120)
for tmax in np.arange(6,10):
	x = np.linspace(0,tmax)
	data = np.loadtxt(f"{path}/{alg} {tmax}.csv", delimiter=",", skiprows=1)
	tq, temp, q, qErr = data[:,0], data[:,1], data[:,2], data[:,3]
	ax.errorbar(tq, q, qErr, fmt='o', capsize=1, elinewidth=1, markersize=2, color=colors_list[2*tmax+5])
	xfit = fit(tq, q, qErr)
	f = lambda x, a, z: a*x**z+q[0]
	xfit.fiting(f)
	ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color=colors_list[tmax+5])
ax.grid(True)
ax.set_ylabel(r"$\chi_{tf}$", fontsize=14)
ax.set_xlabel("#Sweep", fontsize=14)

plt.show()
