#!/usr/bin/python3
import numpy as np
from scipy.optimize import curve_fit
import  matplotlib.pyplot as plt
import os

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

def f(x, tau, k):
	return k*np.exp(-x/tau)

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
	return X, opt, cov, chi2_by_dog

def plot(X, st):
	ax = fig.add_subplot(gs[st["gsx"], st["gsy"]])
	ax.set_xlabel(st["xlabel"], fontsize=14)
	ax.set_ylabel(st["ylabel"], fontsize=14)
	ax.set_title(st["title"], fontsize=14)
	x = np.linspace(t_min, t_max, 200)
	ax.errorbar(X[0], X[1], yerr=X[2], ls="", marker=".")
	ax.plot(x, f(x,*opt))
	if False: 
		stats = "".join([r"$c(t)=k\cdot\exp(-t/\tau)$","\n", r"$\tau =$",f"{fix(opt[0], np.sqrt(cov[0,0]/T.size))}","\n",r"$\chi^2\left/dog\right. =" f"$ {chi2_by_dog.round(4)}"])
	else:
		stats = "".join([r"$c(t)=k\cdot\exp(-t/\tau)$","\n", r"$\tau =$",f"{opt[0].round(4)}","\n",r"$\chi^2\left/dog\right. =" f"$ {chi2_by_dog.round(4)}"])

	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
	ax.text(0.95, 0.6, stats, fontsize=12, bbox=bbox,transform=ax.transAxes, horizontalalignment='right')

name = "record-0"
temp = 2.5
Algs = ["lexic_metropolis", "random_metropolis", "lexic_glauber", "random_glauber", "multi_cluster"]
# Algs = ["multi_cluster"]
t_min, t_max, sep = 0, 200, 1

if not os.path.isdir(f"output/plot/{name}/{temp}"):
	os.makedirs(f"output/plot/{name}/{temp}")

for alg in Algs:
	path = f"output/{name}/{temp}/{alg}.csv"
	data = np.loadtxt(path, delimiter=",", skiprows=1).transpose()

	fig = plt.figure(figsize=(16,9))
	gs = fig.add_gridspec(2, 2)	

	st = {"xlabel":r"$t$", "ylabel":r"$C_{E,E}(t)$", "title":"Energy density", "gsx":1, "gsy":0}
	X, opt, cov, chi2_by_dog = fit(data[0], t_min, t_max, sep)
	plot(X, st)

	st = {"xlabel":r"$t$", "ylabel":r"$C_{Q,Q}(t)$", "title":"Topological charge", "gsx":0, "gsy":0}
	X, opt, cov, chi2_by_dog = fit(data[1], t_min, t_max, sep)
	plot(X, st)

	st = {"xlabel":r"$t$", "ylabel":r"$C_{M,M}(t)$", "title":"Magnetization density", "gsx":0, "gsy":1}
	X, opt, cov, chi2_by_dog = fit(data[2], t_min, t_max, sep)
	plot(X, st)
	# plt.tight_layout()
	fig.suptitle(alg,fontsize=16)
	plt.subplots_adjust(hspace=0.3, wspace=0.2)
	plot_name = f"output/plot/{name}/{temp}/{alg}.png"
	fig.savefig(plot_name)
	print(plot_name, "finished")
	del fig, data