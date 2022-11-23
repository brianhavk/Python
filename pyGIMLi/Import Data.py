import pybert as pb
import pygimli as pg

fileName = "Extended ABEM DD.txt"
# dataset = pb.importData(fileName)
dataset = pg.load(fileName)
dataset.save("Extended ABEM DD.udf")