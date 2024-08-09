#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def correlation(X, t):
	X_mean = X.mean()
	N = X.size-t
	if t==0:
		C = (X-X_mean)**2
	else:
		C = (X[0:-t]-X_mean)*(X[t:]-X_mean)
	C_mean = C.mean()
	C_Var = (C**2).mean()-C_mean**2
	C_Error = np.sqrt(C_Var/N)
	return t,C_mean,C_Error
	

def chi2_by_dof(y0, y, yerr, dof):
	ss = (y-y0)**2/yerr
	return ss.sum()/dof

def fix(x,dx):
	before, after = str(dx).split('.')
	i = 0
	val=0
	for d in after:
		i +=1
		if  d != "0":
			val=  round(float(d+"."+after[i:]))
			break
	y = round(x,i)
	if i>len(str(y).split('.')[1]):
		y = f"{y}{'0'*(i-len(str(y).split('.')[1]))}"
	return f"{y}({val})"

def f(x, a, b,c):
	return c+a/(x+b)

class fit:
	def __init__(self, xdata, ydata, yerr):
		self.xdata = xdata
		self.ydata = ydata
		self.yerr = yerr
	def fiting(self, func, args=dict()):
		self.func = func
		self.opt, self.cov = curve_fit(func, self.xdata, self.ydata, **args, sigma = self.yerr)
		r = self.ydata-func(self.xdata, *self.opt)
		chisq = ((r/self.yerr)**2).sum()
		dof = self.xdata.size-self.opt.size
		self.chisq_by_dof = np.round(chisq/dof,2)
		self.error = np.sqrt(self.cov.diagonal())