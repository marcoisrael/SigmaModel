#!/bin/bash/python3
import matplotlib.pyplot as plt 
import numpy as np

c = 2*0.5**2
fig, ax = plt.subplots() 
x = np.linspace(0.35,0.5)
y = 2*x**2
ax.plot(x, y, color="tab:blue", ls="dashed")
x = np.linspace(0.5, 0.65)
y = c+(x-0.5)**2
ax.plot(x, y, color="tab:blue", ls="dashed")
ax.plot([0.65],[c+0.15**2],marker="o",color="black")

x = np.linspace(0.45, 0.5)
y = c-6*(x-0.5)
ax.plot(x, y, color="tab:blue", ls="dashed")

ax.text(0.4,0.54,"Sólido", fontsize=16)
ax.text(0.55,0.37, "Gaseoso", fontsize=16)
ax.text(0.55,0.65, "Líquido", fontsize=16)
ax.text(0.53,0.47, "Evaporación", rotation=2)
ax.text(0.4,0.35, "Sublimación", rotation=38)
ax.text(0.466,0.65, "Fusión", rotation=-70)
ax.text(0.65+0.005,c+0.15**2-0.01,r"$T_c$", fontsize=16)
ax.set_xlim(0.33,0.68)
ax.set_ylim(0.25,0.8)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel(r"$T$", fontsize=20)
ax.set_ylabel(r"$P$", fontsize=20)
fig.savefig("output/phase_liquid.pdf", format="pdf", bbox_inches="tight")


fig, ax = plt.subplots() 
x = np.linspace(0, 1)
y = 0*x
ax.plot(x, y, color="black")
t = np.linspace(0,np.pi, 200)
ax.plot(np.cos(t),np.sin(t), color="tab:blue", ls="dashed")
ax.plot([1],[0], marker="o",color="black")
ax.text(1.02,-0.02,r"$T_c$", fontsize=16)
ax.set_xlim(0,1.4)
#ax.set_ylim(-1,1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel(r"$T$", fontsize=20)
ax.set_ylabel(r"$M$", fontsize=20)
# plt.show()
fig.savefig("output/phase_magnet.pdf", format="pdf", bbox_inches="tight")
