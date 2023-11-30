#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import os

text_kwargs = dict(ha='center', va='center', fontsize=12)
def fit(x,y):
    cof = np.polyfit(x, y, deg=1, cov=True)
    error = np.sqrt(cof[1][0][0]/5), np.sqrt(cof[1][1][1]/5)
    return cof[0],error

name = "4p0-0p0/"
folder = f"output/cooling/v64x64/{name}"
dest = f"output/plot/v64x64/{name}"
algorithm = ['lexic_glauber','lexic_metropolis','random_glauber','random_metropolis']
for alg in algorithm:
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,dpi=100,figsize=(16,9))
    tauQf, chif,chifError = [],[],[]
    for n in [3,6,12,15]:
        data = np.loadtxt(f"{folder}{alg} {n}.csv", delimiter=',',skiprows=1).transpose()
        tauQ,T,chi,chiError,ar,arError = data
        tauQf.append(tauQ[-1])
        chif.append(chi[-1])
        chifError.append(chiError[-1])
        ax1.errorbar(tauQ,chi,yerr=chiError,ls='',marker='.',alpha=0.6,label=r'$\tau_Q=$'+f'{n}')
        ax1.set_xlabel('#sweep',fontsize=12)
        ax1.set_ylabel(r'$\chi$',fontsize=12)
        ax2.errorbar(T,chi,yerr=chiError,ls='',marker='.',alpha=0.6)
        ax2.set_xlabel(r'$T$',fontsize=12)
        ax2.set_ylabel(r'$\chi$',fontsize=12)
        ax4.errorbar(T,ar,yerr=arError,ls='',marker='.',alpha=0.6)
        ax4.set_xlabel(r'$T$',fontsize=12)
        ax4.set_ylabel('Acceptance Rate',fontsize=12)
    tauQf,chif,chifError = np.array(tauQf),np.array(chif),np.array(chifError)
    x, y = np.log(tauQf),np.log(chif)
    cof, err = fit(x,y)
    t = np.log(np.linspace(2,16))
    ax3.plot(t, np.polyval(cof,t),linewidth=0.8)
    ax3.errorbar(x,y,yerr=chifError/chif,ls='',marker='.',alpha=0.6)
    ax3.set_xlabel(r'$\log\left(\tau_{Q}\right)$',fontsize=12)
    ax3.set_ylabel(r'$\log\left(\chi_f\right)$',fontsize=12)
    text = f'$y = {cof[0].round(2)}x+{cof[1].round(2)}$'
    ax3.text(0.7, 0.7, text,transform=ax3.transAxes, **text_kwargs) 
    title = alg.replace('_',' ')+', '+r'$T\in(4,0)$'+', '+r'$V=64\times 64$'
    title = title.replace('lexic','lexicographical')
    fig.suptitle(title,fontsize=14)
    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines, labels)
    #fig.tight_layout()
    if not os.path.isdir(f'output/plot/{name}/'):
        os.makedirs(f'output/plot/{name}/')
    fig.savefig(f'output/plot/{name}/{alg}.png')   

alg ='multi_cluster'
fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,dpi=100,figsize=(16,9))
tauQf, chif,chifError = [],[],[]
for n in [3,6,12,15]:
    data = np.loadtxt(f"{folder}{alg} {n}.csv", delimiter=',',skiprows=1).transpose()
    tauQ,T,chi,chiError,ar,arError = data
    tauQf.append(tauQ[-1])
    chif.append(chi[-1])
    chifError.append(chiError[-1])
    ax1.errorbar(tauQ,chi,yerr=chiError,ls='',marker='.',alpha=0.6,label=r'$\tau_Q=$'+f'{n}')
    ax1.set_xlabel('#Update',fontsize=12)
    ax1.set_ylabel(r'$\chi$',fontsize=12)
    ax2.errorbar(T,chi,yerr=chiError,ls='',marker='.',alpha=0.6)
    ax2.set_xlabel(r'$T$',fontsize=12)
    ax2.set_ylabel(r'$\chi$',fontsize=12)
    ax4.errorbar(T,ar,yerr=arError,ls='',marker='.',alpha=0.6)
    ax4.set_xlabel(r'$T$',fontsize=12)
    ax4.set_ylabel('Cluster SIze',fontsize=12)
tauQf,chif,chifError = np.array(tauQf),np.array(chif),np.array(chifError)
x, y = np.log(tauQf),np.log(chif)
cof, err = fit(x,y)
t = np.log(np.linspace(2,16))
ax3.plot(t, np.polyval(cof,t),linewidth=0.8)
ax3.errorbar(x,y,yerr=chifError/chif,ls='',marker='.',alpha=0.6)
ax3.set_xlabel(r'$\log\left(\tau_{Q}\right)$',fontsize=12)
ax3.set_ylabel(r'$\log\left(\chi_f\right)$',fontsize=12)
text = f'$y = {cof[0].round(2)}x+{cof[1].round(2)}$'
ax3.text(0.7, 0.7, text,transform=ax3.transAxes, **text_kwargs)
title = alg.replace('_',' ')+', '+r'$T\in(4,0)$'+', '+r'$V=64\times 64$'
title = title.replace('lexic','lexicographical')
fig.suptitle(title,fontsize=14)
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels)
#fig.tight_layout()
if not os.path.isdir(f'output/plot/{name}/'):
    os.makedirs(f'output/plot/{name}/')
fig.savefig(f'output/plot/{name}/{alg}.png') 