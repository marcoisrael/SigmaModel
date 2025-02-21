#!/usr/bin/python3
from numpy import sin, cos, linspace, meshgrid, pi, array, dot, sqrt
from arrowClass import *
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
u, v = linspace(0, 2*pi), linspace(0, 2 * pi)
u, v = meshgrid(u, v)

# R, r = 2, 1.01
# x = (R+r*cos(u))*cos(v)
# y = (R+r*cos(u))*sin(v)
# z = r*sin(u)
# ax.plot_wireframe(x, y, z, rstride=2, cstride=8)

R, r = 2, 1
x = (R+r*cos(u))*cos(v)
y = (R+r*cos(u))*sin(v)
z = r*sin(u)
ax.plot_wireframe(x, y, z, color="red",rstride=2, cstride=2, linewidth=0.7)

ax.set_aspect("equal")
ax.view_init(35, 0)
ax.axis("off")
# plt.show()
fig.savefig("output/toro.pdf", format="pdf", bbox_inches="tight")
