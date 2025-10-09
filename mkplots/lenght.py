#!/bin/bash/python3
import numpy as np
from plotClass import *
import matplotlib.pyplot as plt
algs = [
        "lexic_metropolis",
        "random_metropolis",
        "lexic_glauber",
        "random_glauber",
        "multi_cluster",
        ]
names = [
        "Metropolis\nLexic",
        "Metropolis\nAleatorio",
        "Glauber\nLexic",
        "Glauber\nAleatorio",
        "Multi\ncluster",
        ]
T = np.array([0.3,0.4,0.5])
for LENGTH in [32,64,128]:
    val=[]
    valErr=[]
    for alg in algs:
        psi = []
        psiErr = []
        for temp in T:
            path = f"output/correlation_length/L{LENGTH}/{alg}/{temp}.csv"
            # print(path)
            data = np.loadtxt(path, delimiter=",", skiprows=1)

            def f(x, a, b):
                return a * np.exp(-x / b) + a * np.exp((x - LENGTH) / b)

            xfit = fit(data[:, 0], data[:, 1], data[:, 2])
            xfit.fiting(f, args={"bounds": ((0, np.inf))})
            psi.append(xfit.opt[1])
            psiErr.append(xfit.error[1])
        psi = np.array(psi)
        
        def f(x, a, b):
            return a*x**-b
            
        xfit = fit(T, psi, psiErr)
        xfit.fiting(f)
        val.append(xfit.opt[1])
        valErr.append(xfit.error[1])
    x=np.array([1,2,3,4,5])
    fig, ax = plt.subplots()
    ax.errorbar(x,val,valErr,ls="",marker=".",color="b",capsize=3,elinewidth=1)
    y = np.array(val).mean()
    ax.plot(x,y*np.ones_like(x),color="black")
    ax.set_ylabel(r"$\nu$",fontsize=20)
    ax.set_xticks(x,names,rotation=0)
    fig.savefig(
        f"output/plot/length/size_{LENGTH}.pdf",
        format="pdf",
        bbox_inches="tight"
        )
