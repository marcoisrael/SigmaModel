from numpy import sin, cos, pi, array, arccos, sqrt, dot
from numpy import arcsin, cross, shape, transpose, linspace, meshgrid
from numpy.random import random
from arrowClass import *

import matplotlib.pyplot as plt

s = array([1,1,1])
s = s/sqrt(dot(s,s))
phi = 2*pi*random()
theta = arcsin(random())
#r = array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
r = array([1,1,-1])
r = r/sqrt(dot(r,r))
k = cross(s,r)
k = k/sqrt(dot(k,k))

delta = 0.2
alpha = arccos(1-2*delta*random())
u = s*cos(alpha)+cross(k,s)*sin(alpha)
u = u/sqrt(dot(u,u))

fig = plt.figure(dpi=200)
ax = fig.add_subplot(projection='3d')

U = []
for alpha in linspace(0,alpha):
	u = s*cos(alpha)+cross(k,s)*sin(alpha)
	U.append(u)
U = 0.9*array(U)
ax.plot(U[:,0],U[:,1],U[:,2], color="red")
names=[r"$\vec{r}$",r"$\vec{s_0}$",r"$\vec{k}$",r"$\vec{s_r}$"]
shifts=[[0.2,0.2,0.2],[0.1,0.1,0.1],[0.2,0.2,0.2],[0.3,0.1,0.2]]
for v, vec, delta in zip([r,s,k,u],names,shifts):
	x, y, z = v
	ax.arrow3D(0,0,0,x,y,z, mutation_scale=16,ec ='black',fc='black')
	ax.text(x+delta[0]*x,y+delta[1]*y,z+delta[2]*z,vec,fontsize=16)

u, v = linspace(0,pi), linspace(0,2*pi)
u,v = meshgrid(u,v)
x = sin(u)*cos(v)
y = sin(u)*sin(v)
z = cos(u)
ax.plot_wireframe(x, y, z, alpha=0.5,rstride=2, cstride=2, linewidth=0.7)


lim = 1
t = linspace(-lim,lim)

a, c, b = k
z = -(a*x+b*y)/c
#ax.plot_surface(x, z, y, alpha=0.3)


#t = linspace(0,2*pi)
#plt.plot(cos(t), sin(t), 0)

lim = 1.1
ax.set_xlim(-lim,lim)
ax.set_ylim(-lim,lim)
ax.set_zlim(-lim,lim)
ax.set_aspect("equal")
ax.axis("off")
ax.view_init(-30,65)
#plt.show()
fig.savefig("output/cone.pdf", format="pdf" , bbox_inches="tight")
