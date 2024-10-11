#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import matplotlib.colors as colors
import os, argparse
parser = argparse.ArgumentParser(prog="autocorrelation")
parser.add_argument('-alg','--algorithm')
args = parser.parse_args()
colors_list = list(colors._colors_full_map.values())
import os
make_temp_plots=True
name = "charge"
alg = args.algorithm
L = 64
T = os.listdir(f"output/record-3/L64/{alg}")
def convert(x):
	return float(x.replace(".csv",""))
T = np.sort(np.array(list(map(convert, T))))
f = lambda x, b, A: A*np.exp(-x/b)
cor = []
corErr = []
cor2 = []
cor2Err = []
for temp in T:	
	path = f"output/record-3/L{L}/{alg}/{temp}.csv"
	data = np.loadtxt(path, delimiter=",", skiprows=1)
	X = []
	nmax = 3
	var = 0
	for t in np.arange(0,1000):
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
	x = np.linspace(t[nmin],t[nmax],500)
	cor2.append(texp)
	cor2Err.append(texpErr)
	cor.append(xfit.opt[0])
	corErr.append(xfit.error[0])	
	print(temp, xfit.opt[0], texp)	
	if make_temp_plots:
		fig, ax = plt.subplots(dpi=120,tight_layout=True)
		ax.plot(x, f(x, *xfit.opt), linewidth=0.7, color="black", label="Fitting")
		ax.errorbar(t[:nmax], q[:nmax], qErr[:nmax], fmt='o', capsize=1, elinewidth=1, markersize=1, color="red", label="Data")
		#head=r"$\tau_{exp}=$"+fix(n*xfit.opt[0],n*xfit.error[0])+"\n"+r"$\tau_{int}=$"+fix(n*texp,n*texpErr)
		#ax.text(0.5 ,0.9, head, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
		ax.set_xlabel(r"$t$", fontsize=18)
		ax.set_ylabel(obs[name]["label"], fontsize=18)
		#ax.grid(True)
		ax.legend()
		#ax.set_title(f"{alg}, temp = {temp}", fontsize=15)
		#print(temp, xfit.opt[-1])
		os.makedirs(f"output/plot/{name}/L{L}/{alg}", exist_ok=True)
		fig.tight_layout()
		fig.savefig(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.pdf",format="pdf",bbox_inches="tight")
		#print(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
		plt.close()
		del ax, fig
cor2 = np.array(cor2)
cor = np.array(cor)
corErr = np.array(corErr)
cor2Err = np.array(cor2Err)
data = np.array([T, cor, corErr, cor2, cor2Err]).transpose()
os.makedirs("output/autocorrelation",exist_ok=True)
np.savetxt(f"output/autocorrelation/{name}_{alg}.csv", data, 
	delimiter=",",header="T,tauExp,tauExp_error,tauInt,tauInt_error",comments="", fmt="%16f")