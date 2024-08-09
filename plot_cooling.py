#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
from scipy import interpolate

alg = "lexic_metropolis"
params = {
			"charge":{"index":2, "ylabel":r"$\chi_{t_f}$"}, 
			"energy":{"index":4, "ylabel":r"$E_f$"}, 
			"magnet":{"index":6, "ylabel":r"$\chi_{m_f}$"}
			}

markers = dict(zip([4,8,16,20],["2",".","x","+"]))
for obs in ["charge", "energy", "magnet"]:
	ob = params[obs]["index"]
	path = "output/cooling/FastCooling/4-0"
	indexes = [4,8,16,20]
	fig, ax = plt.subplots()
	for i in indexes:
		data = np.loadtxt(f"{path}/{alg} {i}.csv", delimiter=",", skiprows=1).transpose()
		ax.errorbar(data[1], data[ob], data[ob+1], marker=markers[i], color="black", ls="", label=r"$\tau_{cool}$"+f"={i}")
		x=np.linspace(0, 4)
		f = interpolate.interp1d(data[1], data[ob], kind="cubic")
		ax.plot(x, f(x), color="black", linewidth=0.8)
	ax.legend()
	ax.grid(True)
	ax.set_xlabel(r"$T$", fontsize=20)
	ax.set_ylabel(params[obs]["ylabel"], fontsize=20)
	plt.savefig(f"output/plot/cooling/{obs}_{alg}.svg", format="svg")