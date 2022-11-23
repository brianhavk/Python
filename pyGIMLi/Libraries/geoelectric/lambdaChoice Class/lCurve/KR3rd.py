import pygimli as pg
import geoelectric as gelt

data = pg.load("simple.dat")
lv = gelt.lambdaChoice.lCurve.KR3rd(data, 0.24, 0.44, 21)
print("Lambda Value: " ,  lv)
