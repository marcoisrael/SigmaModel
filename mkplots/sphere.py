from numpy import sin, cos, linspace, meshgrid, pi, array, dot, sqrt
from arrowClass import *
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
u, v = linspace(0, pi), linspace(0, 2 * pi)
u, v = meshgrid(u, v)
x = sin(u) * cos(v)
y = sin(u) * sin(v)
z = cos(u)
# ~ ax.plot_surface(x, y, z, alpha=0.2, color="orange")
ax.plot_wireframe(x, y, z,  color="red", rstride=2, cstride=2, linewidth=0.7)
v = array([1, -1, 1])
x, y, z = v / sqrt(dot(v, v))
ax.arrow3D(0, 0, 0, x, y, z, mutation_scale=16,
           ec="blue", fc="blue", alpha=0.6)
t = linspace(0, 2 * pi, 100)
# ~ ax.plot(cos(t), sin(t), 0 * t, linewidth=0.7, color="black")
delta = 0.1
ax.text(x + delta * x, y + delta * y, z + delta * z, r"$\vec{s}$", fontsize=16)
ax.set_aspect("equal")
ax.view_init(22, 60)
ax.axis("off")
fig.savefig("output/sphere.pdf", format="pdf", bbox_inches="tight")
