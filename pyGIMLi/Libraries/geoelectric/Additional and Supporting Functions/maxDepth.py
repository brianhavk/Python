import pygimli as pg
import geoelectric as gelt
data = pg.load("simple.dat")
md = gelt.maxDepth(data)
print ("Maximum Depth: ",  md)
