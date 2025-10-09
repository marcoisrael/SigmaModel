#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from plotClass import fit, fix, correlation, obs
import argparse
parser = argparse.ArgumentParser(prog="autocorrelation")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
parser.add_argument("-o", "--observable", default="energy")
args = parser.parse_args()
name = args.observable
alg = args.algorithm
LENGTH = 64
T = np.array([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])

if args.algorithm == "all":
    algs = [
        "lexic_metropolis",
        "lexic_glauber",
        "random_metropolis",
        "random_glauber",
        "multi_cluster"
    ]
if args.algorithm == "local":
    algs = [
        "lexic_metropolis",
        "lexic_glauber",
        "random_metropolis",
        "random_glauber",
            ]
else:
    algs = args.algorithm.split(",")

for alg in algs:
    psi = []
    psiErr = []
    cor = []
    corErr = []
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

        path = f"output/record/L{LENGTH}/{alg}/{temp}.csv"
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        val = 0
        c0 = correlation(data[:, obs[name]["index"]],0)[1]
        ct = np.zeros(3)
        error = 0
        for t in range(1,data[:,0].size):
            ct = correlation(data[:, obs[name]["index"]],t)/c0
            if ct[1]>=0:
                val = val+ct[1]
                error = error+ct[2]
            else:
                break
        cor.append(val)
        corErr.append(error)
        
    psi = np.array(psi)
    psiErr = np.array(psiErr)
    cor = np.array(cor)
    corErr = np.array(corErr)
    
    ax.errorbar(
        cor,
        psi,
        xerr=corErr,
        yerr=psiErr,
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="tab:blue",
    )

     
    def f(x, a, b):
        return a*x**b
    
    xfit = fit(cor, psi, psiErr)
    xfit.fiting(f)
    
    x = np.linspace(cor[0],cor[-1])
    ax.plot(x,f(x,*xfit.opt), ls=(0,(3,3)))
    ax.errorbar(
            [],[],[],
            fmt="o",
            capsize=3,
            elinewidth=1,
            markersize=5,
            color="tab:blue",
            ls=(0,(3,3)),
            label=r"$\xi$, $z=$"+fix(xfit.opt[1],xfit.error[1]),
            )
    text = r"$\xi\propto \tau^{z}$"+"\n"+r"$z$="+fix(xfit.opt[0], xfit.error[0])
    text = r"$z=$"+fix(xfit.opt[1],xfit.error[1])
    ax.text(0.24,0.96,text,fontsize=12,ha="right",va="top",transform=ax.transAxes,bbox=dict(facecolor='none', edgecolor='black'))
    print(alg, fix(xfit.opt[1], xfit.error[1]))
    
    ax.set_xlabel(r"$\tau$", fontsize=18)
    ax.set_ylabel(r"$\xi$", fontsize=18)
    # ax.legend(fontsize=12)
    ax.set_yscale("log")
    ax.set_xscale("log")

    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[2.0],numticks=8))
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[2.0],numticks=6))

    # Ticks menores (ej. 2 y 5 en cada década)
    ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[1,2,3,4,6,8,9,10,12,14,20], numticks=8))
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[2,4,6,8,10], numticks=6))

    # --- FORMATOS ---
    formatter = ticker.StrMethodFormatter("{x:.0f}")
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)

    fig.savefig(f"output/plot/scaling/{alg}_{name}.pdf",format="pdf",bbox_inches="tight")
