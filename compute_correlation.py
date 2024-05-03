#!/usr/bin/python3
import numpy as np
from plotClass import correlation, fit
import os
o = "charge"
#Algs = ["multi_cluster","lexic_metropolis","random_metropolis", "lexic_glauber", "random_glauber"]
#T = np.array([0.8,0.9,1.0,2.0,3.0,4.0])
obs = {"charge":{"label":"Q","index":1}, "magnetization":{"label":"M","index":2}}

Algs = ["random_metropolis","lexic_metropolis","random_glauber"]
Temp = np.array([0.9])

for alg in Algs:
	for temp in Temp:
		lb = obs[o]["label"]
		path = f"output/record-1/{alg}/{temp}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		T = np.arange(0,10)
		X = []
		for t in T:
			X.append(correlation(data[:,obs[o]["index"]], t))

		X = np.array(X)
		label = obs[o]["label"]
		name = f"output/{o}/{alg}/{temp}_{label}.csv"
		if not os.path.isdir(f"output/{o}/{alg}/"):
			os.makedirs(f"output/{o}/{alg}/")
		np.savetxt(name, X, delimiter=",",header="t,c,cErr", comments="")
		print(name, "finished")
