#!/usr/bin/python3
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def f(x, tau, k):
	return k*np.exp(-x/tau)

def f1(x, tau, c, k):
	return c+k/(tau+x)

def f2(x, tau, c, k):
	return c+k*np.exp(-x/tau)#k/(tau+x)

def f3(x, k):
	return x*0+k

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

def fit2(f, X):
	opt, cov = curve_fit(f, X[0], X[1])

	chi2_by_dog = np.sum(((X[1]-f(X[0],*opt))/X[2])**2)/(X[0].size-opt.size)
	return opt, np.sqrt(cov[0,0]/X[0].size), chi2_by_dog

name = "record-0"

TQ = {1:[2,30,1], 1.5:[1,30,1], 2:[0,30,1], 2.5:[0,30,1], 3:[0,30,1], 3.5:[0,30,1], 4:[0,30,1]}
TM = {1:[4,100,1], 1.5:[3,30,1], 2:[3,30,1], 2.5:[1,30,1], 3:[0,30,1], 3.5:[0,30,1], 4:[0,30,1]}
TE = {1:[6,100,1], 1.5:[3,30,1], 2:[3,30,1], 2.5:[0,30,1], 3:[0,30,1], 3.5:[0,30,1], 4:[0,30,1]}

#TQ = {0.5:[0,30,1],1:[0,30,1], 1.5:[0,30,1], 2:[0,30,1], 2.5:[0,30,1], 3:[0,30,1], 3.5:[0,30,1], 4:[0,30,1]}
#TM = {0.5:[3,80,1],1:[2,60,1], 1.5:[1,30,1], 2:[1,30,1], 2.5:[0,30,1], 3:[0,30,1], 3.5:[0,30,1], 4:[0,30,1]}
#TE = {0.5:[4,80,1],1:[4,80,1], 1.5:[3,60,1], 2:[0,30,1], 2.5:[0,30,1], 3:[0,30,1], 3.5:[0,30,1], 4:[0,30,1]}


Algs = ["lexic_metropolis", "random_metropolis", "lexic_glauber", "random_glauber"]
#Algs = ["multi_cluster"]

for alg in Algs: 
	Q, M, E = [], [], []
	for temp in TQ:
		path = f"output/{name}/{temp}/{alg}.csv"
		data = np.loadtxt(path, delimiter=",", skiprows=1).transpose()
		tau, tauerr, chi2_by_dog = fit(data[0], TE[temp][0], TE[temp][1], TE[1][2])
		E.append([temp, tau, tauerr, chi2_by_dog])

		tau, tauerr, chi2_by_dog = fit(data[1], TQ[temp][0], TQ[temp][1], TQ[temp][2])
		Q.append([temp, tau, tauerr, chi2_by_dog])

		tau, tauerr, chi2_by_dog = fit(data[2], TM[temp][0], TM[temp][1], TM[temp][2])
		M.append([temp, tau, tauerr, chi2_by_dog])

	fig = plt.figure(dpi=140)
	ax = fig.add_subplot()

	setings = {
		"Q":{"data":Q,"color":"red","label":r"$\alpha_Q$","func":f1},
		"E":{"data":E,"color":"gray","label":r"$\alpha_E$","func":f1},
		"M":{"data":M,"color":"cyan","label":r"$\alpha_M$","func":f1}
		}

	for s in setings:
		st = setings[s]
		X = np.array(st["data"]).transpose()
		opt, err, chi2_by_dog = fit2(st["func"],X)
		x = np.linspace(0.5, 4, 200)
		ax.plot(x, st["func"](x,*opt), color=st["color"], linewidth=0.8)
		ax.plot(X[0], X[1], ls='', marker=".", color=st["color"], label=st["label"]+"="+f"{fix(opt[0],err)}")

	stats = "".join([r"$\tau=C+k/(\alpha+T)$"])
	#stats = "".join([r"$\tau=C+k\cdot\exp(-T/\alpha)$","\n",r"$\tau=C$"])
	bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
	ax.text(0.65, 0.85, stats, fontsize=12, bbox=bbox,transform=ax.transAxes, horizontalalignment='right')
	ax.legend()
	ax.set_xlabel(r"$T$", fontsize=14)
	ax.set_ylabel(r"$\tau$", fontsize=14)
	ax.set_title(alg, fontsize=14)
	fig.savefig(f"output/{alg}.png")
	print(f"output/{alg}.png", "finished")
	del fig
