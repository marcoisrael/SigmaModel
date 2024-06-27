#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())
import os
make_temp_plots=False
make_plt_sacaling_law=True
name = "charge"
alg = "multi_cluster"
L = 128
#T = np.array([0.5,0.75,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.0])
T = np.array([0.75,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.0])
tc = 0.74

N = np.ones_like(T)
#T = np.array([0.5,0.6,0.8,0.9,1.0])

N[0], N[1] = 4, 3

Algs = {
		"lexic_metropolis":"Lexicographical Metropolis",
		"random_metropolis":"Random Metropolis",
		"random_glauber":"Random Glauber",
		"lexic_glauber":"Lexicographical Glauber",
		"multi_cluster":"Multi Cluster",
		}

f = lambda x, b, A: A*np.exp(-x/b)
obs = {"charge":{"label":r"$\frac{C_{Q,Q}(t)}{C_{Q,Q}(0)}$","index":1,"sym":"Q"},
		"magnetization":{"label":r"$\frac{C_{M,M}(t)}{C_{M,M}(0)}$","index":2,"sym":"M"},
		"energy":{"label":r"$\frac{C_{M,M}(t)}{C_{M,M}(0)}$","index":0,"sym":"E"}}

cor = []
corErr = []
cor2 = []
cor2Err = []
for temp, n in zip(T,N):	
	path = f"output/record-1/L{L}/{alg}/{temp}.csv"
	data = np.loadtxt(path, delimiter=",", skiprows=1)
	X = []
	nmax = 3
	var = 0
	for t in np.arange(0,2000):
		x = correlation(data[:,obs[name]["index"]],t)
		X.append(x)
		if x[1]>0 and var==0:
			nmax+=1
		else:
			var=1
	X = np.array(X)

	t, q, qErr = X[:,0],X[:,1]/X[0,1],X[:,2]/X[0,1]

	xfit = fit(t[:nmax],q[:nmax],qErr[:nmax])
	xfit.fiting(f, args={"bounds":((0,np.inf))})
	nmin = 0
	while xfit.chisq_by_dof>10:
		nmin+=1
		xfit = fit(t[nmin:nmax],q[nmin:nmax],qErr[nmin:nmax])
		xfit.fiting(f)

	texp = 0
	texpErr = 0

	for i in range(nmin,int(np.ceil(4*xfit.opt[0]))):
		texp = texp+q[i]/q[nmin]
		texpErr = texpErr+qErr[i]

	xlabel = f"$t_{n}$"

	x = np.linspace(t[nmin],t[nmax],500)

	cor2.append(n*texp)
	cor2Err.append(n*texpErr)
	cor.append(n*xfit.opt[0])
	corErr.append(n*xfit.error[0])
	
	print(n, temp, n*xfit.opt[0], n*texp)
	
	if make_temp_plots:
		fig, ax = plt.subplots(dpi=120,tight_layout=True)
		ax.plot(x, f(x, *xfit.opt), linewidth=0.7, color="black", label="Fitting")
		ax.errorbar(t[:nmax], q[:nmax], qErr[:nmax], fmt='o', capsize=1, elinewidth=1, markersize=1, color="blue", label="Data")
		head=r"$\tau_{exp}=$"+fix(n*xfit.opt[0],n*xfit.error[0])+"\n"+r"$\tau_{int}=$"+fix(n*texp,n*texpErr)
		ax.text(0.5 ,0.9, head, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
		ax.set_xlabel(xlabel, fontsize=30)
		ax.set_ylabel(obs[name]["label"], rotation="horizontal", fontsize=18, ha="right")
		ax.grid(True)
		ax.legend()
		ax.set_title(f"{alg}, temp = {temp}", fontsize=15)
		#print(temp, xfit.opt[-1])
		if not os.path.isdir(f"output/plot/{name}/L{L}/{alg}"):
			os.makedirs(f"output/plot/{name}/L{L}/{alg}")
		fig.tight_layout()
		fig.savefig(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
		#print(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
		plt.close()
		del ax, fig

if not make_plt_sacaling_law:
	exit()

fig, ax = plt.subplots()
x = np.linspace(T[0],T[-1],200)
cor2 = np.array(cor2)
cor = np.array(cor)
corErr = np.array(corErr)
cor2Err = np.array(cor2Err)
f = lambda x, a, b:a*x**(-b)

xfit = fit(T,cor,corErr)
#xfit.fiting(f)
#print(xfit.opt)
ax.errorbar(T,cor,corErr, fmt='o', capsize=3, elinewidth=1, markersize=2, label=r"$\tau_{exp}$", color="black")
#ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color="black")
#ax.text(0.5 ,0.9, r"$z=$"+fix(xfit.opt[1],xfit.error[1]), 
#		horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=16)


#ax.errorbar(T, cor2, cor2Err, fmt='o', capsize=3, elinewidth=1, markersize=2, label=r"$\tau_{int}$", color="r")
ax.set_xlabel(r"$T$",fontsize=14)
ax.set_ylabel(r"$\tau$",fontsize=14)
#ax.legend() 
ax.grid(True)
#fig.tight_layout()
data = np.array([T, cor, corErr]).transpose()
np.savetxt(f"output/send/autocorrelation_{name}_{alg}.csv", data, 
	delimiter=",",header="T,tau,tau_error",comments="", fmt="%16f")
title =Algs[alg]
#ax.set_title(f"Autocorrelation time, {title}, L={L}", fontsize=12)
i = obs[name]["sym"]
if not os.path.isdir(f"output/plot/{name}/L{L}/{alg}"):
	os.makedirs(f"output/plot/{name}/L{L}/{alg}")
fig.savefig(f"output/plot/{name}/autocorrelation_{alg}_L{L}_{i}.png")
print(f"output/plot/{name}/autocorrelation_{alg}_L{L}_{i}.png")