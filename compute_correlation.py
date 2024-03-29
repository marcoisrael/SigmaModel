#!/usr/bin/python3
import numpy as np
from plotClass import correlation, fit

Algs = ["lexic_metropolis", "random_metropolis", "lexic_glauber", "random_glauber", "multi_cluster"]
Algs = ["lexic_metropolis"]
for alg in Algs:
	for temp in [0.5,0.75,1,1.5,2]:
		path = f"output/record-1/{temp}/{alg}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)
		T = np.arange(0,1000)
		X = []
		for t in T:
			X.append(correlation(data, t))

		X = np.array(X)

		head = "tau_E,tau_E_error,tau_Q,tau_Q_error,tau_M,tau_M_error"
		name = f"output/correlation/{alg}_{temp}.csv"
		np.savetxt(name, X, delimiter=",",header=head)
		print(name, "finished")
