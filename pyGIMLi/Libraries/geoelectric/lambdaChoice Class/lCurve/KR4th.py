import pygimli as pg

from geophysics import geoelectric as gelt

data = pg.load("simple.dat")
lv = gelt.lambdaChoice.lCurve.KR4th(data, 0.24, 0.44, 21)
print("Lambda Value: " ,  lv)
