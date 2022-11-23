import numpy as np

import pygimli as pg
import pygimli.meshtools as mt
from pygimli.physics import ert
# from pygimli.physics.ert import simulate as simulateERT
from pygimli.physics.ert import VESModelling, VESCModelling
# from pygimli.physics.ert import createERTData

scheme = pg.load('Example_4.dat')

Snrs_Value = np.array(scheme.sensorPositions()); Snrs_Value = Snrs_Value[:,0]

copy = np.zeros((len(scheme['a']), 4))
copy[:,0] = np.array(scheme['a'])
copy[:,1] = np.array(scheme['b'])
copy[:,2] = np.array(scheme['m'])
copy[:,3] = np.array(scheme['n'])

for i in range(len(scheme['a'])):
    for j in range(4):
        copy[i, j] = Snrs_Value[int(copy[i, j])]
scheme['a'] = pg.Vector(copy[:,0])
scheme['b'] = pg.Vector(copy[:,1])
scheme['m'] = pg.Vector(copy[:,2])
scheme['n'] = pg.Vector(copy[:,3])

bn4 = (np.abs(np.array(scheme['b'])) - np.abs(np.array(scheme['a'])))/2

fig, ax = pg.plt.subplots(1, 1)
ax.plot(bn4, scheme('rhoa'), '-o', label='1D (VES)')

ax.set_xlabel('AB/2 (m)')
ax.set_ylabel('Apparent resistivity ($\Omega$m)')
ax.grid(1)
ax.legend()










    
