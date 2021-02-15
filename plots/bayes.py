#!/usr/local/bin/python3

'''
BAYES' THEOREM
with probability density
P(A|B) = P(B|A) * P(A) / P(B)
'''

from matplotlib import pyplot as plt, colors, cm
import numpy as np
from scipy.stats import multivariate_normal
from scipy.integrate import dblquad

res = .25

x, y = np.mgrid[0:12:res, 0:20:res]
mean = [6, 10]
cov  = [[5.5, -5], [-5, 7]]

point_dist = multivariate_normal(mean, cov, seed=1611433680)
point_space = point_dist.pdf(np.dstack((x, y)))

point = point_dist.rvs()

def new_info(p, s, x, y):
	new_p = s.rvs()
	if new_p[0] < p[0]:
		x_sl = slice(None, None, -1)
	else:
		x_sl = slice(None, None,  1)
	if new_p[1] < p[1]:
		y_sl = slice(None, None, -1)
	else:
		y_sl = slice(None, None,  1)
	# use cdf to calculate
	return s.cdf(np.dstack((x[x_sl,:], y[y_sl,:])))[x_sl, y_sl]

fig, axes = plt.subplots(3, 4)
axes = axes.ravel()
dist = point_space

my_cm = plt.get_cmap('terrain')

dists = [dist]

for _ in range(len(axes)-1):
	new_d = new_info(point, point_dist, x, y)
	prod = dist * new_d
	def get_index(y_pos, x_pos):
		return prod[int(x_pos//res), int(y_pos//res)]
	dist = prod / dblquad(get_index, 0, 10, 0, 20, None, res, res)[0]
	dists.append(dist)

max_val = max([i.max() for i in dists])
tk_space = np.linspace(0, 40, 21)
norm = colors.BoundaryNorm(tk_space, 256, extend='max')
cbar = plt.colorbar(cm.ScalarMappable(norm, my_cm), ax=axes,
	ticks=tk_space, orientation='horizontal', extend='max')
fmt = r'$\frac{%d\%%}{{cm}^2}$'
cbar.ax.set_xticklabels([fmt %i for i in tk_space])

for ax, d in zip(axes, dists):
	ax.imshow(d*100, cmap=my_cm, norm=norm, extent=(0, 20, 0, 12),
		interpolation='gaussian')
	ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%d cm'))
	ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d cm'))

plt.show()
