#!/usr/bin/python3 
import matplotlib.pyplot as plt
import numpy as np
n=60

fig, ax = plt.subplots()

path="output/hot.csv"
data = np.loadtxt(path, delimiter=",", skiprows=1)
ax.plot(data[:n,0], ls="dotted", color="red", label="Hot start")

path="output/cold.csv"
data = np.loadtxt(path, delimiter=",", skiprows=1)
ax.plot(data[:n,0],ls="dotted", color="blue", label="Cold start")

ax.set_ylabel(r"$h$", fontsize=20)
ax.set_xlabel(r"$i$", fontsize=20)
ax.legend()
fig.savefig(
	f"output/thermalization.pdf",
	format="pdf",
	bbox_inches="tight",
)
