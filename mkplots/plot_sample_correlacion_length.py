#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from plotClass import fit

alg = "lexic_metropolis"
temp=1.0
LENGTH=32
path = f"output/correlation_length/L{LENGTH}/{alg}/{temp}.csv"
# print(path)
data = np.loadtxt(path, delimiter=",", skiprows=1)

def f(x, a, b):
    return a * np.exp(-x / b) + a * np.exp((x - LENGTH) / b)

xfit = fit(data[:, 0], data[:, 1], data[:, 2])
xfit.fiting(f, args={"bounds": ((0, np.inf))})

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
ax.set_ylabel(r"$\langle\vec{\sigma_i}\cdot\vec{\sigma_0}\rangle_c$", fontsize=18)
ax.set_xlabel(r"$i$", fontsize=18)
fig.savefig(
    f"output/plot/correlation_length/lexic_metropolis_L{LENGTH}_{temp}.svg",
    format="pdf",
    bbox_inches="tight"
)

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
ax.set_ylabel(r"$\langle\vec{\sigma_i}\cdot\vec{\sigma_0}\rangle_c$", fontsize=18)
ax.set_xlabel(r"$i$", fontsize=18)
ax.set_yscale("log")
fig.savefig(
    f"output/plot/correlation_length/lexic_metropolis_L{LENGTH}_{temp}_log.svg",
    format="pdf",
    bbox_inches="tight"
)

