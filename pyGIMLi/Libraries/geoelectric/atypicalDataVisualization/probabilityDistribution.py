import pygimli as pg
import numpy as np

from geophysics import geoelectric as gelt

fileName = "simple.dat"
dataset = pg.load(fileName)
apparentResistivity = np.array(dataset["rhoa"])
layers = []
layers.append(apparentResistivity[:18])
layers.append(apparentResistivity[18:35])
layers.append(apparentResistivity[35:51])
layers.append(apparentResistivity[51:66])
layers.append(apparentResistivity[66:80])
layers.append(apparentResistivity[80:93])
layers.append(apparentResistivity[93:105])
layers.append(apparentResistivity[105:116])
layers.append(apparentResistivity[116:126])
layers.append(apparentResistivity[126:135])
layers.append(apparentResistivity[135:143])
layers.append(apparentResistivity[143:150])
layers.append(apparentResistivity[150:156])
layers.append(apparentResistivity[156:161])
layers.append(apparentResistivity[161:165])
layers.append(apparentResistivity[165:168])
layers.append(apparentResistivity[168:170])
layers.append(apparentResistivity[170:])
gelt.atypicalDataVisualization.probabilityDistribution(layers)

fileName = "ABEM DD.dat"
layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers, filtering=True)

fileName = "ABEM GDE.dat"
layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers)

fileName = "ABEM SBG.dat"
layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers, filtering=True)

fileName = "ABEM WN.dat"
layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers)