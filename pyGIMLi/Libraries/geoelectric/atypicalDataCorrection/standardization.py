import matplotlib.pyplot as plt
import pygimli as pg

from geophysics import geoelectric as gelt

filename = "ABEM DD.dat"
dataset = pg.physics.ert.load(filename)

###############################################################################
###        Quasi-Pseudosection before correction by standardization         ###
###############################################################################
gelt.showQuasiPseudosection(filename)
layers = gelt.layers(filename)
gelt.atypicalDataVisualization.probabilityDistribution(layers, filtering=True)


atypicalData = gelt.atypicalDataCorrection.standardization(filename, token="rhoa")

filename = f"Standardisation {filename}.dat"
dataset = pg.physics.ert.load(filename)
gelt.showQuasiPseudosection(filename)
layers = gelt.layers(filename)

ax1, ax2, = gelt.atypicalDataVisualization.probabilityDistribution(layers[9])
ax1.legend(["Label 10"])

ax1, ax2 = gelt.atypicalDataVisualization.probabilityDistribution(layers[10])
ax1.legend(["Label 11"])