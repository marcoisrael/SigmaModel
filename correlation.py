#!/usr/bin/python3
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def f(x, tau, k):
	return k*np.exp(-x/tau)

def f2(x, tau, k, c):
	return c+k/(tau+x)
def correlation(x, t):
	mean = x.mean()
	n = x.size-t
	if t==0:
		c = (x-mean)*(x-mean)
	else:
		c = (x[0:-t]-mean)*(x[t:]-mean)

	s = np.sqrt((c*c).mean()-c.mean()**2)
	serr = s/np.sqrt(n)
	return t, c.mean(), serr

def fix(x,dx):
	before, after = str(dx).split('.')
	i = 0
	for d in after:
		i +=1
		if  d != "0":
			val=  round(float(d+"."+after[i:]))
			break
	y = round(x,i)
	if i>len(str(y).split('.')[1]):
		y = f"{y}{'0'*(i-len(str(y).split('.')[1]))}"
	return f"{y}({val})"

def fit(data, t_min,t_max, sep):
	X = []
	for t in np.arange(t_min, t_max, sep):
		X.append(correlation(data,t))

	X = np.array(X).transpose()
	opt, cov = curve_fit(f, X[0], X[1], p0=[1, 0])

	chi2_by_dog = np.sum(((X[1]-f(X[0],*opt))/X[2])**2)/(X[0].size-opt.size)
	return opt[0], np.sqrt(cov[0,0]/X[0].size), chi2_by_dog

def fit2(X):
	opt, cov = curve_fit(f2, X[0], X[1])

	chi2_by_dog = np.sum(((X[1]-f2(X[0],*opt))/X[2])**2)/(X[0].size-opt.size)
	return opt, np.sqrt(cov[0,0]/X[0].size), chi2_by_dog

name = "record-0"
alg = "lexic_metropolis"


Q, M, E = [], [], []
T = [1.5, 2, 2.5, 3, 3.5, 4]
T_max = [200, 150, 100, 50, 25, 25]
t_min, sep = 0, 1 
for i in np.arange(len(T)):
	t_max = T_max[i]
	temp = T[i]
	path = f"output/{name}/{temp}/{alg}.csv"
	data = np.loadtxt(path, delimiter=",", skiprows=1).transpose()
	tau, tauerr, chi2_by_dog = fit(data[0], t_min, t_max, sep)
	E.append([temp, tau, tauerr, chi2_by_dog])

	tau, tauerr, chi2_by_dog = fit(data[1], t_min, t_max, sep)
	Q.append([temp, tau, tauerr, chi2_by_dog])

	tau, tauerr, chi2_by_dog = fit(data[2], t_min, t_max, sep)
	M.append([temp, tau, tauerr, chi2_by_dog])

fig = plt.figure(dpi=140)
ax = fig.add_subplot()

setings = {
	"Q":{"data":Q,"color":"red","label":r"$\tau_Q$"},
	"E":{"data":E,"color":"gray","label":r"$\tau_E$"},
	"M":{"data":M,"color":"cyan","label":r"$\tau_M$"}
	}

for s in setings:
	st = setings[s]
	X = np.array(st["data"]).transpose()
	opt, err, chi2_by_dog = fit2(X)
	print(chi2_by_dog)
	x = np.linspace(1, 4, 200)
	ax.plot(x, f2(x,*opt))
	ax.errorbar(X[0], X[1], yerr=X[2], ls='', marker=".", label=st["label"]+"="+f"{fix(opt[0],err)}", color=st["color"])

stats = "".join([r"$F(\tau)=C+k/(\alpha+\tau)$"])
bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
ax.text(0.95, 0.3, stats, fontsize=12, bbox=bbox,transform=ax.transAxes, horizontalalignment='right')
ax.legend()
ax.set_xlabel(r"$T$", fontsize=14)
ax.set_ylabel(r"$\tau$", fontsize=14)
ax.set_title(alg, fontsize=14)
fig.savefig(f"output/{alg}.png")