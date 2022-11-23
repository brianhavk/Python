import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM DD.dat"
dataset = pg.physics.ert.load(fileName)

x = pg.x(dataset)
B = np.array(x[dataset("b")])
N = np.array(x[dataset("n")])

depthOfInvestigations = (B-N)*0.25
depthOfInvestigations = list(depthOfInvestigations)
depthOfInvestigations.sort()  

result = []
for item in depthOfInvestigations:
    if item not in result:
        result.append(item)
depthOfInvestigations = np.array(result.copy())

depthOfInvestigations = np.around(depthOfInvestigations, 2)
