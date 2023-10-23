#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import os
folder = "output/cooling/plot"
algs = ['lexic_metropolis','random_metropolis','lexic_glauber', 'random_glauber','single_cluster']
words = {'lexic':'Lexicographic'}
def update(alg):
	if alg=='single_cluster':
		return "#update"
	else:
		return "#sweep"
if not os.path.isdir(folder):
	os.makedirs(folder)
for alg in algs:
	fig, ax = plt.subplots()
	ax.set_title(f'{alg}')
	ax.set_xlabel(update(alg))
	ax.set_ylabel(r'$\left<Q^2\right>$')
	for i in [10,20,30,40]:
		data = np.loadtxt(f"output/cooling/data0/{alg} {i}.tsv", skiprows=1)
		step, temp,sucept, suceptError ,absSucept, absSucepError= data.transpose()
		
		ax.errorbar(step, sucept, yerr=suceptError, marker='.', label=r'$\tau_Q=$'+str(i))
	ax.legend()
	fig.savefig(f'{folder}/{alg}.png')