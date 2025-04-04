#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit, fix
import os
import argparse

parser = argparse.ArgumentParser(prog="plot_length")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
args = parser.parse_args()
make_plots = False
os.makedirs("output/plot/length/", exist_ok=True)
if args.algorithm == "all":
    algs = ["lexic_metropolis", "lexic_glauber",
            "random_metropolis", "random_glauber", "multi_cluster"]
else:
    algs = args.algorithm.split(",")

for alg in algs:
    print(alg)
    fig, ax = plt.subplots()
    T = np.array([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    params = {
        32: {"color": "red", "line": "dotted", "marker": "."},
        64: {"color": "blue", "line": "dashed", "marker": "+"},
        128: {"color": "green", "line": "dashdot", "marker": "2"},
    }
    # ~ i = 0
    for LENGTH in [32, 64, 128]:
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
            if make_plots:
                fig, ax = plt.subplots()
                x = np.linspace(0, LENGTH, 100)
                ax.errorbar(
                    data[:, 0],
                    data[:, 1],
                    yerr=data[:, 2],
                    fmt="o",
                    capsize=3,
                    elinewidth=1,
                    markersize=5,
                    color="red",
                )
                ax.plot(x, f(x, *xfit.opt), linewidth=1.8, ls=(0, (3, 3)),color="blue")
                ax.set_ylabel(r"$\langle \vec{\sigma_i}\cdot\vec{\sigma_j}\rangle$", fontsize=18)
                ax.set_xlabel(r"$i$", fontsize=18)
                fig.savefig(
                    f"output/plot/correlation_length/lexic_metropolis_L{LENGTH}_{temp}.png"
                )
                print(temp, xfit.opt[1])
                plt.close()

        psi = np.array(psi)
        ax.errorbar(
            T,
            psi,
            psiErr,
            fmt=params[LENGTH]["marker"],
            capsize=1,
            elinewidth=1,
            markersize=8,
            color=params[LENGTH]["color"],
        )

        def f(x, a, b):
            return a*x**-b

        xfit = fit(T[:3], psi[:3], psiErr[:3])
        xfit.fiting(f)
        print(LENGTH, fix(xfit.opt[1], xfit.error[1]))

        x = np.linspace(T[0], T[-1], 200)   
        ax.plot(
            x,
            f(x, *xfit.opt),
            linewidth=1,
            color=params[LENGTH]["color"],
            linestyle=params[LENGTH]["line"],
            label=f"$L={LENGTH}$",
        )
        ax.set_xlabel(r"$\log(T)$", fontsize=18)
        ax.set_ylabel(r"$\log(\xi)$", fontsize=18)
        ax.legend()
        ax.set_yscale("log")
        ax.set_xscale("log")
    fig.savefig(
        f"output/plot/length/length_{alg}.pdf",
        format="pdf",
        bbox_inches="tight"
    )
