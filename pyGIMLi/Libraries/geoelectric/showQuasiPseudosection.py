import matplotlib.pyplot as plt
import pygimli as pg
from geophysics import geoelectric as gelt

fileName = "ABEM DD.dat"
gelt.showQuasiPseudosection(fileName)

fileName = "ABEM GDE.dat"
gelt.showQuasiPseudosection(fileName)

fileName = "ABEM SBG.dat"
gelt.showQuasiPseudosection(fileName)

fileName = "ABEM WN.dat"
dataset = pg.physics.ert.load(fileName)
gelt.showQuasiPseudosection(fileName, vals=dataset["ip"], 
                                           logScale=False)
