# -*- coding: utf-8 -*-
"""
Created: Brayan Quiceno
License: Grupo de Geofísica y Ciencias de la Computación - GGC3
         Institución Universitaria ITM
         Medellín, Antioquia, Colombia
"""
#%% Libraries
import matplotlib.pyplot as plt
import pygimli as pg

#%% Fonts
bar = {'family': 'serif',
       'color': 'black',
       'weight': 'medium',
       'size': 12}

label = {'family': 'serif',
         'color': 'darkblue',
         'weight': 'normal',
         'size': 14} 

text = {'family': 'Serif',
        'color': 'black',
        'weight': 'normal',
        'size': 12}

#%% Inversion
dataset = pg.physics.ert.load("simple.dat")

ERTManager = pg.physics.ert.ERTManager(dataset, verbose=True)

ERTManager.invert(lam=0.35)
relrms = ERTManager.inv.relrms()
absrms = ERTManager.inv.absrms()

ax, cbar = ERTManager.showResult(orientation="vertical")

ax.set_xlabel("Surface Position [m]", fontdict=label)
ax.set_ylabel("Depth [m]", fontdict=label)

plt.gcf().text(0.135, 0.75, f"Absolute RMS: {round(absrms, 3)}", fontdict=text,
               bbox=dict(facecolor="white", alpha=1))
plt.gcf().text(0.525, 0.75, f"Relative RMS: {round(relrms, 3)}%", fontdict=text,
               bbox=dict(facecolor="white", alpha=1))

cbar.set_label("Resistivity [$\Omega$m]", fontdict=bar)