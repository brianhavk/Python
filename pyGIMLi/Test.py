import matplotlib.pyplot as plt
import pybert as pb
import numpy as np
import pygimli as pg

import pygimli.physics.ert as ert

filename = "simple.dat"
dataset = pg.physics.ert.load(filename)

# dataset.save("Unsorted ABEM SBG-1.res2dinv")

# sensorPositions = np.array([[0, 0, 0],
#                             [4.5, 0, 0],
#                             [9.0, 0, 0],
#                             [13.5, 0, 0],
#                             [18.0, 0, 0],
#                             [22.5, 0, 0],
#                             [27.0, 0, 0],
#                             [31.5, 0, 0],
#                             [36.0, 0, 0],
#                             [40.5, 0, 0],
#                             [45.0, 0, 0],
#                             [49.5, 0, 0],
#                             [54.0, 0, 0],
#                             [58.5, 0, 0],
#                             [63.0, 0, 0],
#                             [67.5, 0, 0],
#                             [72.0, 0, 0],
#                             [76.5, 0, 0],
#                             [81.0, 0, 0],
#                             [85.5, 0, 0],
#                             [90.0, 0, 0],
#                             [94.5, 0, 0],
#                             [99.0, 0, 0],
#                             [103.5, 0, 0],
#                             [108.0, 0, 0],
#                             [112.5, 0, 0],
#                             [117.0, 0, 0],
#                             [121.5, 0, 0],
#                             [126.0, 0, 0],
#                             [130.5, 0, 0],
#                             [135.0, 0, 0],
#                             [139.5, 0, 0],
#                             [144.0, 0, 0],
#                             [148.5, 0, 0],
#                             [153.0, 0, 0],
#                             [157.5, 0, 0],
#                             [162.0, 0, 0],
#                             [166.5, 0, 0],
#                             [171.0, 0, 0],
#                             [175.5, 0, 0],
#                             [180.0, 0, 0]])

# dataset.setSensorPositions(sensorPositions)
# pg.show(dataset)

mgr = ert.ERTManager(dataset)
inversion = mgr.invert(paraBoundary=0)
pg.show(dataset, mgr.inv.response)

# mgr = pg.physics.ert.ERTManager(dataset, verbose=True)
# pg.show(dataset)

# kw = dict(cMin=42.82, cMax=104, logScale=True, cMap="Spectral_r")
# # mgr.inv.setRegularization(4, limits=[min(dataset["rhoa"]), max(dataset["rhoa"])], 
# #                           trans="log")
# mgr.invert(quality=34.6, paraMaxCellSize=100)
# mgr.showResult(**kw)


# manager =  pg.physics.ert.ERTManager(sr=False, useBert=True, debug=False, verbose=True)
# inversion = manager.invert(dataset, lam=1, paraDepth=33.8)
# manager.showResult(cMin=min(np.array(dataset['rhoa'])), cMax=max(np.array(dataset['rhoa']))) 