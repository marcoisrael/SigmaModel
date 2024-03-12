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
	return c.mean(), serr

def f(x, tau, c):
	return c*np.exp(-x/tau)

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

def fit(data, t_min,t_max):
	X = []
	T = np.arange(t_min, t_max)
	n = t_max-t_min
	for t in T:
		X.append(correlation(data,t))

	X = np.array(X).transpose()

	opt, cov = curve_fit(f, T, X[0])

	chi2_by_dog = np.sum(((X[0]-f(T,*opt))/X[1])**2)/(T.size-opt.size)
	print(chi2_by_dog.round(4), fix(opt[0], np.sqrt(cov[0,0]/n)))
	print(opt[0])
	return X, opt, cov, chi2_by_dog

def plot(X, st):
	ax = fig.add_subplot(gs[st["gsx"], st["gsy"]])
	ax.set_xlabel(st["xlabel"], fontsize=14)
	ax.set_ylabel(st["ylabel"], fontsize=14)
	ax.set_title(st["title"], fontsize=14)
	x = np.linspace(t_min, t_max, 200)
	T = np.arange(t_min, t_max)
	ax.errorbar(T, X[0], yerr=X[1], ls="", marker=".")
	ax.plot(x, f(x,*opt))
	stats = "".join([r"$c(t)=k\exp(-t/\tau)$","\n", r"$\tau =$",f"{fix(opt[0], np.sqrt(cov[0,0]/T.size))}","\n",r"$\chi^2\left/dog\right. =" f"$ {chi2_by_dog.round(4)}"])
	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
	ax.text(0.95, 0.6, stats, fontsize=12, bbox=bbox,transform=ax.transAxes, horizontalalignment='right')

temp = 4
Algs = ["lexic_metropolis", "random_metropolis", "lexic_glauber", "random_glauber"]

if not os.path.isdir(f"output/plot/thermalized/{temp}"):
	os.makedirs(f"output/plot/thermalized/{temp}")

for alg in Algs:
	path = f"output/thermalized/{temp}/{alg}.csv"
	data = np.loadtxt(path, delimiter=",", skiprows=1).transpose()

	fig = plt.figure(figsize=(16,9))
	gs = fig.add_gridspec(2, 2)	

	t_min, t_max = 0, 30
	st = {"xlabel":r"$t$", "ylabel":r"$C_{E,E}(t)$", "title":"Energy density", "gsx":1, "gsy":0}
	X, opt, cov, chi2_by_dog = fit(data[0], t_min, t_max)
	plot(X, st)

	st = {"xlabel":r"$t$", "ylabel":r"$C_{Q,Q}(t)$", "title":"Topological charge", "gsx":0, "gsy":0}
	X, opt, cov, chi2_by_dog = fit(data[1], t_min, t_max)
	plot(X, st)

	st = {"xlabel":r"$t$", "ylabel":r"$C_{M,M}(t)$", "title":"Magnetization density", "gsx":0, "gsy":1}
	X, opt, cov, chi2_by_dog = fit(data[2], t_min, t_max)
	plot(X, st)
	# plt.tight_layout()
	fig.suptitle(alg,fontsize=16)
	plt.subplots_adjust(hspace=0.3, wspace=0.2)
	name = f"output/plot/thermalized/{temp}/{alg}.png"
	fig.savefig(name)
	del fig