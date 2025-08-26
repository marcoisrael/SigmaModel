#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit, fix, Algs, obs
import os, argparse
from incertidumbres import measure

parser = argparse.ArgumentParser(prog="plot_autocorrelation")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
parser.add_argument("-o", "--observable", default="energy")
args = parser.parse_args()
name = args.observable
if args.algorithm == "all":
    algs = [
        "lexic_metropolis",
        "random_metropolis",
        "lexic_glauber",
        "random_glauber",
        "multi_cluster",
    ]
elif args.algorithm == "local":
    algs = [
        "lexic_metropolis",
        "random_metropolis",
        "lexic_glauber",
        "random_glauber",
    ]
else:
    algs = args.algorithm.split(",")

def f(x, a, b):
    return a*x**-b

for alg in algs:
    L = 64
    fig, ax = plt.subplots()

    data = np.loadtxt(
        f"output/autocorrelation/{name}_{alg}.csv", skiprows=1, delimiter=","
    )
    nstart, nend = 4,-1
    data = data.transpose()
    x = np.linspace(data[0][0], data[0][-1], 200)
    
    y , yerr = 0.5*(data[1,:]+data[3,:]), 0.5*(data[2,:]+data[4,:]) 
    
    xfit2 = fit(data[0,nstart:nend], data[1,nstart:nend], data[2,nstart:nend])
    xfit2.fiting(f)
    
    xfit1 = fit(data[0,nstart:nend], data[3,nstart:nend], data[4,nstart:nend])
    xfit1.fiting(f)
    
    # xfit = fit(data[0,:n], y[n:n], yerr[n:n])
    # xfit.fiting(f)

    # text = (r"$\tau \propto T^{-\nu z}$"+"\n"+ r"$\nu z = $"+f"{fix(xfit.opt[1], xfit.error[1])}" )
    #
    # ax.text(
    #     0.92,
    #     0.70,
    #     text,
    #     fontsize=16,
    #     ha="right",
    #     va="top",
    #     transform=ax.transAxes,
    # )
    
    ax.plot(
        x,
        f(x, *xfit1.opt),
        linewidth=1.8,
        color="tab:blue",
        linestyle=(0, (3, 3)),
    )
    
    
    ax.plot(
        x,
        f(x, *xfit2.opt),
        linewidth=1.8,
        color="tab:red",
        linestyle=(0, (3, 3)),
    )
    ax.errorbar(
        data[0],
        data[1],
        data[2],
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="tab:red",
    )   
    ax.errorbar(
        data[0],
        data[3],
        data[4],
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="tab:blue",
    )
       
    ax.errorbar(
        [],
        [],
        [],
        linestyle=(0, (2, 3)),
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="tab:red",
        label=r"$\tau_\mathrm{int}$, $\nu z=$"+fix(xfit2.opt[1], xfit2.error[1]),
    )

    ax.errorbar(
        [],
        [],
        [],
        linestyle=(0, (3, 3)),
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="tab:blue",
        label=r"$\tau_\mathrm{exp}$, $\nu z=$"+ fix(xfit1.opt[1], xfit1.error[1]),
    )

    # m1 = measure(xfit1.opt[1],xfit1.error[1])
    # m2 = measure(xfit2.opt[1],xfit2.error[1])
    # m = (m1+m2)/measure(2,0)
    
    #print(alg, fix(xfit1.opt[1],xfit1.error[1]))
    
    ax.set_xlabel(r"$T$", fontsize=18)
    ax.set_ylabel(r"$\tau$", fontsize=18)

    ax.legend(fontsize=12)
    ax.set_yscale("log")
    ax.set_xscale("log")
    title = Algs[alg]
    i = obs[name]["sym"]
    #plt.show()
    os.makedirs(f"output/plot/{name}/L{L}/{alg}", exist_ok=True)
    fig.savefig(
        f"output/plot/{name}/autocorrelation_{alg}_L{L}_{i}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
