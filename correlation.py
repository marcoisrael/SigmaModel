#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os	
alg_list = ["lexic_metropolis", "lexic_glauber", "random_metropolis", "random_glauber"]
tmax = 30
for temp in [4]:
	for alg in alg_list:
		data = pd.read_csv(f"output/thermalized/{temp}/{alg}.csv")
		ac = (data*data).mean()-data.mean()**2
		for t in np.arange(1,tmax):
			ac = pd.concat([ac,(data*data.shift(t)).dropna().mean()-data.mean()**2],axis=1)
		point = 3
		ac = ac.transpose()
		ac = ac.iloc[point:]
		t = np.arange(point,tmax)
		fig = plt.figure(dpi=140,figsize=(16,9))
		gs = fig.add_gridspec(2, 2,  width_ratios=(1,1))
		def f(x, a, b, c):
			return c+a/(x+b)
		x = np.linspace(point,tmax)
		opt, cov = curve_fit(f, t, ac["H/V"])
		ax1 = fig.add_subplot(gs[0,0])
		ax1.plot(x,f(x, *opt))
		ax1.plot(t, ac["H/V"],color="red", label=f"$H/V$", ls="",marker=".")
		stats = "".join([r"$c(t)=k+c_0/(\tau + t)$","\n", r"$\tau =$",f"{opt[1].round(4)}"])
		bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
		ax1.text(0.95, 0.8, stats, fontsize=14, bbox=bbox,transform=ax1.transAxes, horizontalalignment='right')
		ax1.set_xlabel("t", fontsize=15)
		ax1.set_ylabel(r"$C_{E,E}(t)$",fontsize=15)
		ax1.set_title("Energy density",fontsize=15)

		opt, cov = curve_fit(f, t, ac["chi_t"])
		ax2 = fig.add_subplot(gs[0,1])
		ax2.plot(x,f(x, *opt))
		ax2.plot(t, ac["chi_t"],color="purple", label=f"$\chi_t$", ls="", marker=".")
		stats = "".join([r"$c(t)=k+c_0/(\tau + t)$","\n", r"$\tau =$",f"{opt[1].round(4)}"])
		bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
		ax2.text(0.95, 0.8, stats, fontsize=14, bbox=bbox,transform=ax2.transAxes, horizontalalignment='right')
		ax2.set_xlabel("t",fontsize=15)
		ax2.set_ylabel(r"$C_{Q,Q}(t)$",fontsize=15)
		ax2.set_title("Topological charge",fontsize=15)

		opt, cov = curve_fit(f, t, ac["chi_m"])
		ax3 = fig.add_subplot(gs[1,0])
		ax3.plot(x,f(x, *opt))
		ax3.plot(t, ac["chi_m"],color="orange", label=f"$\chi_m$",ls="", marker=".")
		stats = "".join([r"$c(t)=k+c_0/(\tau + t)$","\n", r"$\tau =$",f"{opt[1].round(4)}"])
		bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
		ax3.text(0.95, 0.8, stats, fontsize=14, bbox=bbox,transform=ax3.transAxes, horizontalalignment='right')
		ax3.set_xlabel("t",fontsize=15)
		ax3.set_ylabel(r"$C_{M,M}(t)$",fontsize=15)
		ax3.set_title("Magnetization",fontsize=15)
		title = " ".join(alg.split("_"))
		fig.suptitle(title,fontsize=16)
		if not os.path.isdir(f"output/plot/thermalized/{temp}"):
			os.makedirs(f"output/plot/thermalized/{temp}")
		fig.savefig(f"output/plot/thermalized/{temp}/{alg}.png")
		plt.close(fig) 
		print(f"{alg}, Temp = {temp} done.")
