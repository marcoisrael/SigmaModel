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
        "lexic_glauber",
        "random_metropolis",
        "random_glauber",
        #"multi_cluster",
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
    data = data.transpose()
    x = np.linspace(data[0][0], data[0][-1], 200)
    xfit = fit(data[0,:4], data[1,:4], data[2,:4])
    xfit.fiting(f)
    
    xfit2 = fit(data[0,:4], data[3,:4], data[4,:4])
    xfit2.fiting(f)

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
        f(x, *xfit.opt),
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
        linestyle=(0, (3, 3)),
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="tab:red",
        label=r"$\tau_\mathrm{int}$, $\nu z=$"+fix(xfit.opt[1], xfit.error[1]),
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
        label=r"$\tau_\mathrm{exp}$, $\nu z=$"+ fix(xfit2.opt[1], xfit2.error[1]),
    )
    # print(alg,"tau_int=", fix(xfit.opt[1], xfit.error[1]),"tau_exp=",fix(xfit2.opt[1], xfit2.error[1]))
    m1 = measure(xfit.opt[1],xfit.error[1])
    m2 = measure(xfit2.opt[1],xfit2.error[1])
    m = (m1+m2)/measure(2,0)
    print(alg, fix(m.value,m.error))
    ax.set_xlabel(r"$\log(T)$", fontsize=18)
    ax.set_ylabel(r"$\log(\tau)$", fontsize=18)

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
