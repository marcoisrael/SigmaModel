#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())
import os

Algs = ["lexic_metropolis", "random_metropolis", "lexic_glauber", "random_glauber", "multi_cluster"]
Algs = ["lexic_metropolis"]
T = np.array([0.6,0.8,1.0,2.0,3.0,4.0])
T = np.array([0.9])
x = np.linspace(0.6,4.0,200)
f = lambda x, b: np.exp(-x/b)

fig, ax = plt.subplots(dpi=120,tight_layout=True)
for alg in Algs:
	for temp in T:
		fig, ax = plt.subplots(dpi=120)
		path = f"output/correlation/{alg}/{temp}_Q.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		t, q, qErr = data[:,0],data[:,1]/data[0,1],data[:,2]/data[0,1]
		x = np.linspace(t[0],t[-1],500)
		xfit = fit(t,q,qErr)
		xfit.fiting(f, args={"bounds":((0,np.inf))})
		#print(xfit.opt[-1])
		
		ax.plot(x, f(x, *xfit.opt), linewidth=0.8, color="black", label="Fitting")
		ax.errorbar(t,q,qErr, fmt='o', capsize=1, elinewidth=1, markersize=1, color="blue", label="Data")
		ax.text(0.5 ,0.9, r"$\tau_{exp}=$"+fix(xfit.opt[-1],xfit.error[-1])+"\n"+r"$\chi^2/dof=$"+f"{xfit.chisq_by_dof}", 
			horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
		ax.set_xlabel(r"$t_{50}$", fontsize=14)
		ax.set_ylabel(r"$\frac{C_{Q,Q}(t)}{C_{Q,Q}(0)}$", rotation="horizontal", fontsize=18, ha="right")
		ax.grid(True)
		ax.legend()
		ax.set_title(f"{alg}, temp = {temp}", fontsize=15)
		#print(temp, xfit.opt[-1])
		if not os.path.isdir(f"output/plot/correlation/{alg}"):
			os.makedirs(f"output/plot/correlation/{alg}")
		fig.tight_layout()
		fig.savefig(f"output/plot/correlation/{alg}/{alg}_{temp}.png")
		print(f"output/plot/correlation/{alg}/{alg}_{temp}.png")
		plt.close()
exit()
f = lambda x, a, z, c: c+a*x**z
fig, (ax1,ax2) = plt.subplots(1,2,dpi=120,figsize=(16,7))

cn = 0
for alg in Algs:
	#print(alg)

	cor = []
	corErr = []
	for temp in T:
		path = f"output/correlation/{alg}/{temp}_Q.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)

		t, q, qErr = data[:,0],data[:,1],data[:,2]
		
		time = q.sum()/q[0]
		
		cor.append(time)
		print(time)
		exit()
		corErr.append(0.5*timeErr)
	ax1.errorbar(T,cor,corErr, fmt='o', capsize=3, elinewidth=1, markersize=2, label=alg, color=colors_list[cn])
	ax2.errorbar(1/T,cor,corErr, fmt='o', capsize=3, elinewidth=1, markersize=2, label=alg, color=colors_list[cn])

	#xfit = fit(T,cor,corErr)
	#xfit.fiting(f)
	#ax1.plot(x, f(x,*xfit.opt), linewidth=0.8, color=colors[alg])
	#ax2.plot(1/x, f(x,*xfit.opt), linewidth=0.8, color=colors[alg])
	cn += 1 

for ax in (ax1, ax2):
	ax.legend()
	ax.grid(True)
	ax.set_ylabel(r"$\tau$", fontsize=14)

ax1.set_xlabel(r"$T$", fontsize=14)
ax2.set_xlabel(r"$1/T$", fontsize=14)
fig.suptitle("Autocorrelation time", fontsize=16)
#fig.savefig(f"output/plot/autocorrelation_time/autocorrelation_time.png")