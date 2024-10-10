#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
from scipy import interpolate

obs = "charge"

f = lambda x, a, b:a*np.exp(-x/b)
alg = "lexic_metropolis"
params = {
			"charge":{"index":2, "ylabel":r"$\chi_t$"}, 
			"energy":{"index":4, "ylabel":r"$\rho_\mathcal{H}$"}, 
			"magnet":{"index":6, "ylabel":r"$\langle m\rangle $"}
			}
#colors_list = ["red", "black", "blue", "purple"]
#markers = dict(zip([4,8,16,20],["x","+","x","+"]))
X = []
ob = params[obs]["index"]
path = "output/cooling/L64/4-0"
indexes = [4,6,8,10,12,14,16]
fig, ax1 = plt.subplots()
for i in indexes:
	data = np.loadtxt(f"{path}/{alg} {i}.csv", delimiter=",", skiprows=1).transpose()
	ax1.errorbar(data[1], data[ob], data[ob+1], marker=".", color="black", ls="", label=f"$\\tau_{{\\mathrm{{cool}}}}={i}$")
	x=np.linspace(0, 4)
	f = interpolate.interp1d(data[1], data[ob], kind="cubic")
	X.append([i,data[ob][-1],data[ob+1][-1]])
	ax1.plot(x, f(x), color="black", linewidth=0.8)
ax1.legend()
ax1.set_xlabel(r"$T$", fontsize=20)
ax1.set_ylabel(params[obs]["ylabel"], fontsize=20)
#plt.savefig(f"output/plot/cooling/{obs}_{alg}.pdf", format="pdf",bbox_inches="tight")
X = np.array(X).transpose()
#np.savetxt("test.csv",X.transpose(),delimiter=",",header="tauCool,obs,error")

fig, ax2 = plt.subplots()
ax2.errorbar(X[0],X[1],X[2], ls="",marker=".")
x = np.linspace(1,20)
f = lambda x, a, b:a*x**(-b)
xfit = fit(X[0],X[1],X[2])
xfit.fiting(f)
ax2.plot(x,f(x,*xfit.opt))
plt.show()