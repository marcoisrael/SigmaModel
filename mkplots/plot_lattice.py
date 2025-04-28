#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np


def rsquare(x, y):
    ax.plot(sx + x, sy + y, color="black", linewidth=0.5)
    ax.plot(rdx + x, rdx + y, color="black", linewidth=0.5)


def lsquare(x, y):
    ax.plot(sx + x, sy + y, color="black", linewidth=0.5)
    ax.plot(ldx + x, ldy + y, color="black", linewidth=0.5)


sx, sy = np.array([0, 0, 1, 1, 0]), np.array([0, 1, 1, 0, 0])
rdx, rdy = np.array([0, 1]), np.array([0, 1])
ldx, ldy = np.array([0, 1]), np.array([1, 0])

fig, ax = plt.subplots()

k = 1
for i in range(7):
    for j in range(7):
        if k > 0:
            rsquare(j, i)
        else:
            lsquare(j, i)
        k = -k
ax.axis("off")
ax.set_aspect("equal")
fig.savefig("output/lattice.pdf", format="pdf", bbox_inches="tight")

fig, ax = plt.subplots()
lsquare(0, 0)
ax.text(-0.06, -0.06, r"$\vec{s}_1$", fontsize=14)
ax.text(1.01, -0.05, r"$\vec{s}_2$", fontsize=14)
ax.text(-0.06, 1.02, r"$\vec{s}_3$", fontsize=14)
ax.text(1.0, 1.01, r"$\vec{s}_4$", fontsize=14)
ax.text(0.25, 0.25, r"$1$", fontsize=14)
ax.text(0.75, 0.75, r"$2$", fontsize=14)
ax.axis("off")
ax.set_aspect("equal")
fig.savefig("output/lsquare.pdf", format="pdf", bbox_inches="tight")

fig, ax = plt.subplots()
rsquare(0, 0)
ax.text(-0.06, -0.06, r"$\vec{s}_3$", fontsize=14)
ax.text(1.01, -0.05, r"$\vec{s}_1$", fontsize=14)
ax.text(-0.06, 1.02, r"$\vec{s}_4$", fontsize=14)
ax.text(1.0, 1.01, r"$\vec{s}_2$", fontsize=14)
ax.text(0.75, 0.25, r"$1$", fontsize=14)
ax.text(0.25, 0.75, r"$2$", fontsize=14)

ax.axis("off")
ax.set_aspect("equal")
fig.savefig("output/rsquare.pdf", format="pdf", bbox_inches="tight")
