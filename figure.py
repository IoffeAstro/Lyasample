import matplotlib
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FormatStrFormatter, FixedLocator
import numpy as np
import sys,os
sys.path.append('C:/science/python')
from spectro.utils import cmap_from_color

data = np.genfromtxt('sample.dat', delimiter='\t', names=True, dtype=None)

print(data['z_min'], data['z_max'])

plot_hist = 1
plot_spec = 0
font = 22

if plot_hist:
    z = np.linspace(1.5, 4, 30)
    h = np.zeros_like(z)

    for d in data:
        if 'not used' not in d['comment'].astype('U'):
            mask = (d['z_min'] < z) * (z < d['z_max'])
            h += mask

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.step(z, h, color='dodgerblue', lw=2, where='mid')
    ax.tick_params(axis='both', which='major', labelsize=font-2)
    ax.axis([1.6, 4, 0, 45])
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.set_xlabel('z', fontsize=font)
    ax.set_ylabel('number of spectra', fontsize=font)


if plot_spec:
    fig, ax = plt.subplots(figsize=(6, 8))
    n = 0
    z, inds = [], []
    for i, d in enumerate(data):
        if 'not used' not in d['comment'].astype('U') and 'used' in d['comment'].astype('U'):
            inds.append(i)
            z.append(d['z_min'])
            n += 1
    inds, i = np.asarray(inds), np.argsort(z)
    print(inds[i])
    cmap = cmap_from_color('lightseagreen', c='paleturquoise')
    #cmap = matplotlib.cm.get_cmap('Spectral')
    #print(cmap)
    #print(cmap(0.5))
    for k, d in enumerate(data[inds[i]]):
        print(d['SNR']/np.max(data['SNR']))
        ax.add_patch(Polygon([[d['z_min'], k], [d['z_min'], (k+1)], [d['z_max'], (k+1)], [d['z_max'], k]],
                             closed=True, fill=True, facecolor='lightseagreen',
                             #cmap(d['SNR']/np.max(data['SNR'])),
                             alpha=1, hatch='', lw=1,
                             edgecolor='seagreen'))

    ax.axis([1.55, 3.8, 0, 68])
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.set_xlabel('z', fontsize=font)
    ax.set_ylabel('spectrum', fontsize=font)

    sc = plt.scatter(-data['z_min'], np.ones_like(data['z_min']), c=data['SNR'], cmap=cmap)
    cbar_pos = [0.70, 0.15, 0.02, 0.15]
    cbaxes = fig.add_axes(cbar_pos)
    cbar = plt.colorbar(sc, cax=cbaxes, format="%.1f", ticks=[30, 50, 70])
    cbar.ax.set_xlabel(r'      SNR')

    fig.tight_layout()
    fig.savefig('C:/science/Telikova/Lyasample/spectra_range.pdf')

plt.show()