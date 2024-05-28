#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())
import os
make_temp_plots=False
name = "charge"
alg = "lexic_metropolis"
L = 128
T = np.array([0.6,0.7,0.8,0.9,1.0,2.0,3.0,4.0])
f = lambda x, b: np.exp(-x/b)
obs = {"charge":{"label":r"$\frac{C_{Q,Q}(t)}{C_{Q,Q}(0)}$","index":1,"sym":"Q"},
		"magnetization":{"label":r"$\frac{C_{M,M}(t)}{C_{M,M}(0)}$","index":1,"sym":"M"}}
spacing = {60:r"$t_{60}$",30:r"$t_{30}$",20:r"$t_{20}$",10:r"$t_{10}$",5:r"$t_{5}$",1:r"$t$"}
cor = []
corErr = []
cor2 = []
cor2Err = []
for temp in T:
	n = np.ceil(4*575.21*np.exp(-temp/0.1558)+0.5)
	
	path = f"output/record-1/L{L}/{alg}/{temp}.csv"
	data = np.loadtxt(path, delimiter=",", skiprows=1)
	X = []
	for t in np.arange(0,10):
		X.append(correlation(data[:,obs["charge"]["index"]], t))
	X = np.array(X)

	t, q, qErr = X[:,0],X[:,1]/X[0,1],X[:,2]/X[0,1]
	x = np.linspace(t[0],t[-1],500)
	xfit = fit(t,q,qErr)
	xfit.fiting(f, args={"bounds":((0,np.inf))})
	cor.append(np.max([n*xfit.opt[0],0.5]))
	corErr.append(n*xfit.error[0])
	texp = 0
	texpErr = 0
	for i in np.arange(0,int(np.ceil(4*xfit.opt[0]))):
		texp = texp+0.5*X[i,1]/X[:,1].max()
		texpErr = texpErr+0.5*X[i,2]/X[:,1].max()
	cor2.append(n*texp)
	cor2Err.append(n*texpErr)
	#print(xfit.opt[0], n*xfit.opt[0], n*texp)
	if make_temp_plots:
		fig, ax = plt.subplots(dpi=120,tight_layout=True)

		ax.plot(x, f(x, *xfit.opt), linewidth=0.8, color="black", label="Fitting")
		ax.errorbar(t,q,qErr, fmt='o', capsize=1, elinewidth=1, markersize=1, color="blue", label="Data")
		ax.text(0.5 ,0.9, r"$\tau_{exp}=$"+fix(n*xfit.opt[0],n*xfit.error[0])+"\n"+r"$\chi^2/dof=$"+f"{xfit.chisq_by_dof}", 
			horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
		ax.set_xlabel(r"$\t$", fontsize=14)
		ax.set_ylabel(obs[name]["label"], rotation="horizontal", fontsize=18, ha="right")
		ax.grid(True)
		ax.legend()
		ax.set_title(f"{alg}, temp = {temp}", fontsize=15)
		#print(temp, xfit.opt[-1])
		if not os.path.isdir(f"output/plot/{name}/L{L}/{alg}"):
			os.makedirs(f"output/plot/{name}/L{L}/{alg}")
		fig.tight_layout()
		fig.savefig(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
		print(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
		plt.close()
		del ax, fig
fig, (ax1,ax2) = plt.subplots(1,2,dpi=120,figsize=(16,7))
x = np.linspace(0.6,4.0,200)
cor2 = np.array(cor2)
cor = np.array(cor)
corErr = np.array(corErr)
cor2Err = np.array(cor2Err)
f = lambda x, a, b:a*np.exp(-x/b)+0.5
f = lambda x, a, b:a*x**(-b)+0.5
xfit = fit(T,cor,corErr)
xfit.fiting(f)
ax2.errorbar(T,cor,corErr, fmt='o', capsize=3, elinewidth=1, markersize=2, label=r"$\tau_{exp}$", color="b")
ax2.plot(x, f(x,*xfit.opt), linewidth=0.8, color="b")
ax2.text(0.5 ,0.9, r"$\alpha_{exp}=$"+fix(xfit.opt[1],xfit.error[1])+"\n"+r"$\chi^2/dof=$"+f"{xfit.chisq_by_dof}", 
		horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes, fontsize=12)

xfit = fit(T,cor2,cor2Err)
xfit.fiting(f)
ax2.text(0.5 ,0.75, r"$\alpha_{int}=$"+fix(xfit.opt[1],xfit.error[1])+"\n"+r"$\chi^2/dof=$"+f"{xfit.chisq_by_dof}", 
		horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes, fontsize=12)

ax2.errorbar(T, cor2, cor2Err, fmt='o', capsize=3, elinewidth=1, markersize=2, label=r"$\tau_{int}$", color="r")
ax2.plot(x, f(x,*xfit.opt), linewidth=0.8, color="r")
ax2.set_xlabel(r"$T$",fontsize=16)
ax2.set_ylabel(r"$\tau$",fontsize=18)
ax2.legend() 

startTemp = 4
endTemp = 0
path = f"output/cooling/jkL64/{startTemp}-{endTemp}"
qmax = []
qmaxErr = []
x = np.linspace(0.5, 4.0,100)
f = lambda x, a, b, c, d: a+b*x+c*x**2+d*x**3
for tmax in np.array([4,5,6,7]):
	data = np.loadtxt(f"{path}/{alg} {tmax}.csv", delimiter=",", skiprows=1)[:-1]
	tq, temp, q, qErr = data[:,0], data[:,1], data[:,2], data[:,3]
	ax1.errorbar(temp, q, qErr, fmt='o', capsize=1, elinewidth=1, markersize=2, color=colors_list[2*tmax+5],
		label=r"$\tau_{cool}=$"+str(int(tq.max())))
	xfit = fit(temp, q, qErr)
	xfit.fiting(f)
	ax1.plot(x, f(x,*xfit.opt), linewidth=0.8, color=colors_list[2*tmax+5])

data = np.loadtxt(f"output/therm/L32/{alg}/4.0-0.6-30.csv", delimiter=",", skiprows=1)[:-2]
tq, temp, q, qErr = data[:,0], data[:,1], data[:,2], data[:,3]
ax1.errorbar(temp, q, qErr, fmt='o', capsize=1, elinewidth=1, markersize=2, color=colors_list[0], 
		label="Therm")
#xfit = fit(temp, q, qErr)
#f = lambda x, a, b: b*x**b

#xfit.fiting(f)
#ax1.plot(x, f(x,*xfit.opt), linewidth=0.8, color=colors_list[0])


ax1.set_xlabel(r"$T$",fontsize=16)
ax1.set_ylabel(r"$\frac{\left<Q^2\right>_f}{V}$", rotation="horizontal", ha="right",fontsize=22)
ax1.legend()
ax1.grid(True)
ax2.grid(True)
#fig.tight_layout()
#ax1.set_yscale("log")
fig.suptitle(f"{alg}", fontsize=16)
fig.savefig(f"output/{alg}L{L}.png")
print(f"output/{alg}L{L}.png")