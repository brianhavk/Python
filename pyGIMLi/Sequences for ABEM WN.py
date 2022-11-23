import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM WN.dat"
data = pg.physics.ert.load(fileName)

# x = pg.x(data)
# A = np.array(x[data('a')])
# B = np.array(x[data('b')])
# M = np.array(x[data('m')])
# N = np.array(x[data('n')])

A = np.array(data['a'])
B = np.array(data['b'])
M = np.array(data['m'])
N = np.array(data['n'])

depthOfInvestigations = (B-A)*0.17
depthOfInvestigations = list(depthOfInvestigations)
depthOfInvestigations.sort()

result = []
for item in depthOfInvestigations:
    if item not in result:
        result.append(item)
depthOfInvestigations = np.array(result.copy())

obj = []
electrodePositions = np.transpose(np.vstack((A, B, M, N)))
count = 0
for array in electrodePositions:
    #print((array[1]-array[0])*0.19)
    if(round((array[1]-array[0])*0.17, 2) != 6.12):
        obj.append(count)
    count +=1
layer = np.delete(electrodePositions, obj, axis=0)