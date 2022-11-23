import math 
import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM GDE.dat"
dataset = pg.physics.ert.load(fileName)
    
x = pg.x(dataset)
A = np.array(x[dataset("a")])
B = np.array(x[dataset("b")])

depthOfInvestigations = (B-A)*0.19
depthOfInvestigations = list(depthOfInvestigations)
depthOfInvestigations.sort()  

result = []
for item in depthOfInvestigations:
    if item not in result:
        result.append(item)
depthOfInvestigations = result.copy()
depthOfInvestigations.append(depthOfInvestigations[0]*0.3)
depthOfInvestigations.append(depthOfInvestigations[0]*0.5)
depthOfInvestigations.append(depthOfInvestigations[1]*0.3)
depthOfInvestigations.append(depthOfInvestigations[0]*0.7)
depthOfInvestigations.append(depthOfInvestigations[2]*0.3)
depthOfInvestigations.append(depthOfInvestigations[0]*0.9)
depthOfInvestigations.append(depthOfInvestigations[3]*0.3)
depthOfInvestigations.append(depthOfInvestigations[1]*0.7)
depthOfInvestigations.append(depthOfInvestigations[2]*0.5)
depthOfInvestigations.append(depthOfInvestigations[1]*0.9)
depthOfInvestigations.append(depthOfInvestigations[2]*0.7)
depthOfInvestigations.append(depthOfInvestigations[2]*0.9)
depthOfInvestigations.append(depthOfInvestigations[3]*0.7)
depthOfInvestigations.append(depthOfInvestigations[3]*0.9)
depthOfInvestigations.sort()

depthOfInvestigations = np.around(np.array(depthOfInvestigations), 2)  
depthOfInvestigations = np.delete(depthOfInvestigations, [15, 17], axis=0)
  
# """ Percentages of Relative Depth of Investigation """
# A = np.array(dataset["a"])
# B = np.array(dataset["b"])
# M = np.array(dataset["m"])
# N = np.array(dataset["n"])
    
# midPoints = B[:32]/2
# midPoints = list(midPoints)
# midPoints.sort()
# result = []
# for item in midPoints:
#     if item not in result:
#         result.append(item)
# midPoints = np.array(result.copy())
# midPoints = np.around(midPoints, 2)
# hypotenuses = []
# for item in midPoints:
#     hypotenuse = item/math.cos(math.radians(45))
#     hypotenuses.append(hypotenuse)

# surfacePositions = (M+N)/2

# firstLenght = surfacePositions[:4]
# hypotenusesOfFirstLenght = []
# for item in firstLenght:
#     hypotenuse = item/math.cos(math.radians(45))
#     hypotenusesOfFirstLenght.append(hypotenuse)    
# percentagesOfFirstLenght = []
# for item in hypotenusesOfFirstLenght:
#     percentage = (item/hypotenuses[0])*100
#     percentagesOfFirstLenght.append(percentage)

# secondLenght = surfacePositions[8:12]
# hypotenusesOfSecondLenght = []
# for item in secondLenght:
#     hypotenuse = item/math.cos(math.radians(45))
#     hypotenusesOfSecondLenght.append(hypotenuse)    
# percentagesOfSecondLenght = []
# for item in hypotenusesOfSecondLenght:
#     percentage = (item/hypotenuses[1])*100
#     percentagesOfSecondLenght.append(percentage)

# secondLenght = surfacePositions[8:12]
# hypotenusesOfSecondLenght = []
# for item in secondLenght:
#     hypotenuse = item/math.cos(math.radians(45))
#     hypotenusesOfSecondLenght.append(hypotenuse)    
# percentagesOfSecondLenght = []
# for item in hypotenusesOfSecondLenght:
#     percentage = (item/hypotenuses[1])*100
#     percentagesOfSecondLenght.append(percentage)  