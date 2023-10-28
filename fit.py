#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
folder = "output/cooling/plot"
algs = ['lexic_metropolis','random_metropolis','lexic_glauber',
		 'random_glauber','single_cluster']
def update(alg):
	if alg=='single_cluster':
		return "#Update"
	else:
		return "#Sweep"
r = [10,20,30,40]
for alg in algs:
    x, y, yerr = [], [], []
    for i in r:
        data = np.loadtxt(f"output/cooling/data0/{alg} {i}.tsv", skiprows=1).transpose()
        x.append(i)
        y.append(data[2][-1])
        yerr.append(data[3][-1])
    x, y, yerr = np.array(x), np.array(y), np.array(yerr)
    cof = np.polyfit(np.log(x), np.log(y), deg=1, cov=True)
    m, b =cof[0]
    m_err, b_err = np.sqrt(cof[1][0][0]/5), np.sqrt(cof[1][1][1]/5)
    t = np.log(np.linspace(10,40))
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(t, m*t+b, linewidth=0.8)
    ax.errorbar(np.log(x), np.log(y), yerr=b_err,marker='.', ls='', alpha=0.5)
    ax.set_xlabel(update(alg),fontsize=14)
    ax.set_ylabel(r'$\left<Q^2\right>_f$',fontsize=14)
    # fig.savefig(f'{folder}/fit_{alg}.png')
    print(m,m_err)