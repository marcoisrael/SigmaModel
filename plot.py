#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import os
folder = "output/cooling/plot"
algs = ['lexic_metropolis','random_metropolis','lexic_glauber', 'random_glauber','single_cluster']
words = {'lexic':'lexicographical','random':'random','single':'single'}
def update(alg):
	if alg=='single_cluster':
		return "#Update"
	else:
		return "#Sweep"
if not os.path.isdir(folder):
	os.makedirs(folder)
for alg in algs:
	a, n = alg.split('_')
	fig, ax = plt.subplots()
	# ax.set_title(f'100 cluster termalization and 4 to 0 {words[a]} {n} cooling '+r'$V=64$',fontsize=10)
	ax.set_xlabel(update(alg),fontsize=14)
	ax.set_ylabel(r'$\left<Q^2\right>$',fontsize=14)
	for i in [10,20,30,40]:
		data = np.loadtxt(f"output/cooling/data0/{alg} {i}.tsv", skiprows=1)
		step, temp,sucept, suceptError ,absSucept, absSucepError= data.transpose()
		
		ax.errorbar(step, sucept, yerr=suceptError, marker='.',ls='', label=r'$\tau_Q=$'+str(i))
	ax.legend()
	fig.savefig(f'{folder}/{alg}.png')