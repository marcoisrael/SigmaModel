#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os	
tmax = 10
temp= 4
alg_list = ["lexic_metropolis", "lexic_glauber", "random_metropolis", "random_glauber", "multi_cluster"]
# ~ alg_list = ["single_cluster"]
for alg in alg_list:
	data = pd.read_csv(f"output/thermalized/{temp}/{alg}.csv")

	ac = (data**2).mean()- data.mean()**2
	for t in np.arange(1,tmax):
		ac = pd.concat([ac,(data*data.shift(t)).mean()-data.mean()**2],axis=1)

	ac = ac.transpose()
	t = np.arange(0,tmax)
	fig = plt.figure(dpi=140,figsize=(16,9))
	gs = fig.add_gridspec(2, 2,  width_ratios=(1,1))
	def f(x, a, b):
		return a*np.exp(-b*x)
	x = np.linspace(0,tmax)
	opt, cov = curve_fit(f, t, ac["H/V"])
	ax1 = fig.add_subplot(gs[0,0])
	ax1.plot(x,f(x, *opt))
	ax1.plot(t, ac["H/V"],color="red", label=f"$H/V$", ls="",marker=".")
	stats = "".join([r"$c(\tau)=C\cdot\exp(-\alpha\cdot\tau)$","\n", r"$\alpha =$",f"{opt[1].round(4)}"])
	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
	ax1.text(0.95, 0.8, stats, fontsize=14, bbox=bbox,transform=ax1.transAxes, horizontalalignment='right')
	ax1.set_xlabel("t", fontsize=15)
	ax1.set_ylabel(r"$C_{E,E}(\tau)$",fontsize=15)
	ax1.set_title("Energy density",fontsize=15)

	opt, cov = curve_fit(f, t, ac["chi_t"])
	ax2 = fig.add_subplot(gs[0,1])
	ax2.plot(x,f(x, *opt))
	ax2.plot(t, ac["chi_t"],color="purple", label=f"$\chi_t$", ls="", marker=".")
	stats = "".join([r"$c(\tau)=C\cdot\exp(-\alpha\cdot\tau)$","\n", r"$\alpha =$",f"{opt[1].round(4)}"])
	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
	ax2.text(0.95, 0.8, stats, fontsize=14, bbox=bbox,transform=ax2.transAxes, horizontalalignment='right')
	ax2.set_xlabel("t",fontsize=15)
	ax2.set_ylabel(r"$C_{Q,Q}(\tau)$",fontsize=15)
	ax2.set_title("Topological charge",fontsize=15)
	
	opt, cov = curve_fit(f, t, ac["chi_m"])
	ax3 = fig.add_subplot(gs[1,0])
	ax3.plot(x,f(x, *opt))
	ax3.plot(t, ac["chi_m"],color="orange", label=f"$\chi_m$",ls="", marker=".")
	stats = "".join([r"$c(\tau)=C\cdot\exp(-\alpha\cdot\tau)+k$","\n", r"$\alpha =$",f"{opt[1].round(4)}"])
	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
	ax3.text(0.95, 0.8, stats, fontsize=14, bbox=bbox,transform=ax3.transAxes, horizontalalignment='right')
	ax3.set_xlabel("t",fontsize=15)
	ax3.set_ylabel(r"$C_{M,M}(\tau)$",fontsize=15)
	ax3.set_title("Magnetization",fontsize=15)
	title = " ".join(alg.split("_"))
	fig.suptitle(title,fontsize=16)
	if not os.path.isdir(f"output/plot/thermalized/{temp}"):
		os.makedirs(f"output/plot/thermalized/{temp}")
	fig.savefig(f"output/plot/thermalized/{temp}/{alg}.png")
	print(f"{alg} done")
