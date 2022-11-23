import numpy as np
import pygimli as pg

filename = "Unsorted ABEM DD.dat"
dataset = pg.physics.ert.load(filename)

x = pg.x(dataset)
B = np.array(x[dataset('b')])
N = np.array(x[dataset('n')])

surfacePositionList = np.array(((B-N)/2) + N)