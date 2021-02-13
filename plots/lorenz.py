#!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons

fig = plt.figure()
ax = fig.gca(projection="3d")

title = r"""LORENZ ATTRACTOR
$\frac{\delta x}{\delta t} = %05.2f (y-z) \quad\qquad (\sigma) = %05.2f$
$\frac{\delta y}{\delta t} = z(%05.2f - z) - y  \quad (\rho)   = %05.2f$
$\frac{\delta z}{\delta t} = xy - %05.2f z\quad\qquad (\beta)  = %05.2f$
"""

plt.subplots_adjust(left=0.25, bottom=0.25)

rho = 28.0
sig = 10.0
bet = 8.0 / 3.0
state0 = 1,1,1

title_txt = fig.suptitle(title %(sig, sig, rho, rho, bet, bet))

def f(state, t):
    x, y, z = state  # Unpack the state vector
    return sig * (y - x), x * (rho - z) - y, x * y - bet * z  # Derivatives

def gen_data():
	st = state0
	t = np.arange(0.0, 40.0, 0.01)

	states = odeint(f, st, t)
	return states

states = gen_data()

l, = ax.plot(states[:, 0], states[:, 1], states[:, 2])

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.margins(x=0)

axcolor = 'lightgoldenrodyellow'
ax_rho = plt.axes([0.15, 0.08, 0.3, 0.02], facecolor=axcolor)
ax_sig = plt.axes([0.15, 0.12, 0.3, 0.02], facecolor=axcolor)
ax_bet = plt.axes([0.15, 0.16, 0.3, 0.02], facecolor=axcolor)

ax_sz  = plt.axes([0.6, 0.08, 0.3, 0.02], facecolor=axcolor)
ax_sy  = plt.axes([0.6, 0.12, 0.3, 0.02], facecolor=axcolor)
ax_sx  = plt.axes([0.6, 0.16, 0.3, 0.02], facecolor=axcolor)

rho_sl = Slider(ax_rho, r'$\rho$',    0, 30, valinit=28 )
sig_sl = Slider(ax_sig, r'$\sigma$',  0, 20, valinit=10 )
bet_sl = Slider(ax_bet, r'$\beta$',   0, 10, valinit=8/3)
sx_sl  = Slider(ax_sx,  'x coord.', -30, 30, valinit=1  )
sy_sl  = Slider(ax_sy,  'y coord.', -30, 30, valinit=1  )
sz_sl  = Slider(ax_sz,  'z coord.', -30, 30, valinit=1  )

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)

def reset(event):
	rho_sl.reset()
	sig_sl.reset()
	bet_sl.reset()

	sx_sl.reset()
	sy_sl.reset()
	sz_sl.reset()

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")

	title_txt.set_text(title %(sig, sig, rho, rho, bet, bet))

lbl = 'red'
l.set_color(lbl)

def colorfunc(label):
	global lbl
	lbl = label
	l.set_color(label)
	fig.canvas.draw_idle()

def update(val):
	global states, state0, rho, sig, bet, l

	rho = rho_sl.val
	sig = sig_sl.val
	bet = bet_sl.val

	state0 = sx_sl.val, sy_sl.val, sz_sl.val

	title_txt.set_text(title %(sig, sig, rho, rho, bet, bet))

	states = gen_data()

	ax.clear()

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")

	l, = ax.plot(states[:, 0], states[:, 1], states[:, 2])
	l.set_color(lbl)
	fig.canvas.draw_idle()

rho_sl.on_changed(update)
sig_sl.on_changed(update)
bet_sl.on_changed(update)

sx_sl.on_changed(update)
sy_sl.on_changed(update)
sz_sl.on_changed(update)

button.on_clicked(reset)
radio.on_clicked(colorfunc)

plt.show()
