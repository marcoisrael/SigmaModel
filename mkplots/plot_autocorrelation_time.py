#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit, fix, Algs, obs
import os
import argparse

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
        "multi_cluster"
    ]
else:
    algs = args.algorithm.split(",")
for alg in algs:
    L = 64

    def f(x, a, b):
        return a*x**-b

    data = np.loadtxt(
        f"output/autocorrelation/{name}_{alg}.csv",
        skiprows=1,
        delimiter=","
    )
    data = data.transpose()
    x = np.linspace(data[0][0], data[0][-1], 200)
    xfit = fit(data[0][1:], data[1][1:], data[2][1:])
    xfit.fiting(f)
    fig, ax = plt.subplots()
    text = fix(xfit.opt[0], xfit.error[0])+r"$\exp(-$"+fix(xfit.opt[1], xfit.error[1]) + \
        r"$T)$"+"\n" + \
        r"$\frac{\chi^2}{\mathrm{dof}}=$"+str(xfit.chisq_by_dof)

    ax.text(
        0.99,
        0.99,
        text,
        fontsize=16,
        ha="right",
        va="top",
        transform=ax.transAxes,
    )
    ax.errorbar(
        data[0],
        data[1],
        data[2],
        fmt="o",
        capsize=3,
        elinewidth=1,
        markersize=5,
        color="red",
    )
    ax.plot(
        x,
        f(x, *xfit.opt),
        linewidth=1.8,
        color="blue",
        label=r"$\tau_{exp}$",
        linestyle=(0, (3, 3)),
    )
    print(alg, fix(xfit.opt[1], xfit.error[1]))
    ax.set_xlabel(r"$\log(T)$", fontsize=18)
    ax.set_ylabel(r"$\log(\tau)$", fontsize=18)
    # ax.legend()
    ax.set_yscale("log")
    ax.set_xscale("log")
    title = Algs[alg]
    i = obs[name]["sym"]
    os.makedirs(f"output/plot/{name}/L{L}/{alg}", exist_ok=True)
    fig.savefig(
        f"output/plot/{name}/autocorrelation_{alg}_L{L}_{i}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
