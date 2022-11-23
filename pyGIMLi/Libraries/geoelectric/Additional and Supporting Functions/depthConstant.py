import pygimli as pg
import geoelectric as gelt
data = pg.load("simple.dat")
dc = gelt.depthConstant(data)
print ("Depth Constant: ",  dc)
