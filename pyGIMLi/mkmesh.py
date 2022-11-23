#!/usr/bin/env python

import pygimli as pg
import numpy as np
import matplotlib.pyplot as plt

data = pg.DataContainer('simple.dat')

z1 = data.sensorPosition(0)[0]  # z of first electrode
z2 = data.sensorPosition(1)[0]  # z of second electrode
zN = data.sensorPosition(data.sensorCount() - 1)[0]
dz = z2 - z1  # regular spacing with electrode distance
nb = 1     # number of boundary elements
nx2 = 40      # half number of x cells

# position vectors, regular spacing
xx = np.arange(-nx2, nx2) * dz
zz = np.arange(z1 - (nb * dz), zN + (nb * dz), dz)
mesh =  pg.meshtools.createMesh2D(zz, xx, 2)

# append triangles around mesh, show and save it
mesh2 = pg.meshtools.appendTriangleBoundary(mesh, 5., 5., marker=0, isSubSurface=True)
print(mesh)
print(mesh2)
marker2 = mesh2.cellMarker()

fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(8,7))
pg.show(mesh2, ax=ax, data=mesh2.cellMarkers(), linear=True, cMap='Spectral_r', logScale=True)
# ax.set_xlim(-5, 4.6)
# ax.set_ylim(-64, -44.75)


