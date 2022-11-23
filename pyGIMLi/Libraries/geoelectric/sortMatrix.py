from geophysics import geoelectric as gelt

fileName = "ABEM DD.dat"
dataset, data = gelt.sortMatrix(fileName)
print(data)

fileName = "ABEM GDE.dat"
dataset, data = gelt.sortMatrix(fileName)
print(data)

fileName = "ABEM SBG.dat"
dataset, data = gelt.sortMatrix(fileName)
print(data)

fileName = "ABEM WN.dat"
dataset, data = gelt.sortMatrix(fileName)
print(data)
