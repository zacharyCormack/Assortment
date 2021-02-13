#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(figsize=(8, 8), facecolor="lightgray")

ax = plt.subplot(111, frameon=False)

data = np.random.normal(.5, .5, (128, 150))
X = np.linspace(-1.2, 1.2, data.shape[-1])
G = 1.5 * np.exp(-4 * X ** 2)

# Generate line plots
get_y = lambda pdist, value, pos: 400*(1 - pdist) + (1/(1+1/pdist)-pdist)*(
	10*value*(np.sin(pos*17)+3)*(np.sin(pos*13)+3) - pos**2*6) - 225

lines = []
for i in range(len(data)):
	# one point perspective
	# add 5 to i to make start not immediate
	pdist  = 1 / (i+3)
	xscale = 2 * pdist
	y = get_y(pdist, G*data[i], X)
	line, = ax.plot(xscale*X, y, color="dimgray", lw=xscale*12)
	lines.append(line)

ax.set_ylim(0, 200)

ax.set_xticks([])
ax.set_yticks([])


def update(*args):
	data[:, 1:] = data[:, :-1]
	data[:, 0] = np.random.normal(.5, .5, len(data))

	for i in range(len(data)):
		lines[i].set_ydata(get_y(1 / (i+3), G*data[i], X))

	# Return modified artists
	return lines

# Construct the animation, using the update function as the animation director.
anim = animation.FuncAnimation(fig, update, interval=7)
plt.show()
