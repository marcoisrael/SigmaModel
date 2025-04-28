import matplotlib.pyplot as plt
import numpy as np

n=5000
u, v = np.random.random(n),np.random.random(n)
fig, ax = plt.subplots()
ax.plot(u,v, ls="",marker=".",markersize=1)
ax.set_xlabel(r"$v$", fontsize=20)
ax.set_ylabel(r"$u$", fontsize=20)
ax.set_xlim([0,1])
ax.set_ylim([0,1])
fig.savefig("output/dist1.pdf", format="pdf", bbox_inches="tight")

theta, phi = np.arccos(1-2*u), 2*np.pi*v

fig, ax = plt.subplots()

ax.plot(phi,theta, ls="",marker=".",markersize=1)
ax.set_xlabel(r"$\phi$", fontsize=20)
ax.set_ylabel(r"$\theta$", fontsize=20)
ax.set_xlim([0,2*np.pi])
ax.set_ylim([0,np.pi])
fig.savefig("output/dist2.pdf", format="pdf", bbox_inches="tight")

# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")
# x = np.sin(theta) * np.cos(phi)
# y = np.sin(theta) * np.sin(phi)
# z = np.cos(theta)
# ax.plot(x,y,z, ls="",marker=".")
# ax.set_xlabel(r"$\phi$", fontsize=20)
# ax.set_ylabel(r"$\theta$", fontsize=20)
# ax.set_aspect("equal")
# ax.axis("off")
# plt.show()
