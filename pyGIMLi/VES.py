import numpy as np

import pygimli as pg
import pygimli.meshtools as mt
from pygimli.physics import ert
# from pygimli.physics.ert import simulate as simulateERT
from pygimli.physics.ert import VESModelling, VESCModelling
# from pygimli.physics.ert import createERTData

data= pg.load('Example_5.dat')

x = pg.x(data)
ab2 = (x[data('b')] - x[data('n')])/4

x = np.array(x[data('b')])
###############################################################################
# Plot results
fig, ax = pg.plt.subplots(1, 1)
ax.plot(ab2, data('rhoa'), '-o', label='1D (VES)')
ax.set_xlabel('BN/4 (m)')
ax.set_ylabel('Apparent resistivity ($\Omega$m)')
ax.grid(1)
ax.legend()
