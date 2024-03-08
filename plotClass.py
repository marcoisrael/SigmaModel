#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.optimize import curve_fit

label1 = [[r"$\chi_t$", "Sweep"],[r"$\chi_t$", r"$T$"],[r"$\chi_t\left(\tau_Q\right)$", r"$\tau_Q$"],["Acceptance rate", "T"]]
label2 = [[r"$\chi_t$", "Update"],[r"$\chi_t$", r"$T$"],[r"$\chi_t\left(\tau_Q\right)$", r"$\tau_Q$"],["Cluster size", "T"]]
select = {"Metropolis":label1,"Glauber":label1,"Cluster":label2}

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
def f(x, a, b,c):
	return c+a/(x+b)
class loadData:
	def __init__(self,algVar, alg, startTemp, endTemp, path, dest,tauq):
		self.alg = alg
		self.algVar = algVar
		self.path = path
		self.dest = dest
		self.name = f"{algVar.lower()}_{alg.lower()}"
		self.startTemp = startTemp
		self.endTemp = endTemp
		self.tauq = tauq
		self.data = []
		self.chitf = np.array([])
		self.chitfErr = np.array([])

		for i in tauq:
			self.data.append(pd.read_csv(f"{self.path}/{self.name} {i}.csv"))
	
	def fit(self):
		for d in self.data:
			self.chitf = np.append(self.chitf, d.iloc[-1]["chi_t"],)
			self.chitfErr = np.append(self.chitfErr, d.iloc[-1]["Error chi_t"],)

		x, y = self.tauq, self.chitf
		# d = {"tau_Qf":x, "chi_tf":y}
		# df = pd.DataFrame(d)
		# df.to_csv(f"output/data_{self.alg}.csv")
		self.opt, self.cov = curve_fit(f, x, y)
		e = f(x,*self.opt)
		self.zeta = abs(self.opt[1])
		self.zetaErr = np.sqrt(np.sum((e-y)**2)/(x.size-self.opt.size))
		print(f"{self.algVar} {self.alg} done")
		
	def chi2(self):
		x, y = self.tauq, self.chitf
		yerr = self.chitfErr
		y0 = f(x,*self.opt)
		return np.sum(((y-y0)/yerr)**2)/(y.size-self.opt.size)
		
	def plot(self):
		fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,dpi=140,figsize=(16,9))
		for d, tq in zip(self.data,self.tauq):
			ax1.errorbar(d["tau_Q"],d["chi_t"],yerr=d["Error chi_t"],linewidth=0.6,marker='.',markersize=2, label=r"$\tau_Q$"+f" = {tq}")
			ax2.errorbar(d["T"],d["chi_t"],yerr=d["Error chi_t"],linewidth=0.6,marker='.',markersize=2)
			ax4.errorbar(d["T"],d["AR|CS"],yerr=d["Error AR|CS"],linewidth=0.6,marker='.',markersize=2)
		x = np.linspace(self.tauq[0],self.tauq[-1])
		ax3.plot(x,f(x,*self.opt),linewidth=0.6)
		ax3.fill_between(x, f(x,*self.opt)+self.zetaErr,f(x,*self.opt)-self.zetaErr, alpha=0.3)
		ax3.errorbar(self.tauq, self.chitf, yerr=self.chitfErr,ls="",marker=".",markersize=2)
		stats = "".join([r"$\chi_t(\tau_Q)=C\cdot\exp(-\alpha\cdot\tau_Q)+k$", "\n", r"$\alpha=$", f"{self.opt[1].round(4)}\n", r"$\chi^2\left/dog\right. =" f"$ {self.chi2().round(4)}"])
		bbox = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5)
		ax3.text(0.95, 0.7, stats, fontsize=14, bbox=bbox,transform=ax3.transAxes, horizontalalignment='right')
		lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
		lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
		fig.legend(lines, labels)
		title = f"{self.algVar} {self.alg}"+r", $V=64 \times 64$"+ f", $T \in ({self.startTemp},{self.endTemp})$"
		fig.suptitle(title,fontsize=16)
		for i, ax in zip([0,1,2,3],[ax1,ax2,ax3,ax4]):
			ax.set_ylabel(select[self.alg][i][0], fontsize=15)
			ax.set_xlabel(select[self.alg][i][1], fontsize=15)
		if not os.path.isdir(self.dest):
			os.makedirs(self.dest)
		print(self.opt)
		fig.savefig(f'{self.dest}/{self.name}.png')		
