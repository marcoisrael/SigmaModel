#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import matplotlib.colors as colors
import os
from scipy.interpolate import interp1d

fig, ax = plt.subplots()
Tq = [3,6,12,20]
N = [3, 5, 10, 17]
alg = "multi_cluster"
x = np.linspace(0,4,200)
symbol = ["p", "*", "x", "P" ]
symbol = dict(zip(N,symbol))


color = ["blue", "orange", "green", "yellow" ]
color = dict(zip(N,color))
f = lambda x, a, b: a*x**(-b)+0.051
for tq, n in zip(Tq,N):
	data = np.loadtxt(f"output/cooling/jkL64/4-0/{alg} {tq}.csv", skiprows=1, delimiter=",")
	ax.errorbar(data[:,1], data[:,2], data[:,3], fmt=symbol[n], color=color[n], markersize=4, label=f"$\\tau_{{cool}} = {tq}$")
	#xfit = fit(data[:,1], data[:,2], data[:,3])
	#xfit.fiting(f)
	spl = interp1d(data[:,1], data[:,2], kind="quadratic")  # type: BSpline

	ax.plot(x, spl(x), color=color[n], linewidth=0.7)

data = np.loadtxt(f"output/therm/L64/lexic_metropolis/4-0-30.csv", skiprows=1, delimiter=",")
ax.errorbar(data[:,1], data[:,2], data[:,3], color="black",  fmt=".")
#xfit = fit(data[:,1], data[:,2], data[:,3])
#xfit.fiting(f)
#ax.plot(x, f(x, *xfit.opt), color="blue", linewidth=0.7)
spl = interp1d(data[:,1], data[:,2], kind="quadratic")  # type: BSpline
ax.plot(x, spl(x), color="black", linewidth=0.7)
ax.set_xlabel(r"$T$",fontsize=14)
ax.set_ylabel(r"$\chi_t$",fontsize=14, rotation="horizontal", ha="right")
ax.invert_xaxis()
ax.legend()
ax.grid(True)
fig.savefig("output/plot/cooling.png")