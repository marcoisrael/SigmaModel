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
x = np.linspace(0,1,100)
f = lambda x, a, b, c:c+a*x**b
fig, ax = plt.subplots(dpi=120)
for tmax in np.arange(6,10):
	data = np.loadtxt(f"{path}/{alg} {tmax}.csv", delimiter=",", skiprows=1)[:-1]
	tq, temp, q, qErr = data[:,0], data[:,1], data[:,2], data[:,3]
	ax.errorbar(tq/tq.max(), q, qErr, fmt='o', capsize=1, elinewidth=1, markersize=2, color=colors_list[2*tmax+5])
	xfit = fit(tq/tq.max(), q, qErr)
	#f = lambda x, b, c: q.max()+b*x+c*x**2
	xfit.fiting(f)
	ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color=colors_list[2*tmax+5])
data = np.loadtxt(f"output/therm/data0/4-0.5/{alg} 30.csv", delimiter=",", skiprows=1)[:-2]
tq, temp, q, qErr = data[:,0], data[:,1], data[:,2], data[:,3]
ax.errorbar(tq/tq.max(), q, qErr, fmt='o', capsize=1, elinewidth=1, markersize=2, color=colors_list[0])
xfit = fit(tq/tq.max(), q, qErr)

xfit.fiting(f)
ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color=colors_list[0])
ax.grid(True)
ax.set_ylabel(r"$\chi_{tf}$", fontsize=14)
ax.set_xlabel(r"$sweep/\tau_Q$", fontsize=14)
plt.show()
