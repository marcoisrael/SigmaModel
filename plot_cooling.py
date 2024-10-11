#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
from scipy import interpolate
obs = "charge"
alg = "random_glauber"
params = {
			"charge":{"index":2, "ylabel":r"$\chi_t$"}, 
			"energy":{"index":4, "ylabel":r"$\rho_\mathcal{H}$"}, 
			"magnet":{"index":6, "ylabel":r"$\langle m\rangle $"}
			}
colors = {4:"red",6:"blue",8:"purple"}
lines = {4:(0,(3,3)),6:(0,(5,1)),8:(0,(5,5))}
#markers = dict(zip([4,8,16,20],["x","+","x","+"]))
X = []
ob = params[obs]["index"]
path = "output/cooling/L64/4-0"
indexes = [4,6,8,10,12,14,16]
fig1, ax1 = plt.subplots()
for i in indexes:
	data = np.loadtxt(f"{path}/{alg} {i}.csv", delimiter=",", skiprows=1).transpose()
	X.append([i,data[ob][-1],data[ob+1][-1]])
	if i in [4,6,8]:
		ax1.errorbar(data[0], data[ob], data[ob+1],color=colors[i], ls="",marker=".",alpha=0.3)
		f = lambda x, a, b,c:c/(1+np.exp((x-a)/b))
		xfit = fit(data[0],data[ob],data[ob+1])
		xfit.fiting(f)
		x = np.linspace(0,i,200)
		ax1.plot(x, f(x,*xfit.opt), color=colors[i], linewidth=0.8, linestyle=lines[i],label=f"$\\tau_{{\\mathrm{{cool}}}}={i}$")
ax1.legend()
ax1.set_xlabel(r"$t$", fontsize=18)
ax1.set_ylabel(params[obs]["ylabel"], fontsize=18)
#fig1.savefig(f"output/plot/cooling/{obs}_{alg}.pdf", format="pdf",bbox_inches="tight")
X = np.array(X).transpose()
#np.savetxt("test.csv",X.transpose(),delimiter=",",header="tauCool,obs,error")
fig2, ax2 = plt.subplots()
ax2.errorbar(X[0],X[1],X[2], ls="",color="red",marker=".",alpha=0.3)
x = np.linspace(1,20)
f = lambda x, a, b:a*x**(-b)
xfit = fit(X[0],X[1],X[2])
xfit.fiting(f)
print(fix(xfit.opt[1],xfit.error[1]))
ax2.plot(x,f(x,*xfit.opt),linewidth=0.8,color="blue",linestyle=(0,(3,3)))
ax2.set_ylabel(params[obs]["ylabel"], fontsize=18)
ax2.set_xlabel(r"$\tau_{\mathrm{cool}}$",fontsize=18)
#fig2.savefig(f"output/plot/cooling/scaling_law_{obs}_{alg}.pdf", format="pdf",bbox_inches="tight")