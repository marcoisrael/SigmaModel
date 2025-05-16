#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit, correlation, obs, fix
import matplotlib.colors as colors
import os
import argparse

parser = argparse.ArgumentParser(prog="autocorrelation")
parser.add_argument("-alg", "--algorithm", default="lexic_metropolis")
parser.add_argument("-o", "--observable", default="energy")
args = parser.parse_args()
colors_list = list(colors._colors_full_map.values())
make_temp_plots = True
name = args.observable
alg = args.algorithm
L = 64
T = np.array([0.75,0.8,0.85,0.9])
if args.algorithm == "all":
    algs = [
        "lexic_metropolis",
        "random_metropolis",
        "lexic_glauber",
        "random_glauber",
        "multi_cluster",
    ]
else:
    algs = args.algorithm.split(",")
for alg in algs:
    print(alg)
    cor = []
    corErr = []
    Ti = []
    for temp in T:
        path = f"output/record/L{L}/{alg}/{temp}.csv"
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
        Ti.append(temp)
        print(fix(val,error))
        # X = []
        # for t in np.arange(0, 101):
        #     x = correlation(data[:, obs[name]["index"]], t)
        #     X.append(x)
        # p0=0
        # X = np.array(X)
        # t, q, qErr = X[:, 0], X[:, 1] / X[0, 1], X[:, 2] / X[0, 1]
        #
        # xfit = fit(t[p0:], q[p0:], qErr[p0:])
        #
        # def f(x, a,b):
        #     return a*np.exp(-x/b)
        #
        # xfit.fiting(f, args={"bounds": ((0, np.inf))})
        # print(temp, "  ",fix(val,error), "  ", fix(xfit.opt[1],xfit.error[1]))
        # cor.append(xfit.opt[1])
        # corErr.append(xfit.error[1])
        #   
        # x = np.linspace(t[0], t[-1], 500)
        # if make_temp_plots:
        #     fig, ax = plt.subplots(tight_layout=True)
        #     ax.plot(x, f(x, *xfit.opt), linewidth=1.2, color="black",
        #             label="Fitting")
        #     ax.errorbar(
        #         t,
        #         q,
        #         qErr,
        #         fmt="o",
        #         capsize=1,
        #         elinewidth=1,
        #         markersize=2,
        #         color="red",
        #         label="Data",
        #     )
        #     ax.set_xlabel(r"$t$", fontsize=20)
        #     ax.set_ylabel(r"$\tau$", fontsize=20)
        #     ax.legend()
        #    
        #     os.makedirs(f"output/plot/{name}/L{L}/{alg}", exist_ok=True)
        #     fig.tight_layout()
        #     fig.savefig(
        #         f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.pdf",
        #         format="pdf",
        #         bbox_inches="tight",
        #     )
        #     print(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.png")
        #     plt.close()
        #     del ax, fig

    cor = np.array(cor)
    corErr = np.array(corErr)
    data = np.array([Ti, cor, corErr]).transpose()
    os.makedirs("output/autocorrelation", exist_ok=True)
    np.savetxt(
        f"output/autocorrelation/{name}_{alg}.csv",
        data,
        delimiter=",",
        header="T,tauExp,tauExp_error",
        comments="",
    )
    cmd = [
        "/usr/bin/python3",
        "mkplots/plot_autocorrelation_time.py",
        f"-alg {alg} -o {name}"
    ]
    #os.system(" ".join(cmd))
