#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import matplotlib.colors as colors
import os, argparse
parser = argparse.ArgumentParser(prog="autocorrelation")
parser.add_argument('-alg','--algorithm',default="lexic_metropolis")
parser.add_argument('-o','--observable',default="energy")
args = parser.parse_args()
colors_list = list(colors._colors_full_map.values())
make_temp_plots=False
name = args.observable
alg = args.algorithm
L = 64
"""
T = os.listdir(f"output/record-3/L64/{alg}")
def convert(x):
	return float(x.replace(".csv",""))
T = np.sort(np.array(list(map(convert, T))))
"""
T = np.array([0.9,1.0,1.2,1.4,1.6,1.8])

if args.algorithm=="all":
	algs = ["lexic_metropolis","random_metropolis","lexic_glauber","random_glauber"]
else:
	algs = args.algorithm.split(",")
for alg in algs:	
	cor = []
	corErr = []
	Ti = []
	for temp in T:	
		path = f"output/record-3/L{L}/{alg}/{temp}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		X = []
		for t in np.arange(0,501):
			x = correlation(data[:,obs[name]["index"]],t)
			X.append(x)
		
		X = np.array(X)
		t, q, qErr = X[:,0],X[:,1]/X[0,1],X[:,2]/X[0,1]

		if temp in (0.9,1.0,1.2,1.4,1.6,1.8,2.0):
			xfit = fit(t[0:50],q[0:50],qErr[0:50])
			f = lambda x,a,b:a*np.exp(-x/b)
			xfit.fiting(f, args={"bounds":((0,np.inf))})
			i = 1
		if temp in (0.7,0.8):
			xfit = fit(t[0:200:4],q[0:200:4],qErr[0:200:4])
			f = lambda x,a1,a2,b1,b2: a1*np.exp(-x/b1)+a2*np.exp(-x/b2)
			xfit.fiting(f, args={"bounds":((0,np.inf))})
			i, = np.where(xfit.opt==xfit.opt[2:].max())[0]
		if temp in (0.5,0.6):
			xfit = fit(t[0:500:10],q[0:500:10],qErr[0:500:10])
			f = lambda x,a1,a2,a3,b1,b2,b3: a1*np.exp(-x/b1)+a2*np.exp(-x/b2)+a3*np.exp(-x/b3)
			xfit.fiting(f, args={"bounds":((0,np.inf))})
			i, = np.where(xfit.opt==xfit.opt[3:].max())[0]

		
		#print(temp,fix(xfit.opt[i],xfit.error[i]))
		cor.append(xfit.opt[i])
		corErr.append(xfit.error[i])
		Ti.append(temp)
		x = np.linspace(t[0],t[-1],500)
		if make_temp_plots:
			fig, ax = plt.subplots(tight_layout=True)
			ax.plot(x, f(x, *xfit.opt), linewidth=1.2, color="black", label="Fitting")
			ax.errorbar(t, q, qErr, fmt='o', capsize=1, elinewidth=1, markersize=2, color="red", label="Data")
			ax.set_xlabel(r"$t$", fontsize=18)
			ax.set_ylabel(obs[name]["label"], fontsize=18)
			ax.legend()
			#ax.set_title(f"{alg}, temp = {temp}", fontsize=15)
			#print(temp, xfit.opt[-1])
			os.makedirs(f"output/plot/{name}/L{L}/{alg}", exist_ok=True)
			fig.tight_layout()
			fig.savefig(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.pdf",format="pdf",bbox_inches="tight")
			#print(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
			plt.close()
			del ax, fig

	cor = np.array(cor)
	corErr = np.array(corErr)
	data = np.array([Ti, cor, corErr]).transpose()
	os.makedirs("output/autocorrelation",exist_ok=True)
	np.savetxt(f"output/autocorrelation/{name}_{alg}.csv",data,delimiter=",",header="T,tauExp,tauExp_error",comments="")
	os.system(f"/usr/bin/python3 plot_autocorrelation_time.py -alg {alg} -o {name}")