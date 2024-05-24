#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
color = {32:"blue",64:"red",128:"black"}
fig, ax = plt.subplots()
h = 0
for LENGTH in [32, 64,128]:
	psi = []
	psiErr = []
	T = np.array([0.6,0.7,0.8,0.9,1.0])
	for temp in T:
		path = f"output/correlation_length/L{LENGTH}/lexic_metropolis/{temp}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		#ax.errorbar(data[:,0],data[:,1],yerr=data[:,2], fmt='o', capsize=1, elinewidth=1, markersize=1)
		xfit = fit(data[:int(LENGTH/4),0]/LENGTH,data[:int(LENGTH/4),1],data[:int(LENGTH/4),2])
		f = lambda x, a, b: a*np.exp(-x/b)#a*np.cosh((i-1/2)/b)
		xfit.fiting(f, args={"bounds":((0,np.inf))})
		psi.append(xfit.opt[-1])
		psiErr.append(xfit.error[-1])
		x = np.linspace(0,LENGTH,100)
		#ax.plot(x, f(x,*xfit.opt),linewidth=0.8)
		#fig.savefig("output/test.png")
		#plt.show()
	psi = np.array(psi)
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
	ax.set_ylabel(r"$\frac{\xi}{L}$", rotation="horizontal", fontsize=18, ha="right")
ax.legend()
ax.grid(True)
fig.savefig("output/correlation_length.png")