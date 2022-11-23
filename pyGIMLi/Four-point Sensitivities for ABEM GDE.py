import numpy as np
import matplotlib.pyplot as plt
import pygimli as pg
import pygimli.meshtools as mt

from geophysics import geoelectric as gelt
from pygimli.physics import ert

fileName = "Unsorted ABEM GDE.dat"
scheme = pg.physics.ert.load(fileName)

x = pg.x(scheme)
datasetSize = scheme.size()
A = np.array(x[scheme("a")])
B = np.array(x[scheme("b")]) 

world = mt.createWorld(start=[min(A)-12, 0], end=[max(B)+12, -40], worldMarker=True)
for pos in scheme.sensorPositions():
    world.createNode(pos)
mesh = mt.createMesh(world, area=1, quality=33, marker=1)

fop = ert.ERTModelling()
fop.setData(scheme)
fop.setMesh(mesh)

model = np.ones(mesh.cellCount())
fop.createJacobian(model)

i, sens = [], []
for item, complement in enumerate(fop.jacobian()):
    i.append(item)
    sens.append(np.array(complement))
   
for arrangement in range(32):
    fig, ax = plt.subplots(1, 1, sharex=True, figsize=(6,8))
    gelt.plotABMN(ax, scheme, i[arrangement])

    normsens = pg.utils.logDropTol(sens[arrangement]/mesh.cellSizes(), 8e-4)
    normsens /= np.max(normsens)
    ax0, colorbar = pg.show(mesh, normsens, cMap="RdGy_r", ax=ax, orientation="vertical",
            label="Normalized\nsensitivity", nLevs=3, cMin=-1, cMax=1)
    
    if(arrangement < 8):
        scrolling = 3
    if(arrangement>=8 and arrangement<16):
        scrolling = 6
    if(arrangement>=16 and arrangement<24):
        scrolling = 9
    if(arrangement>=24):
        scrolling = 12
    ax0.set_xlim(A[arrangement]-scrolling, B[arrangement]+scrolling)
    ax0.set_ylim(-(B[arrangement]-A[arrangement])*0.19,
                  ((B[arrangement]-A[arrangement])*0.19)*0.7)
    
    fig.tight_layout()
    plt.show()