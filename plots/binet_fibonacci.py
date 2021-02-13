#!/usr/local/bin/python3

'''
Fibonacci Sequence
Complex plot using Binet formula
Graph from a to b, incrament by c
Plot bounds are [lrbt]_b, plot saved to o_f
'''

# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize, LogNorm
from matplotlib import cm
import numpy as np

LOWER_PHI = (1+5**0.5)/2
UPPER_PHI = (1-5**0.5)/2

binet = lambda n: (LOWER_PHI**n - UPPER_PHI**n) / 5**0.5

@plt.FuncFormatter
def scientific(num, pos):
	if not num:
		return r'$+0\cdot10^0$'
	
	order = int(np.log10(num if num > 0 else -num))
	if abs(num) < 10**order:
		order -= 1
	lead  = int(num / 10**order)
	return r'$%+d\cdot10^{%d}$' %(lead, order)

def labeler(ax, xl, yl, zl=None):
	ax.set_xlabel(xl, fontsize=13.5)
	ax.set_ylabel(yl, fontsize=13.5)
	if zl is not None:
		ax.set_zlabel(zl, fontsize=13.5, labelpad=13)

titler = lambda ax, txt: ax.set_title(txt, fontsize=14)

polar_complex = lambda x: (np.arctan2(x.imag, x.real), abs(x))

p = input()

if p == "no":
	a   = float(input())
	b   = float(input())
	c   = float(input())
	o_f =       input()
else:
	a   = float(input(" Start plot at: "))
	b   = float(input("  Stop plot at: "))
	d   = float(input("   Major steps: "))
	c = d/float(input("Ratio to minor: "))
	
	o_f =       input("Output file is: ")

# create figure
fig = plt.figure(figsize=(20, 10))
fig.suptitle(r"""Fibonacci Sequence
$\operatorname{B}(x) = \frac{φ^x-Φ^x}{\sqrt{5}}$""", fontsize=17)

# create subplots
r_line  = fig.add_subplot(241, polar=True)
i_line  = fig.add_subplot(245, polar=True)
r_cross = fig.add_subplot(242)
i_cross = fig.add_subplot(246)
m_full  = fig.add_subplot(222, projection='3d')
r_full  = fig.add_subplot(247, projection='3d')
i_full  = fig.add_subplot(248, projection='3d')
plt.subplots_adjust(.06, .05, .95, .9, .35, .25)
# customize some axis configuarations
i_line .set_rscale('symlog', linthresh=.01)
i_cross.set_yscale('log')
polars = r_line, i_line
[i.grid(linestyle=':') for i in polars]
t_lbl = [r'$2\pi$', r'$\frac{\pi}{3}$', r'$\frac{2\pi}{3}$', r'$\pi$',
		r'$\frac{4\pi}{3}$', r'$\frac{5\pi}{3}$']
[i.set_thetagrids(np.linspace(0,360,6,endpoint=False), t_lbl) for i in polars]
[ax.zaxis.set_major_formatter(scientific) for ax in [r_full, i_full]]
[ax.tick_params(pad=5) for ax in [r_full, i_full]]
im_fmt = plt.FormatStrFormatter('$%di$')
[ax.yaxis.set_major_formatter(im_fmt) for ax in [m_full, r_full, i_full]]

# name subplots
[titler(ax, txt) for ax, txt in [
	(r_line,  "Real Component Parameterized"),
	(i_line,  "Complex Component Parameterized"),
	(r_cross, "Real Component Magnitude"),
	(i_cross, "Complex Component Magnitude"),
	(m_full,  "Magnitude Logarithm"),
	(r_full,  "Real Component"),
	(i_full,  "Complex Component")
]]

# label axes
[labeler(ax,r'$\Re$',r'$\Im$',l) for ax,l in
	[(m_full,r'$\log{(|B|)}$'),(r_full,r'$\Re_B$'),(i_full,r'$\Im_B$')]]
labeler(r_cross, r'$\Re_B$', r'$|B|$')
i_cross.set_xlabel(r'$\Im_B$', fontsize=13.5)
i_cross.set_ylabel(r'$|B|$', fontsize=13.5, labelpad=-5)

[i.set_zlabel(j) for i,j in [(m_full,r'$\log{(|B|)}$'),
	(r_full,r'$\Re_B$'),(i_full,r'$\Im_B$')]]

# calculate data
x = np.arange(a, b, c/16)
y = np.arange(a, b, c/16)

x, y = np.meshgrid(x, y)

full = binet(x + y*1j)
m_f = np.log(abs(full))
m_f = np.maximum(m_f, x/2 + y/8 - 2.5)
r_f = full.real
i_f = full.imag

zline = np.arange(a, b+c/8, c/8, dtype=np.complex)
zdots = np.arange(a, b+c/8, c,   dtype=np.complex)
zdotsk= np.arange(a, b+c/8, d,   dtype=np.complex)

r_l = binet(zline)
i_l = binet(zline*1j)
r_d = binet(zdots)
i_d = binet(zdots*1j)
r_dk= binet(zdotsk)
i_dk= binet(zdotsk*1j)

# set plot color cycle:
# color from red to blue start to end
cm_1 = plt.get_cmap('gist_ncar')
cm_2 = plt.get_cmap('twilight')
c_cycle = [cm_1(2.*i/(len(x)-1)) for i in range(len(x)-1)]
[i.set_prop_cycle('color', c_cycle) for i in [r_line,i_line,r_cross,i_cross]]

# plot data lines
for i in range(len(x)-1):
	r_line .plot(*polar_complex(r_l[i:i+2]), linewidth=2)
	i_line .plot(*polar_complex(i_l[i:i+2]), linewidth=2)
	r_cross.plot(zline.real[i:i+2], abs(r_l)[i:i+2], linewidth=2)
	i_cross.plot(zline.real[i:i+2], abs(i_l)[i:i+2], linewidth=2)

i_cross.set_ylim(.1, max(abs(i_l)))
i_cross.yaxis.set_minor_locator(plt.NullLocator())
r_label_nums = np.linspace (0,max(abs(r_l)),3,endpoint=False)
i_label_nums = np.geomspace(.2,max(abs(i_l)),3,endpoint=False)
i_label_text = [scientific.format_data(i) for i in i_label_nums]
r_line.set_rgrids(r_label_nums, None, 90, '%.2f')
i_line.set_rgrids(i_label_nums, i_label_text, 90)

# plot data points, key points have k appended to var. name
r_line .plot(*polar_complex(r_d),    'r.')
i_line .plot(*polar_complex(i_d),    'r.')
r_line .plot(*polar_complex(r_dk),   'go')
i_line .plot(*polar_complex(i_dk),   'go')
r_cross.plot(zdotsk.real, abs(r_dk), 'go')
i_cross.plot(zdotsk.real, abs(i_dk), 'go')

# add combined colorbar
basic_map = cm.ScalarMappable(norm=Normalize(vmin=a, vmax=b), cmap=cm_1)
pbar = fig.colorbar(basic_map, ax=(r_line,i_line,r_cross,i_cross))
pbar.set_label("Value")

# colormapping by gradient magnitude, g(mri) for gradient of Mag., R, I.
g_grads=[np.gradient(i) for i in [np.exp(m_f), r_f, i_f]]
g_mags=[(i**2+j**2)**.5 for i, j in g_grads]
gm,gr,gi=[cm_2(LogNorm(vmin=i.min(), vmax=i.max())(i)) for i in g_mags]

# specific data
surfaces = [
	(m_full,m_f,gm,.5,r'$\left|\nabla\left(| B |\right)\right|$'),
	(r_full,r_f,gr,1.,r'$\left|\frac{\partial B}{\partial\Re}\right|$'),
	(i_full,i_f,gi,1.,r'$\left|\frac{\partial B}{\partial\Im}\right|$')
]
# argument generators for plot_surface
ar_m = lambda z: (x, y, z)
kw_m = lambda map: {"facecolors":map,"rstride":6,"cstride":6,"cmap":cm_2}
# add colorbars to 3d surfaces
for i, j, k, s, l in surfaces:
	surface = i.plot_surface(*ar_m(j), **kw_m(k))
	
	j_grad_x, j_grad_y = np.gradient(j, c/16)
	j_mag = (j_grad_x**2+j_grad_y**2)**.5
	
	ticks_space = np.linspace(0, 1, 5)
	label_space = np.geomspace(j_mag.min(), j_mag.max(), 5)

	this_b = fig.colorbar(surface, orientation='horizontal', shrink=s,
		ticks=ticks_space, aspect=30, extend='both', ax=i)
	this_b.set_label(l, fontsize=12)

	labels = [scientific.format_data(i) for i in label_space]
	this_b.ax.set_xticklabels(labels)

# display, save, quit, done!
plt.savefig(o_f)
plt.show()
