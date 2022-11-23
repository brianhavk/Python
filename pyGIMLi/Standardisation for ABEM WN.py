import numpy as np
import pygimli as pg

from geophysics import geoelectric as gelt

fileName = "Unsorted ABEM WN.dat"
dataset = pg.physics.ert.load(fileName)
gelt.showQuasiPseudosection(fileName)
layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers)

x = pg.x(dataset)
B = np.array(x[dataset('b')])
A = np.array(x[dataset('a')])

surfacePositionList = np.array(((B-A)/2) + A)
depthOfInvestigationList = np.array((B-A)*gelt.depthConstant(dataset))
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
for layer in layers:
    atypicalData = gelt.atypicalDataDetection.zScore(layer, threshold)
    
    for item, zScore in zip(atypicalData[0], atypicalData[1]):
        print(item, zScore)
        
        for pos in range(profileSpatialResolution):
            if(tokenData[pos] == item):
                mark = pos
        
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
                continue
        
        tokenData[mark] = sum/(count)  
        print(sum/(count))
        break
                            
dataset["rhoa"] = pg.Vector(tokenData)  

fileName = "Standardisation.dat"
dataset.save(fileName)
ax, colorbar = gelt.showQuasiPseudosection(fileName)
ax.set_vlines(x=[30, 40])

layers = gelt.layers(fileName)
gelt.atypicalDataVisualization.probabilityDistribution(layers)    