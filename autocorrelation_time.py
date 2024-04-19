#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit

Algs = ["lexic_metropolis", "lexic_glauber", "random_metropolis", "random_glauber", "multi_cluster"]
#f = lambda x,L,k,x0,c0:np.exp(c0+L/(1+np.exp(-k*(x-x0))))

#Algs = [ "multi_cluster"]
f = lambda x,L,k,x0,c0:L*np.exp(k*(x-x0))+c0

T = np.array([0.5,0.75,1.0,1.5,2.0,2.5,3.0,3.5,4.0])
x = np.linspace(0.5,4.0,200)

args = [
		{"label":"Energy", "color":"blue"}, 
		{"label":"Charge", "color":"orange"},
		{"label":"Magnetization", "color":"green"}
	]

for alg in Algs:
	atime = []
	atimeErr = []

	for temp in T:
		path = f"output/correlation/{alg}/{alg}_{temp}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1)

		tau = np.array([0.5,0.5,0.5])
		tauErr = np.array([0,0,0])
		c0 = np.array([data[0,2]/abs(data[0,1]),data[0,4]/abs(data[0,3]),data[0,6]/abs(data[0,5])])
		for i in np.arange(1,data.shape[0]):
			obs = np.array([data[i,1]/data[0,1], data[i,3]/data[0,3], data[i,5]/data[0,5]])
			tau = tau + obs
			tauErr = tauErr + obs*(np.array([data[i,2]/data[i,1],data[i,4]/data[i,3],data[i,6]/data[i,5]])+c0)
		atime.append(tau)
		atimeErr.append(tauErr)

	atime = np.array(atime)
	atimeErr = np.array(atimeErr)

	fig, (ax1, ax2) = plt.subplots(1,2,dpi=120,figsize=(16,9))

	for ax in [ax1, ax2]:
		for i, arg in zip([0,1,2], args):
			ax.errorbar(1/T,atime[:,i],atimeErr[:,i], color=arg["color"], fmt='o', capsize=3, elinewidth=2, label=arg["label"])
			#xfit = fit(1/T,atime[:,i],atimeErr[:,i])
			#xfit.fiting(f)
			#ax.plot(1/x,f(1/x,*xfit.opt),linewidth=0.8, label=arg["label"], color=arg["color"])

		ax.set_xlabel(r"$1/T$", fontsize=14)
		ax.legend()
		ax.grid(True)

	fig.suptitle(" ".join(alg.split("_")), fontsize=16)
	ax1.set_ylabel(r"$\log(\tau)$", fontsize=14)
	ax1.set_yscale("log")
	ax2.set_ylabel(r"$\tau$", fontsize=14)
	fig.savefig(f"output/plot/autocorrelation_time/{alg}_2.png")

