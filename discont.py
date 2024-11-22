#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0,1,200)-0.5
h = np.heaviside(x,1)

path = "output"

fig, ax = plt.subplots()
x_left = np.linspace(-.5,0-0.01) 
x_right = np.linspace(0,.5)
ax.plot(x_left, np.heaviside(x_left,1),color="tab:blue")
ax.plot(x_right, np.heaviside(x_right,1),color="tab:blue")
ax.set_xticks([],[])
ax.set_yticks([],[])
ax.set_ylabel(r"$\chi_T$",fontsize=20)
ax.set_xlabel(r"$H$",fontsize=20)
fig.savefig(f"{path}/discont_{2}.pdf",format="pdf",bbox_inches="tight")

fig, ax = plt.subplots()
ax.plot(x, h*x,color="tab:blue")
ax.set_xticks([],[])
ax.set_yticks([],[])
ax.set_ylabel(r"$M$",fontsize=20)
ax.set_xlabel(r"$H$",fontsize=20)
fig.savefig(f"{path}/discont_{1}.pdf",format="pdf",bbox_inches="tight")

fig, ax = plt.subplots()
ax.plot(x, 0.5*h*x**2,color="tab:blue")
ax.set_xticks([],[])
ax.set_yticks([],[])
ax.set_ylabel(r"$\mathcal{F}$",fontsize=20)

ax.set_xlabel(r"$H$",fontsize=20)
fig.savefig(f"{path}/discont_{0}.pdf",format="pdf",bbox_inches="tight")