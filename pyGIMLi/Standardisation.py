import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

from geophysics import geoelectric as gelt

fileName = "Unsorted ABEM DD.dat"
dataset = pg.physics.ert.load(fileName)
# gelt.showQuasiPseudosection(fileName)
# plt.show()
# layers = gelt.layers(fileName)
# gelt.atypicalDataVisualization.probabilityDistribution(layers)

x = pg.x(dataset)
B = np.array(x[dataset('b')])
N = np.array(x[dataset('n')])

surfacePositionList = np.array(((B-N)/2) + N)
depthOfInvestigationList = np.array((B-N)*gelt.depthConstant(dataset))
depthOfInvestigations = gelt.depthOfInvestigation(dataset)
profileSpatialResolution = dataset.size()
Offset = (np.array(dataset.sensorPositions())[:,0])[1]

surfacePositionList_r = []
for item in surfacePositionList:
    if item not in surfacePositionList_r:
        surfacePositionList_r.append(item)
surfacePositionList_r = np.array(surfacePositionList_r)

Distances = []
for i in range (len(surfacePositionList_r)):
    try:
        distance = np.abs(surfacePositionList_r[i] - surfacePositionList_r[i+1])
        Distances.append(distance)
    except:
        continue 

distances_r = []
for item in Distances:
    if item not in distances_r:
        distances_r.append(item)
distances_r = np.array(distances_r)
distances_r = np.fromiter((element for element in distances_r if element <= Offset), dtype=distances_r.dtype)

token = "rhoa"
tokenData = np.array(dataset[token])

threshold = 3
layers = gelt.layers(fileName)
surfacePosition = []
depth = []
for layer in layers:
    atypicalData = gelt.atypicalDataDetection.zScore(layer, threshold)
    
    for item, zScore in zip(atypicalData[0], atypicalData[1]):
        
        for pos in range(profileSpatialResolution):
            if(tokenData[pos] == item):
                mark = pos
                surfacePosition.append(surfacePositionList[pos])
                depth.append(depthOfInvestigationList[pos])
        
        sum=0; count=0
        # for pos in range(profileSpatialResolution):
        #     try:
        #         if(surfacePositionList[pos]==surfacePositionList[mark-1] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark-1]):
        #             sum = tokenData[pos] + sum
        #             count +=1
        #     except:
        #         continue
            
        # for pos in range(profileSpatialResolution):
        #     try:
        #         if(surfacePositionList[pos]==surfacePositionList[mark] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark-1]):
        #             sum = tokenData[pos] + sum
        #             count +=1
        #     except:
        #         continue
            
        # for pos in range(profileSpatialResolution):
        #     try:
        #         if(surfacePositionList[pos]==surfacePositionList[mark+1] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark-1]):
        #             sum = tokenData[pos] + sum
        #             count +=1
        #     except:
        #         continue
            
        for pos in range(profileSpatialResolution):
            try:
                if(surfacePositionList[pos]==surfacePositionList[mark-1] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark]):
                    sum = tokenData[pos] + sum
                    count +=1
            except:
                continue
        
        if(zScore < 3):
            for pos in range(profileSpatialResolution):
                try:
                    if(surfacePositionList[pos]==surfacePositionList[mark] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark]):
                        sum = tokenData[pos] + sum
                        count +=1
                except:
                    continue
            
        for pos in range(profileSpatialResolution):
            try:
                if(surfacePositionList[pos]==surfacePositionList[mark+1] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark]):
                    sum = tokenData[pos] + sum
                    count +=1
            except:
                continue
            
        # for pos in range(profileSpatialResolution):
        #     try:
        #         if(surfacePositionList[pos]==surfacePositionList[mark-1] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark+1]):
        #             sum = tokenData[pos] + sum
        #             count +=1
        #     except:
        #         continue
            
        # for pos in range(profileSpatialResolution):
        #     try:
        #         if(surfacePositionList[pos]==surfacePositionList[mark] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark+1]):
        #             sum = tokenData[pos] + sum
        #             count +=1
        #     except:
        #         continue
            
        # for pos in range(profileSpatialResolution):
        #     try:
        #         if(surfacePositionList[pos]==surfacePositionList[mark+1] and depthOfInvestigationList[pos]==depthOfInvestigationList[mark+1]):
        #             sum = tokenData[pos] + sum
        #             count +=1
        #     except:
                # continue
        
        tokenData[mark] = sum/(count)  
                            
dataset["rhoa"] = pg.Vector(tokenData)  

fileName = "Standardisation.dat"
dataset.save(fileName)
# ax, colorbar = gelt.showQuasiPseudosection(fileName)
# ax.vlines(x=surfacePosition, ymin=0, ymax=depth, ls='--')
# ax.hlines(y=depth, xmin=0, xmax=max(surfacePositionList), ls='--')
plt.show()

layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers)    