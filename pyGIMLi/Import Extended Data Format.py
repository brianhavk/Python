import numpy as np
import pygimli as pg

fileName = "Extended ABEM DD.txt"
inputFile = open(fileName)
file = inputFile.readlines(); inputFile.close()

width = 47
data = np.zeros((width,))
for i in file:
    j = str(i).split()
    try:
        j = np.asarray(j[:width])
        data = np.vstack((data,j))
    except:
        continue
data = np.delete(data, 0, axis=0)

fileName = "Unsorted ABEM DD.dat"
dataset = pg.physics.ert.load(fileName)
profileSpatialResolution = dataset.size()

tokens = dataset.tokenList().split()
# tokens.remove("SensorIdx:"); tokens.remove("Data:")