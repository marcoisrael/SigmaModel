#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import *
import os,argparse
parser = argparse.ArgumentParser(prog="plot_length")
parser.add_argument('-alg','--algorithm', default="lexic_metropolis")
args = parser.parse_args()
make_plots=False
os.makedirs("output/plot/length/",exist_ok=True)
if args.algorithm=="all":
	algs = ["lexic_metropolis","lexic_glauber","random_metropolis","random_glauber"]
else:
	algs = args.algorithm.split(",")

for alg in algs:
	print(alg)
	fig, ax = plt.subplots()
	T = np.array([0.6,0.625,0.65,0.7,0.8])
	params = {
			32:{"color":"red","line":(0,(3,3))},
			64:{"color":"blue","line":(0,(3,3))},
			128:{"color":"purple","line":(0,(3,3))}
			}
	for LENGTH in [32,64,128]:
		psi = []
		psiErr = []
		for temp in T:
			path = f"output/correlation_length/L{LENGTH}/{alg}/{temp}.csv"
			#print(path)
			data = np.loadtxt(path, delimiter=",", skiprows=1)
			f = lambda x, a, b: a*np.exp(-x/b)+a*np.exp((x-LENGTH)/b)
			xfit = fit(data[:,0],data[:,1],data[:,2])

			xfit.fiting(f, args={"bounds":((0,np.inf))})
			psi.append(xfit.opt[1])
			psiErr.append(xfit.error[1])
			if make_plots:
				fig, ax = plt.subplots()
				x = np.linspace(0,LENGTH,100)
				ax.errorbar(data[:,0],data[:,1],yerr=data[:,2], fmt='o', capsize=1, elinewidth=1, markersize=1)
				ax.plot(x, f(x,*xfit.opt),linewidth=0.8)
				fig.savefig(f"output/plot/correlation_length/lexic_metropolis_L{LENGTH}_{temp}.png")
				print(temp, xfit.opt[1])
				#plt.show()
				plt.close()
		
		psi = np.array(psi)
		ax.errorbar(T, psi, psiErr, fmt='o',capsize=1,elinewidth=1,markersize=1,color=params[LENGTH]["color"],)#label=f"Datos $(L={LENGTH})$")
		f = lambda x, a, b: a*x**-b
		#f = lambda x, a, b,c:c/(1+np.exp((x-a)/b))
		xfit = fit(T, psi, psiErr)
		#xfit.fiting(f,{"bounds":((0,0),(np.inf,np.inf))})
		xfit.fiting(f)
		print(LENGTH,fix(xfit.opt[1],xfit.error[1]))
		
		x = np.linspace(T[0],T[-1],200)
		ax.plot(x, f(x,*xfit.opt), linewidth=0.8,color=params[LENGTH]["color"],linestyle=params[LENGTH]["line"],label=f"$L={LENGTH}$")
		ax.set_xlabel(r"$T$", fontsize=18)
		ax.set_ylabel(r"$\xi$", fontsize=18)
		ax.legend()
		#ax.set_yscale("log")

		data = np.array([T,psi,psiErr]).transpose()
		#np.savetxt(f"output/length/LM_L{LENGTH}.csv", data, 
		#	delimiter=",",header="T,xi,xi_error",comments="", fmt="%16f")
		#ax.set_title(f"Correlation length, lexicographical Metropolis, L={LENGTH}", fontsize=12)
	fig.savefig(f"output/plot/length/length_{alg}.pdf", format="pdf",bbox_inches="tight")
