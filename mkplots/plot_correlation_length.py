#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from plotClass import fit, fix
import os
import argparse

parser = argparse.ArgumentParser(prog="plot_length")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
args = parser.parse_args()
os.makedirs("output/plot/length/", exist_ok=True)
if args.algorithm == "all":
    algs = ["lexic_metropolis", "lexic_glauber",
            "random_metropolis", "random_glauber", "multi_cluster"]
else:
    algs = args.algorithm.split(",")

for alg in algs:
    print(alg)
    fig, ax = plt.subplots()
    T = np.array([0.3,0.4,0.5,0.6])
    params = {
        32: {"color": "red", "line": (0, (3, 3)), "marker": "."},
        64: {"color": "blue", "line": (0, (1, 1)), "marker": "+"},
        128: {"color": "green", "line": (0, (2, 3)), "marker": "2"},
    }
    # ~ i = 0
    for LENGTH in [32, 64, 128]:
        psi = []
        psiErr = []
        if LENGTH==128:
            T=np.array([0.3,0.4,0.5])
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
        ax.errorbar(
            T,
            psi,
            psiErr,
            fmt=params[LENGTH]["marker"],
            capsize=1,
            elinewidth=1,
            markersize=10,
            color=params[LENGTH]["color"],
        )
        def f(x, a, b):
            return a*x**-b

        xfit = fit(T, psi, psiErr)
        xfit.fiting(f)

        ax.errorbar(
            [],
            [],
            [],
            fmt=params[LENGTH]["marker"],
            capsize=1,
            elinewidth=1,
            markersize=10,
            color=params[LENGTH]["color"],
            linewidth=1.8,
            linestyle=params[LENGTH]["line"],
            label=f"$L=${LENGTH}, "+r"$\nu=$"+fix(xfit.opt[1],xfit.error[1]),
        )
        
        print(LENGTH, fix(xfit.opt[1], xfit.error[1]))

        x = np.linspace(T[0], T[-1], 200)   
        ax.plot(
            x,
            f(x, *xfit.opt),
            linewidth=1.8,
            color=params[LENGTH]["color"],
            linestyle=params[LENGTH]["line"],
        )

    ax.set_xlabel(r"$T$", fontsize=18)
    ax.set_ylabel(r"$\xi$", fontsize=18)
    ax.legend(fontsize=12)
    ax.set_yscale("log")
    ax.set_xscale("log")

    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[1.0], numticks=10))
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[1.0], numticks=10))

    # Ticks menores (ej. 2 y 5 en cada década)
    ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[0.3,0.4,0.5,0.6], numticks=10))
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[2.0, 5.0], numticks=10))

    # --- FORMATOS ---
    formatter = ticker.StrMethodFormatter("{x:.1f}")
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)

    fig.savefig(
        f"output/plot/length/length_{alg}.pdf",
        format="pdf",
        bbox_inches="tight"
    )
