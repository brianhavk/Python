import pygimli as pg
import geoelectric as gelt

data = pg.load("resistivity.dat")
lv = gelt.lambdaChoice.lCurve.KR2nd(data, 0.24, 0.44, 21)
print("Lambda Value: " ,  lv)
