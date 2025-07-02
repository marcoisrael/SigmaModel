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
T = np.array([0.75,0.8,0.85,0.9,1.0,1.2,1.4,1.6,1.8,2.0])
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
for alg in algs:
    tau_exp = []
    tau_exp_error = []
    tau_int = []
    tau_int_error = []
    Ti = []
    for temp in T:
        path = f"output/record/L{L}/{alg}/{temp}.csv"
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        val = 0.5
        c0 = correlation(data[:, obs[name]["index"]],0)[1]
        ct = np.zeros(3)
        n = 0
        for t in range(1,data[:,0].size):
            ct = correlation(data[:, obs[name]["index"]],t)/c0
            if ct[1]>=0:
                val = val+ct[1]
            else:
                n = t
                break
         
        tau_int.append(val)
        tau_int_error.append(np.sqrt(2*val)*np.sqrt(c0/n))
        Ti.append(temp)
        
        X = []
        for t in np.arange(0, 101):
            x = correlation(data[:, obs[name]["index"]], t)
            X.append(x)
        p0=0
        X = np.array(X)
        t, q, qErr = X[:, 0], X[:, 1] / X[0, 1], X[:, 2] / X[0, 1]
        
        xfit = fit(t[p0:], q[p0:], qErr[p0:])
        
        def f(x, a,b):
            return a*np.exp(-x/b)
        

        xfit.fiting(f, args={"bounds": ((0, np.inf))})
        tau_exp.append(xfit.opt[1])
        tau_exp_error.append(xfit.error[1])
        
        #print(f"temp = {temp}","tau_int = "+fix(val,error), "  ", "tau_exp = "+fix(xfit.opt[1],xfit.error[1]))
  
          
        x = np.linspace(t[0], t[-1], 500)
        if make_temp_plots:
            fig, ax = plt.subplots(tight_layout=True)
           
            ax.plot(x, f(x, *xfit.opt), linewidth=1.2, color="tab:blue",
                    label="Ajuste")
            ax.errorbar(
                t,
                q,
                qErr,
                fmt="o",
                capsize=1,
                elinewidth=1,
                markersize=2,
                color="tab:red",
                label="Autocorrelación",
            )
            ax.set_xlabel(r"$t$", fontsize=20)
            ax.set_ylabel(r"$\frac{C_{MM}(t)}{C_{MM}(0)}$", fontsize=20)
            # ax.legend()
           
            os.makedirs(f"output/plot/{name}/L{L}/{alg}", exist_ok=True)
            fig.tight_layout()
            fig.savefig(
                f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.pdf",
                format="pdf",
                bbox_inches="tight",
            )
            #print(f"output/plot/{name}/L{L}/{alg}/{alg}_{temp}.svg")
            plt.close()
            del ax, fig
    
    tau_int = np.array(tau_int)
    tau_int_error = np.array(tau_int_error)
    tau_exp = np.array(tau_exp)
    tau_exp_error = np.array(tau_exp_error)
    data = np.array([Ti, tau_int, tau_int_error, tau_exp, tau_exp_error]).transpose()
    os.makedirs("output/autocorrelation", exist_ok=True)
    # np.savetxt(
    #      f"output/autocorrelation/{name}_{alg}.csv",
    #      data,
    #      delimiter=",",
    #      header="T,tauExp,tauExp_error",
    #      comments="",
    #  )
    # cmd = [
    #      "/usr/bin/python3",
    #      "mkplots/plot_autocorrelation_time.py",
    #      f"-alg {alg} -o {name}"
    #  ]
    # os.system(" ".join(cmd))
