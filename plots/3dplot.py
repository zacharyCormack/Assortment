#!/usr/local/bin/python3

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure()

ax1 = fig.add_subplot(331, projection='3d')
ax2 = fig.add_subplot(332, projection='3d')
ax3 = fig.add_subplot(333, projection='3d')
ax4 = fig.add_subplot(334, projection='3d')
ax5 = fig.add_subplot(335, projection='3d')
ax6 = fig.add_subplot(336, projection='3d')
ax7 = fig.add_subplot(337, projection='3d')
ax8 = fig.add_subplot(338)
ax9 = fig.add_subplot(339)

# Regular 3D plots:

x = np.arange(-15, 15, 0.02)
y = np.arange(-15, 15, 0.02)
x, y = np.meshgrid(x, y)
R = np.sqrt(x ** 2 + y ** 2)

# ripple:
z = np.sin(R)
surf = ax2.plot_surface(x, y, z, cmap="plasma", rstride=8, cstride=8,
			linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5, ax=ax2)

# wobbling ripple:

z = np.sqrt(R) * np.sin(R) + np.sin(x) * np.sin(y)
surf = ax3.plot_surface(x, y, z, cmap="viridis", rstride=8, cstride=8,
			linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5, ax=ax3)

# waves: z = np.sin(D - 20*np.arcsin(y/R))

# polar plots:

R = np.arange(0, np.pi*10, 0.05)
T = np.arange(0, np.pi*2, 0.01)
R, T = np.meshgrid(R, T)

L = np.maximum(np.log(R), 0)
x = np.cos(T) * R
y = np.sin(T) * R

# fracal ossilation:

z = np.sin(L * np.pi) * L
surf = ax1.plot_surface(x, y, z, cmap="magma", rstride=8, cstride=8,
			linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5, ax=ax1)

# fractal spriral:

z = np.sin(T + L * np.pi) * L
surf = ax4.plot_surface(x, y, z, cmap=cm.jet, rstride=8, cstride=8,
			linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5, ax=ax4)

# plot on arbitrary shape: circoid!

r = np.arange(0, 10*np.pi, 0.2)
t = np.arange(0, np.pi*2+0.1, 0.02)
r, t = np.meshgrid(r, t)
d = 2 * r * (1-np.cos(t))
x = d * np.cos(t)
y = d * np.sin(t)
z = np.sin(r) + np.sin(t - np.pi/2)

surf = ax5.plot_surface(x, y, z, cmap="viridis", rstride=1, cstride=1,
			linewidth=0, antialiased=False)
ax5.set_xlim(-130, 20)
ax5.set_ylim(-100, 100)
ax5.set_zlim(-5, 5)
fig.colorbar(surf, shrink=0.5, aspect=5, ax=ax5)

# gradient field:

dr = np.cos(r)
dt = np.cos(t * np.pi/2)
dm = np.sqrt(dr ** 2 + dt ** 2)

ax8.quiver(x[64:-64:8,32::8], y[64:-64:8,32::8], dr[64:-64:8,32::8],
			dt[64:-64:8,32::8], linewidth=1.5, alpha=0.8)
ax8.axis("equal")
# grad = ax9.scatter(x, y, c=dM, s=0.5, alpha=0.8, cmap="copper")
# fig.colorbar(grad, shrink=0.5, aspect=5, extend='max', ax=ax9)

# torus!

t1 = np.arange(0, np.pi*25/12, np.pi/6)
t2 = np.arange(0, np.pi*7/3, np.pi/3)

t1, t2 = np.meshgrid(t1, t2)

xs = np.cos(t1) * (3 + np.cos(t2))
ys = np.sin(t1) * (3 + np.cos(t2))
zs = np.sin(t2)

x = np.arange(-np.pi-0.01, np.pi+0.01, 0.001)

tla = 6 * np.tan(x/2)
tlb = 6 / np.tan(x/2)
tla -= tla % (np.pi / 1000)
tlb -= tlb % (np.pi / 1000)
xla = np.cos(x) * (3 + np.cos(tla))
yla = np.sin(x) * (3 + np.cos(tla))
zla = np.sin(tla)
xlb = np.cos(x) * (3 + np.cos(tlb))
ylb = np.sin(x) * (3 + np.cos(tlb))
zlb = np.sin(tlb)

ax6.set_xlim(-4, 4)
ax6.set_ylim(-4, 4)
ax6.set_zlim(-4, 4)

ax6.plot(xla, yla, zla, "k-", linewidth=3)
ax6.plot(xlb, ylb, zlb, "r-", linewidth=3)

ax6.plot_wireframe(xs, ys, zs)

x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.3),
		      np.arange(-0.8, 1, 0.3),
		      np.arange(-0.8, 1, 0.3))
u =  np.sin(np.pi * x)  * np.cos(np.pi * y) * np.cos(np.pi * z)
v = -np.cos(np.pi * x)  * np.sin(np.pi * y) * np.cos(np.pi * z)
w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
			  np.sin(np.pi * z))

ax7.quiver(x, y, z, u, v, w, length=0.2)

x, y = np.meshgrid(np.arange(-4, 4, 0.005), np.arange(-4, 4, 0.005))
r = np.sqrt(x**2 + y**2)
m = np.e**(-r**2)*(4*r**2-2)+2
u =  y*m - x*(r-1.5**0.5)*0.12
v = -x*m - y*(r-1.5**0.5)*0.12

ax9.streamplot(x, y, u, v, color=m, cmap=cm.coolwarm, linewidth=(m**2+2)/3)

ax9.set_aspect("equal", "box")

fig.tight_layout()

plt.show()