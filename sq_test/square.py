#!/usr/local/bin/python3

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
# from random import random
import pandas as pd

fig = plt.figure()

ax1 = fig.add_subplot(221, projection='3d')
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223, projection='3d')
ax4 = fig.add_subplot(224)


# t = np.arange(0, 1, 0.01)
# r = np.arange(0, 2, 0.01)

# t, r = np.meshgrid(t, r)

# inside = r < 2/np.cos(t)

# ax1.scatter((np.cos(t)*r)[inside], (np.sin(t)*r)[inside])

SIZE = 0.70710678
# F_A = lambda x: 2*np.sqrt(x**2+1)
# F_B = lambda x: np.sqrt(1/2+1/F_A(x))
# F_C = lambda x: x/np.sqrt(2+F_A(x))
# F_D = lambda x: x/2*F_A(x) + np.log(F_B(x)+F_C(x)) - np.log(F_B(x)-F_C(x))
# F_E = lambda b, h: h**3*(F_D(b) + F_D(SIZE-b))
# F   = lambda x, y: (.5 + F_E(x,y) + F_E(x,SIZE-y) + F_E(y,x) + F_E(y,SIZE-x))/3

x = np.arange(0, SIZE-0.01, 0.01)
y = np.arange(0, SIZE-0.01, 0.01)

x, y = np.meshgrid(x, y)

# def test(x, y):
# 	total = 0
# 	i = 0
# 	while i < 0x1000:
# 		i += 1
# 		x_0 = random()*SIZE
# 		y_0 = random()*SIZE
# 		total += np.sqrt((x-x_0)*(x-x_0)+(y-y_0)*(y-y_0))
# 	return total / 0x1000

# z1 = [[test(x[i, j], y[i, j]) for j in range(len(x[i]))] for i in range(len(x))]
# z1 = np.array(z)

# z2 = F(x, y)

z1 = np.array(pd.read_csv("out.csv", nrows=70))
z2 = np.array(pd.read_csv("out.csv", skiprows=70))

x  = np.delete( x, 69, 0)
y  = np.delete( y, 69, 0)
z1 = np.delete(z1, 69, 0)
x  = np.delete( x,  0, 1)
y  = np.delete( y,  0, 1)
z1 = np.delete(z1,  0, 1)
z2 = np.delete(z2,  0, 1)

dev = np.mean((z1 - z2)**2)**0.5
dev_perc = dev * 100 / np.mean(z1)

ax2.set_aspect('equal', adjustable='box')
ax4.set_aspect('equal', adjustable='box')

ax1.plot_surface(x, y, z1)
ax2.contourf    (x, y, z1)
ax3.plot_surface(x, y, z2)
ax4.contourf    (x, y, z2)

print("Standard deviation of difference: %.4f or %.2f%%" %(dev, dev_perc))

# while i-1:
# 	i -= 1
# 	total = 0
# 	x = random() * SIZE
# 	y = random() * SIZE

# 	print("Expected average distance:", F(x, y))

# 	k = j

# 	while k-1:
# 		k -= 1
# 		x_0 = random()*SIZE
# 		y_0 = random()*SIZE
# 		total += np.sqrt((x-x_0)*(x-x_0)+(y-y_0)*(y-y_0))
# 	print("Average to (%.2f,%.2f): %3.3f\n" %(x, y, total/j))

plt.savefig("compare.svg")