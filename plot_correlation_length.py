#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import os
color = {32:"blue",64:"red",128:"black"}
h = 0
make_plots=False
if not os.path.isdir("output/plot/correlation_length/"):
	os.makedirs("output/plot/correlation_length/")
psi = []
psiErr = []
LENGTH=128
name="charge"
T = np.array([0.9,1.0,1.2,1.4,1.6,1.8,2.0])
for temp in T:
	path = f"output/correlation_length/L{LENGTH}/lexic_metropolis/{temp}.csv"
	#print(path)
	data = np.loadtxt(path, delimiter=",", skiprows=1)
	f = lambda x, a, b: a*np.exp(-x/b)+a*np.exp((x-LENGTH)/b)
	#xfit = fit(data[:int(LENGTH/4),0],data[:int(LENGTH/4),1],data[:int(LENGTH/4),2])
	xfit = fit(data[:,0],data[:,1],data[:,2])

	xfit.fiting(f, args={"bounds":((0,np.inf))})
	psi.append(xfit.opt[1])
	psiErr.append(xfit.error[1])
	if make_plots:
		fig, ax = plt.subplots()
		x = np.linspace(0,LENGTH,100)
		ax.errorbar(data[:,0],data[:,1],yerr=data[:,2], fmt='o', capsize=1, elinewidth=1, markersize=1)
		ax.plot(x, f(x,*xfit.opt),linewidth=0.8)
		fig.savefig(f"output/plot/correlation_length/lexic_metropolis_L{LENGTH}_{temp}.png")
		print(temp, xfit.opt[1])
		#plt.show()
		plt.close()
psi = np.array(psi)
fig, ax = plt.subplots()

ax.errorbar(T, psi, psiErr, fmt='o', capsize=1, elinewidth=1, markersize=1, color="black", label=f"L={LENGTH}")
f = lambda x, a, b,c: a*(x+c)**(-b)
xfit = fit(T, psi, psiErr)
xfit.fiting(f)
print(xfit.opt)
print(xfit.error)
ax.text(0.5 ,0.9-h, r"$\nu=$"+fix(xfit.opt[1],xfit.error[1])+"\n"+r"$\chi^2/dof=$"+f"{xfit.chisq_by_dof}", 
		horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=8)
h = h+0.12
x = np.linspace(T[0],T[-1],200)
ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color="black")
ax.set_xlabel(r"$T$", fontsize=14)
ax.set_ylabel(r"$\xi$", rotation="horizontal", fontsize=14, ha="right")
#ax.legend()
ax.grid(True)

data = np.array([T,psi,psiErr]).transpose()
np.savetxt("output/send/correlation_length_LM_L128.csv", data, 
	delimiter=",",header="T,xi,xi_error",comments="", fmt="%16f")
#ax.set_title(f"Correlation length, lexicographical Metropolis, L={LENGTH}", fontsize=12)
fig.savefig(f"output/plot/{name}/correlation_length_lexic_metropolis_L{LENGTH}.png",bbox_inches="tight")
print(f"output/plot/{name}/correlation_length_lexic_metropolis_L{LENGTH}.png")