#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit, fix
import argparse
from matplotlib import ticker

parser = argparse.ArgumentParser(prog="autocorrelation")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
parser.add_argument("-o", "--observable", default="energy")
args = parser.parse_args()
os.makedirs("output/plot/cooling", exist_ok=True)
if args.algorithm == "all":
    algs = [
        "lexic_metropolis",
        "lexic_glauber",
        "random_metropolis",
        "random_glauber",
        "multi_cluster",
    ]
else:
    algs = args.algorithm.split(",")
obs = args.observable


def f1(x, a, b):
    return a*x**(-b)


def f2(x, a, b):
    return a*x**(-b)


def f3(x, a, b):
    return a*x**(b)


params = {
        "charge": {"index": 2, "ylabel": r"$\chi_t$", "ylabel2":
                   r"$\chi_{t_f}$", "func": f1},
    "energy": {"index": 4, "ylabel": r"$\langle h \rangle$", "ylabel2":
               r"$\langle h \rangle_f$", "func": f1},
    "magnet": {"index": 6, "ylabel": r"$\langle M \rangle$", "ylabel2":
               r"$\langle M \rangle_f$", "func": f3},
}
colors = {8: "red", 10: "blue", 16: "green"}
lines = {8: (0, (3, 3)), 10: (0, (5, 1)), 16: (0, (5, 5))}
markers = {8: ".", 10: "+", 16: "2"}
for alg in algs:
    X = []
    ob = params[obs]["index"]
    path = "output/cooling/L64/4-0"
    indexes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    fig1, ax1 = plt.subplots()
    fig3, ax3 = plt.subplots()
    for i in indexes:
        data = np.loadtxt(
            f"{path}/{alg} {i}.csv",
            delimiter=",",
            skiprows=1
        )
        data = data.transpose()
        data[4] = data[4]+2
        X.append([i, data[ob][-1], data[ob + 1][-1]])
        if i in [8, 10, 16]:
            ax1.errorbar(
                data[0],
                data[ob],
                data[ob + 1],
                color=colors[i],
                ls="",
                marker=markers[i],
                markersize=8,
                label=f"$\\tau_Q={i}$",
            )
            ax3.errorbar(
                data[1],
                data[ob],
                data[ob + 1],
                color=colors[i],
                ls="",
                marker=markers[i],
                markersize=8,
                label=f"$\\tau_Q={i}$",
            )

            # f = lambda x, a, b,c:c/(1+np.exp((x-a)/b))
            # xfit = fit(data[0],data[ob],data[ob+1])
            # xfit.fiting(f)
            # x = np.linspace(0,i,200)
            # ax1.plot(x, f(x,*xfit.opt), color=colors[i], linewidth=0.8,
            # linestyle=lines[i],label=f"$\\tau_{{\\mathrm{{cool}}}}={i}$")
    
    ax1.legend()
    ax1.set_xlabel(r"$t$ [barridos]", fontsize=18)
    ax1.set_ylabel(params[obs]["ylabel"], fontsize=18)
    fig1.savefig(
        f"output/plot/cooling/{obs}_{alg}.pdf", format="pdf", bbox_inches="tight"
    )
    ax3.legend()
    ax3.set_xlabel(r"$T$", fontsize=18)
    ax3.set_ylabel(params[obs]["ylabel"], fontsize=18)
    fig3.savefig(
        f"output/plot/cooling/{obs}_temp_{alg}.pdf", format="pdf", bbox_inches="tight"
    )

    X = np.array(X).transpose()
    fig2, ax2 = plt.subplots()
    ax2.errorbar(X[0], X[1], X[2], ls="", color="tab:blue",
                 marker="o", markersize=5)
    x = np.linspace(8, 18)

    f = params[obs]["func"]
    p0=0
    xfit = fit(X[0][p0:], X[1][p0:], X[2][p0:])
    param_bounds = ((0, 0), (np.inf, np.inf))
    xfit.fiting(f, args={"bounds": param_bounds})
    print(alg, fix(xfit.opt[1], xfit.error[1]))
    # text = r"$\zeta=$"+fix(xfit.opt[1], xfit.error[1])
    # ax2.text(
    #         0.05, 0.75,
    #         text,
    #         fontsize=16,
    #         ha="left",
    #         va="top",
    #         transform=ax2.transAxes
    #         )
    ax2.plot(
            x, f(x, *xfit.opt), 
            linewidth=1.8,
            color="tab:blue", 
            linestyle=(0, (3, 3)),
                        )
    ax2.errorbar(
            [],[],[],
            linewidth=1.8,
            color="tab:blue",
            linestyle=(0,(3,3)),
            label=params[obs]["ylabel2"],
            )
    text = r"$\zeta=$"+fix(xfit.opt[1],xfit.error[1])
    ax2.text(0.24,0.94,text,fontsize=12,ha="right",va="top",transform=ax2.transAxes,
            bbox=dict(facecolor='none', edgecolor='black'))
    # 0.24, 0.94,     0.95, 0.94
    ax2.set_ylabel(params[obs]["ylabel2"], fontsize=20)
    ax2.set_xlabel(r"$\tau_\mathrm{cool}$", fontsize=20)
    ax2.set_yscale("log")
    ax2.set_xscale("log")

    ax2.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[1.0], numticks=10))
    ax2.yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[1.0], numticks=10))

    # Ticks menores (ej. 2 y 5 en cada década)
    ax2.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[2.0, 5.0], numticks=10))
    ax2.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[2.0, 5.0], numticks=10))

    # --- FORMATOS ---
    formatter = ticker.StrMethodFormatter("{x:.0f}")
    ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter("{x:.3f}")
    ax2.xaxis.set_minor_formatter(formatter)
    ax2.yaxis.set_minor_formatter("{x:.3f}")

    # for axis in [ax2.xaxis, ax2.yaxis]:
    #     formatter = ScalarFormatter()
    #     formatter.set_scientific(False)
    #     axis.set_major_formatter(formatter)
    #     axis.set_minor_formatter(formatter)
    ax1.legend(fontsize=12)
    # ax2.legend(fontsize=12) 
    #ax2.set_xticks([8,9,10,11,13,15,18])
    fig2.savefig(
        f"output/plot/cooling/scaling_law_{obs}_{alg}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
