import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM WN.dat"
dataset = pg.physics.ert.load(fileName)

x = pg.x(dataset)
A = np.array(x[dataset("a")])
B = np.array(x[dataset("b")])

depthOfInvestigations = (B-A)*0.17
depthOfInvestigations = list(depthOfInvestigations)
depthOfInvestigations.sort()  

result = []
for item in depthOfInvestigations:
    if item not in result:
        result.append(item)
depthOfInvestigations = np.array(result.copy())

depthOfInvestigations = np.around(depthOfInvestigations, 2)
