import numpy as np
from numpy.random import random
from arrowClass import *

import matplotlib.pyplot as plt

s = np.array([0,-np.sin(0.3),np.cos(0.3)])
# s = s/np.sqrt(np.dot(s,s))
phi = 2*np.pi*random()
theta = np.arcsin(random())
#r = array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
r = np.array([1,1,-1])
r = r/np.sqrt(np.dot(r,r))
k = np.cross(s,r)
k = k/np.sqrt(np.dot(k,k))

delta = 0.1
alpha = np.arccos(1-delta)
u = s*np.cos(alpha)+np.cross(k,s)*np.sin(alpha)
u = u/np.sqrt(np.dot(u,u))

fig = plt.figure(dpi=200)
ax = fig.add_subplot(projection='3d')

U = []
for alpha in np.linspace(0,alpha):
	u = s*np.cos(alpha)+np.cross(k,s)*np.sin(alpha)
	U.append(u)
U = 0.9*np.array(U)
ax.plot(U[:,0],U[:,1],U[:,2], color="red")
names=[r"$\vec{r}$",r"$\vec{s_0}$",r"$\vec{k}$",r"$\vec{s_r}$"]
shifts=[[0.2,0.2,0.2],[0.1,0.1,0.1],[0.2,0.2,0.2],[0.3,0.1,0.2]]
for v, vec, delta in zip([r,s,k,u],names,shifts):
	x, y, z = v
	ax.arrow3D(0,0,0,x,y,z, mutation_scale=16,ec ='black',fc='black')
	ax.text(x+delta[0]*x,y+delta[1]*y,z+delta[2]*z,vec,fontsize=16)

u, v = np.linspace(0,np.pi), np.linspace(0,2*np.pi)
u,v = np.meshgrid(u,v)
x = np.sin(u)*np.cos(v)
y = np.sin(u)*np.sin(v)
z = np.cos(u)
ax.plot_wireframe(x, y, z, alpha=0.5,rstride=2, cstride=2, linewidth=0.7)

t = np.linspace(0,2*np.pi)
z = np.linspace(0,1)
t , z = np.meshgrid(t, z)
c = 0.6
x, y = c*z*np.cos(t), c*z*np.sin(t)

alpha = 0.3

y = y*np.cos(alpha)-z*np.sin(alpha)
z = y*np.sin(alpha)+z*np.cos(alpha)

ax.plot_surface(x, y, z, alpha=0.5)

# lim = 1.1
# ax.set_xlim(-lim,lim)
# ax.set_ylim(-lim,lim)
# ax.set_zlim(-lim,lim)

ax.set_aspect("equal")
ax.axis("off")
ax.view_init(41,47)
# plt.show()

fig.savefig("output/cone.pdf", format="pdf" , bbox_inches="tight")
