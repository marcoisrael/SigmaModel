#!/usr/bin/python3
from numpy import exp, loadtxt, linspace
from plotClass import fit
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

alg = "lexic_metropolis"
f = lambda x,a,b,c:b*exp(-x/a)+c

path = f"output/tau_correlation/{alg}.csv"
data = loadtxt(path, delimiter=",",skiprows=1)
i = 4

ax = plt.figure().add_subplot()
ax.errorbar(data[:,0],data[:,1+i],data[:,2+i],ls="",marker=".")
xfit = fit(data[:,0],data[:,1+i],data[:,2+i])
x = linspace(0.5,4,200)
xfit.fiting(f)
ax.plot(x,f(x,*xfit.opt),linewidth=0.8)
plt.show()