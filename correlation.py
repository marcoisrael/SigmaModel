#!/usr/bin/python3
from numpy import exp, loadtxt, linspace, log
from plotClass import fit
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

Algs = ["lexic_metropolis", "lexic_glauber", "random_metropolis", "random_glauber", "multi_cluster"]
f = lambda x,a,b,c:b*exp(-x/a)+c
x = linspace(0.7,4,200)

for alg in Algs:
	path = f"output/tau_correlation/{alg}.csv"
	data = loadtxt(path, delimiter=",",skiprows=1)
	data = data[1:]

	fig = plt.figure(dpi=120)
	ax = fig.add_subplot()

	args = [
			{"label":"Energy", "color":"blue"}, 
			{"label":"Charge", "color":"orange"},
			{"label":"Magnetization", "color":"green"}
		]
	for i, arg in zip([0,1,2], args):
		ax.errorbar(data[:,0],data[:,1+2*i],data[:,2+2*i],ls="",marker=".", color=arg["color"])
		xfit = fit(data[:,0],data[:,1+2*i],data[:,2+2*i])
		
		xfit.fiting(f)
		ax.plot(x,f(x,*xfit.opt),linewidth=0.8, label=arg["label"], color=arg["color"])
		#print(xfit.opt[0],xfit.error[0])

	ax.set_xlabel(r"$T$", fontsize=14)
	ax.set_ylabel(r"$\tau$", fontsize=14)
	ax.set_title(" ".join(alg.split("_")).upper(), fontsize=14)
	ax.legend()

	stats = "".join([r"$\tau=k+\exp(-T/\alpha)$"])
	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='blue', alpha=0.3)
	ax.text(0.95, 0.7, stats, fontsize=13, bbox=bbox,transform=ax.transAxes, horizontalalignment='right')

	name = f"output/{alg}.png"
	fig.savefig(name)
	print(name, "finished")