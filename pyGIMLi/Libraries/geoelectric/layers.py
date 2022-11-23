from geophysics import geoelectric as gelt

fileName = "ABEM DD.dat"
layers = gelt.layers(fileName)
print(layers)

fileName = "ABEM DD.dat"
layers = gelt.layers(fileName)
print(layers)

fileName = "ABEM DD.dat"
layers = gelt.layers(fileName)
print(layers)

fileName = "ABEM DD.dat"
layers = gelt.layers(fileName, token="ip")
print(layers)