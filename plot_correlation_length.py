#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import os
color = {32:"blue",64:"red",128:"black"}
h = 0
if not os.path.isdir("output/plot/correlation_length/"):
	os.makedirs("output/plot/correlation_length/")
for LENGTH in [64]:
	psi = []
	psiErr = []
	T = np.array([0.85,0.9,0.95,1.0,2.0,3.0,4.0])
	for temp in T:
		fig, ax = plt.subplots()
		path = f"output/correlation_length/L{LENGTH}/lexic_metropolis/{temp}.csv"
		print(path)
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		ax.errorbar(data[:,0],data[:,1],yerr=data[:,2], fmt='o', capsize=1, elinewidth=1, markersize=1)
		f = lambda x, a, b: a*np.cosh((x-0.5*LENGTH)/b)
		xfit = fit(data[:,0],data[:,1],data[:,2])
		xfit.fiting(f, args={"bounds":((0,np.inf))})
		psi.append(xfit.opt[-1])
		psiErr.append(xfit.error[-1])
		x = np.linspace(0,LENGTH,100)
		ax.plot(x, f(x,*xfit.opt),linewidth=0.8)
		ax.set_yscale("log")
		fig.savefig(f"output/plot/correlation_length/lexic_metropolis_L{LENGTH}_{temp}.png")
		#print(xfit.error[-1])
		#plt.show()
		del ax, fig
	exit()
	psi = np.array(psi)
	fig, ax = plt.subplots()

	ax.errorbar(T, psi, psiErr, fmt='o', capsize=1, elinewidth=1, markersize=1, color=color[LENGTH], label=f"L={LENGTH}")
	f = lambda x, a, b, c: a*np.exp(-x/b)+c
	xfit = fit(T, psi, psiErr)
	xfit.fiting(f)
	ax.text(0.5 ,0.9-h, r"$\alpha=$"+fix(xfit.opt[1],xfit.error[1])+"\n"+r"$\chi^2/dof=$"+f"{xfit.chisq_by_dof}", 
			horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=8)
	h = h+0.12
	x = np.linspace(0.6,1.0,100)
	ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color=color[LENGTH])
	ax.set_xlabel(r"$T$", fontsize=12)
	ax.set_ylabel(r"$\xi$", rotation="horizontal", fontsize=18, ha="right")
ax.legend()
ax.grid(True)
fig.savefig("output/correlation_length.png")