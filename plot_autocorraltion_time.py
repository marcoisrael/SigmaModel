#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import*
import os
L=128
name, alg = "charge", "lexic_metropolis"
f = lambda x, a, b:a*np.exp(-x/b)

data = np.loadtxt(f"output/autocorrelation/{name}_{alg}.csv",skiprows=1,delimiter=",")[2:].transpose()
x = np.linspace(data[0][0],data[0][-1],200)

xfit = fit(data[0],data[1],data[2])
xfit.fiting(f)
fig, ax = plt.subplots()
ax.errorbar(data[0],data[1],data[2], fmt='o', capsize=3, elinewidth=1, markersize=2, label=r"$\tau_{exp}$", color="red")
#ax.errorbar(data[0],data[3],data[4], fmt='o', capsize=3, elinewidth=1, markersize=2, label=r"$\tau_{exp}$", color="blue")

ax.plot(x, f(x,*xfit.opt), linewidth=0.8, color="black")
#ax.text(0.5 ,0.9, r"$z=$"+fix(xfit.opt[1],xfit.error[1]), 
#		horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=16)

print(xfit.opt)
ax.set_xlabel(r"$T$",fontsize=14)
ax.set_ylabel(r"$\tau_{\mathrm{exp}}$",fontsize=14)
#ax.legend() 

title =Algs[alg]
i = obs[name]["sym"]
if not os.path.isdir(f"output/plot/{name}/L{L}/{alg}"):
	os.makedirs(f"output/plot/{name}/L{L}/{alg}")
fig.savefig(f"output/plot/{name}/autocorrelation_{alg}_L{L}_{i}.pdf",format="pdf",bbox_inches="tight")
print(f"output/plot/{name}/autocorrelation_{alg}_L{L}_{i}.pdf")