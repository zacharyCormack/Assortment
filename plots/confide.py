#!/usr/local/bin/python3

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from random import gauss, sample, seed
import numpy as np
from math import factorial as fac

i_prep = lambda x, y: [(x[i],y[i],x[i+1],y[i+1]) for i in range(len(x)-1)]

# returns a tuple of derivatives, each a list of tuples of coords
def my_inter(coords, deg=2):
	deg-=1
	# when linear interpolation in next degree must cross these points
	targ = [((sx+ex) / 2, (ey-sy) / (ex-sx)) for sx,sy,ex,ey in coords]
	targ.append((coords[-1][2], targ[-1][1]))
	
	# based on targets, create slopes:
	slopes = [(coord[0],0) for coord in coords]
	slopes.append((coords[-1][2], targ[-1][1]))
	for i, t, s in zip(range(len(targ)-1,0,-1), targ[-2::-1], slopes[::-1]):
		"""
		To make the midpoint derivatives average the targes,
		s, t, and slopes[i-1] must be colinear.
		t is the slope in the centre,
		s and slopes[i-1] on the sides.
		If there is another layer of interpolation,
		these are not the same. In this case,
		adjust slopes[i-1] to align the points.
		"""
		if not deg:
			slopes[i-1] = t
		if not (t[0] - s[0]):
			slopes[i-1] = (slopes[i-1][0], t[1])
			continue
		slope = (t[1] - s[1]) / (t[0] - s[0])
		slopes[i-1] = (slopes[i-1][0],
			(t[1] - (t[0] - slopes[i-1][0]) * slope))

	if not deg:
		return (slopes,)
	return (slopes,) + my_inter(i_prep(*zip(*slopes)), deg=deg)

def my_integ(ds, newl=None):
	if newl == None:
		newl = np.arange(ds[0,0,0], ds[0,-1,0], .01)
	vals = []
	for n in newl:
		pairs = [(i, p) for i, p in enumerate(ds[0]) if p[0] < n]
		if not pairs:
			continue
		pos, prev = pairs[-1]
		eps = n - prev[0]
		next = ds[0,pos+1] if pos+2 < len(list(ds[0,:,0])) else prev
		x_space = next[0] - prev[0]
		y_space = next[1] - prev[1]

		pds = np.array([ds[i,pos,1] for i in range(len(ds))])
		
		val = 0
		end_curve = 0
		for i, p in enumerate(pds):
			val += p * eps**i / fac(i)
			end_curve += p * x_space**i / fac(i)
		
		# ...
		y_step = val - prev[1]
		f_step = end_curve - prev[1]
		scale = y_space / f_step if f_step else 0
		p_scale = 1 + (scale - 1) * (eps / x_space if x_space else 0)

		scaled_val = y_step * p_scale + prev[1]

		vals.append((n, scaled_val))
	return np.array(vals)
	 

# fixed seed:
seed(1611433680)

fig = plt.figure()

ax1 = fig.add_subplot(121)

vals  = np.arange(2, 5, .005)

trend = lambda x: 1/2*x**2 - x + 3
noise = lambda x: gauss(0, 1)
dist  = lambda x: (x, trend(x) + noise(x))

raw   = [dist(x) for x in sample(list(vals), 250)]
data  = list(zip(*sorted(raw, key=lambda x: x[0])))

estim = np.poly1d(np.polyfit(data[0], data[1], 2))

pl_1  = ax1.fill_between(vals, trend(vals) + 1, trend(vals) - 1, alpha=.3)
pl_2, = ax1.plot(vals, trend(vals), 'r--')
pl_3  = ax1.scatter(data[0], data[1], 20, color=[.5,.8,.4,.6], edgecolors='red')
pl_4, = ax1.plot(vals, estim(vals), 'g-.')

ax1.legend([pl_3,(pl_1,pl_2),pl_4], ["Sample","Trend","Estimation"])

plt.margins(0, .1)

ax2 = fig.add_subplot(122)

vals  = np.arange(-2, 3.5, .01)
val_sample = np.array(sorted(sample(list(vals), 15)))

func = lambda x: .1*x**4 - .1*x**3 - x**2 + x/5 + 4/3
results = func(val_sample)

slopes = my_inter(i_prep(val_sample, results))
slopes = np.array((list(zip(val_sample, results)),) + slopes)
interp = my_integ(slopes)

print(interp)

ax2.scatter(val_sample, results, label="Points")
ax2.plot(*zip(*interp), label="Quadratic Interpolation")
ax2.plot(vals, func(vals), 'r--', label="Quartic", alpha=.4)
ax2.legend()

plt.margins(0, .1)
plt.show()
