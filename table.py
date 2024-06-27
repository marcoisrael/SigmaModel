#!/usr/bin/python3
import numpy as np
from plotClass import *
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())
import os
name = "charge"
L = 128
tc = 0.74

Algs = {
		"lexic_metropolis":"Lexicographical Metropolis",
		"random_metropolis":"Random Metropolis",
		"lexic_glauber":"Lexicographical Glauber",
		"random_glauber":"Random Glauber",
		#"multi_cluster":"Multi Cluster",
		}
obs = {
		"charge":{"label":r"$\frac{C_{Q,Q}(t)}{C_{Q,Q}(0)}$","index":1,"sym":"Q"},
		"magnetization":{"label":r"$\frac{C_{M,M}(t)}{C_{M,M}(0)}$","index":2,"sym":"M"},
		"energy":{"label":r"$\frac{C_{M,M}(t)}{C_{M,M}(0)}$","index":0,"sym":"E"}
		}

T = np.array([0.9,1.0,1.2,1.4,1.6,1.8,2.0])
#T = np.array([1.0,1.2,1.4,1.6,1.8,2.0])

N = np.ones_like(T)
#N[0], N[1] =  4, 3
#N[0] = 3

for alg in Algs:
	f = lambda x, b, A: A*np.exp(-x/b)

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
		
	x = np.linspace(T[0],T[-1],200)
	cor2 = np.array(cor2)
	cor = np.array(cor)
	corErr = np.array(corErr)
	cor2Err = np.array(cor2Err)
	f = lambda x, a, b:a*(x-tc)**(-b)
	#f = lambda x, a, b:a*x**(-b)

	xfit = fit(T,cor,corErr)
	xfit.fiting(f)

	print(f"z = ", fix(xfit.opt[1], xfit.error[1]), alg)

	#data = np.array([T, cor, corErr]).transpose()
	#np.savetxt(f"output/send/autocorrelation_{name}_{alg}.csv", data, 
	#	delimiter=",",header="T,tau,tau_error",comments="", fmt="%16f")
