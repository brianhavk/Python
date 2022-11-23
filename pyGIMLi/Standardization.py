import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

from geophysics import geoelectric as gelt

filename = "Unsorted ABEM DD.dat"
dataset = pg.physics.ert.load(filename)
gelt.showQuasiPseudosection(filename)
plt.show()
layers = gelt.layers(filename)
gelt.atypicalDataVisualization.probabilityDistribution(layers, filtering=True)

surfacePositionList = gelt.surfacePosition(dataset, full=True)
depthOfInvestigationList = gelt.depthOfInvestigation(dataset, full=True)
profileSpatialResolution = dataset.size()

token = "rhoa"
tokenData = np.array(dataset[token])

threshold = 4
layers = gelt.layers(filename)
Surface_Position = []
depth = []
for layer in layers:
    atypicalData = gelt.atypicalDataDetection.zScore(layer, threshold)
    
    for item, zScore in zip(atypicalData[0], atypicalData[1]):
        
        sum=0; count=0
        for pos in range(profileSpatialResolution):
            if(tokenData[pos] == item):
                mark = pos
                
                for newpos in range(profileSpatialResolution):
                    if(depthOfInvestigationList[newpos] == depthOfInvestigationList[mark]):
                        sum = sum + tokenData[newpos]
                        count +=1
                    if(depthOfInvestigationList[newpos] == depthOfInvestigationList[mark] and surfacePositionList[newpos]==surfacePositionList[mark]):
                        sum = sum - tokenData[newpos]
                        count -=1
                tokenData[mark] = sum/count

dataset["rhoa"] = pg.Vector(tokenData)
filename = "Standardisation.dat"
dataset.save(filename)

gelt.showQuasiPseudosection(filename)
plt.show()
layers = gelt.layers(filename)
gelt.atypicalDataVisualization.probabilityDistribution(layers)