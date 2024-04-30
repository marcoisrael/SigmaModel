#!/usr/bin/python3
import numpy as np
from plotClass import correlation, fit
import os

Algs = ["lexic_metropolis", "random_metropolis", "lexic_glauber", "random_glauber", "multi_cluster"]
Algs = ["lexic_metropolis"]
obs = {"charge":{"label":"Q","index":2}}
for alg in Algs:
	for temp in [0.9]:
		path = f"output/record-1/{alg}/{temp}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		T = np.arange(0,20)
		X = []
		for t in T:
			X.append(correlation(data[:,obs["charge"]["index"]], t))

		X = np.array(X)
		label = obs["charge"]["label"]
		name = f"output/correlation/{alg}/{temp}_{label}.csv"
		if not os.path.isdir(f"output/correlation/{alg}/"):
			os.makedirs(f"output/correlation/{alg}/")
		np.savetxt(name, X, delimiter=",",header="t,c,cErr", comments="")
		print(name, "finished")
