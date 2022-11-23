import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

from geophysics import geoelectric as gelt

font_label = {'family': 'serif',
                          'color':  'darkblue',
                          'weight': 'normal',
                          'size': 13,
                          }

fileName = 'Unsorted ABEM SBG.dat'
dataset, data = gelt.sortMatrix(fileName)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
count = 0;
for item in tokens:
    if(item=='err'):
        rmeTokenPosition = count
    if(item=='valid'):
        validTokenPosition = count
    count +=1

layerAverageTwentyoneAndTwentytwo = []
for i in range(6):
    measurements1 = data[507+i, rmeTokenPosition:validTokenPosition]
    measurements2 = data[513+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerAverageTwentyoneAndTwentytwo.append(measurements)   
data[507:513, rmeTokenPosition:validTokenPosition] = layerAverageTwentyoneAndTwentytwo
data = np.delete(data, np.s_[513:519], axis=0)

dataset.resize(316)
pos = 0
for item in tokens:
    dataset[item] = pg.Vector(data[:, pos])
    pos += 1

surfacePosition = data[:, 1] + ((data[:, 0]-data[:, 1])/2)

sensorPositions = np.array(dataset.sensorPositions())
sensorPositions = sensorPositions[:, 0]
dataLenght = len(data)
for i in range(dataLenght):
    for j in range(4):
        data[i, j] = sensorPositions[int(data[i, j])]

depthOfInvestigations = data[:, 1] - data[:, 0]
depthOfInvestigations[:38] = depthOfInvestigations[:38]*0.17 #38-WN
depthOfInvestigations[38:74] = depthOfInvestigations[38:74]*0.19 #36-SBG
depthOfInvestigations[74:109] = depthOfInvestigations[74:109]*0.17 #35-WN
depthOfInvestigations[109:143] = depthOfInvestigations[109:143]*0.19 #34-SBG
depthOfInvestigations[143:175] = depthOfInvestigations[143:175]*0.17 #32-WN
depthOfInvestigations[175:207] = depthOfInvestigations[175:207]*0.19 #32-SBG
depthOfInvestigations[207:238] = depthOfInvestigations[207:238]*0.19 #31-SBG
depthOfInvestigations[238:267] = depthOfInvestigations[238:267]*0.17 #29-WN
depthOfInvestigations[267:293] = depthOfInvestigations[267:293]*0.17 #26-WN
depthOfInvestigations[293:320] = depthOfInvestigations[293:320]*0.19 #27-SBG
depthOfInvestigations[320:346] = depthOfInvestigations[320:346]*0.19 #26-SBG
depthOfInvestigations[346:369] = depthOfInvestigations[346:369]*0.17 #23-WN
depthOfInvestigations[369:392] = depthOfInvestigations[369:392]*0.19 #23-SBG
depthOfInvestigations[392:412] = depthOfInvestigations[392:412]*0.17 #20-WN
depthOfInvestigations[412:433] = depthOfInvestigations[412:433]*0.19 #21-SBG
depthOfInvestigations[433:453] = depthOfInvestigations[433:453]*0.17 #20-WN
depthOfInvestigations[453:] = depthOfInvestigations[453:]*0.19 

measurement = "ip2"
plt.figure(figsize=[8, 4])
plt.scatter(surfacePosition, depthOfInvestigations, s=30, c=np.array(dataset[measurement]),
            cmap='Spectral_r').axes.invert_yaxis()
plt.xlabel('Surface Position [m]', fontdict=font_label)
plt.ylabel('Depth of Investigation [m]', fontdict=font_label)

plt.colorbar(orientation="vertical",
              pad=0.025, shrink=1, aspect=20)