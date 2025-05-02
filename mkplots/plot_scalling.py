#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit, fix
import os
import argparse
parser = argparse.ArgumentParser(prog="autocorrelation")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
parser.add_argument("-o", "--observable", default="energy")
args = parser.parse_args()
name = args.observable
alg = args.algorithm
LENGTH = 64
T = np.array([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2])

if args.algorithm == "all":
    algs = [
        "lexic_metropolis",
        "lexic_glauber",
        "random_metropolis",
        "random_glauber",
        "multi_cluster"
    ]
else:
    algs = args.algorithm.split(",")

for alg in algs:
    psi = []
    psiErr = []
    fig, ax = plt.subplots()

    #os.system(f"/usr/bin/python3 mkplots/autocorrelation_time.py -alg {alg} -o {name}")
    for temp in T:
        path = f"output/correlation_length/L{LENGTH}/{alg}/{temp}.csv"
        data = np.loadtxt(path, delimiter=",", skiprows=1)

        def f(x, a, b):
            return a * np.exp(-x / b) + a * np.exp((x - LENGTH) / b)

        xfit = fit(data[:, 0], data[:, 1], data[:, 2])

        xfit.fiting(f, args={"bounds": ((0, np.inf))})
        psi.append(xfit.opt[1])
        psiErr.append(xfit.error[1])
        
    psi = np.array(psi[4:-1])
    psiErr = np.array(psiErr[4:-1])

    
    data = np.loadtxt(
        f"output/autocorrelation/{name}_{alg}.csv",
        skiprows=1,
        delimiter=","
    )
    print(data.shape, psi.size)
    data = data.transpose()

    ax.errorbar(
        data[1],
        psi,
        xerr=data[2],
        yerr=psiErr,
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="red",
    )

     
    def f(x, a, b):
        return a*x**-b
    
    xfit = fit(data[1], psi, psiErr)
    xfit.fiting(f)
    
    x = np.linspace(data[1][0],data[1][-1])
    ax.plot(x,f(x,*xfit.opt), ls="dotted")
    
    text = r"$\xi\propto T^{-z}$"+"\n"+r"$z$="+fix(xfit.opt[0], xfit.error[0])
    
    ax.text(0.96,0.20,text,fontsize=16,ha="right",va="top",transform=ax.transAxes)
    print(fix(xfit.opt[0], xfit.error[0]))
    
    ax.set_xlabel(r"$\log(\tau)$", fontsize=18)
    ax.set_ylabel(r"$\log(\xi)$", fontsize=18)
    # ax.legend()
    ax.set_yscale("log")
    ax.set_xscale("log")

    fig.savefig(
        f"output/plot/scaling/{alg}_{name}.pdf",
        format="pdf",
        bbox_inches="tight"
    )
