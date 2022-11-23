import pygimli as pg

fileName = "Unsorted ABEM GDE.dat"
dataset = pg.physics.ert.load(fileName)
pg.show(dataset)