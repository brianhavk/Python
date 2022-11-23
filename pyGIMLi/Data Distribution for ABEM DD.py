import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

from geophysics import geoelectric as gelt

font_label = {'family': 'serif',
                          'color':  'darkblue',
                          'weight': 'normal',
                          'size': 13,
                          }

fileName = "Unsorted ABEM DD.dat"
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
 
layerAverageFiveAndSix = []
for i in range(32):
    measurements1 = data[143+i, rmeTokenPosition:validTokenPosition]
    measurements2 = data[175+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerAverageFiveAndSix.append(measurements)    
data[143:175, rmeTokenPosition:validTokenPosition] = layerAverageFiveAndSix
data = np.delete(data, np.s_[175:207], axis=0)

dataset.resize(316)
pos = 0
for item in tokens:
    dataset[item] = pg.Vector(data[:, pos])
    pos += 1

surfacePosition = data[:, 3]+( (data[:, 1] - data[:, 3])/2 )

sensorPositions = np.array(dataset.sensorPositions())
sensorPositions = sensorPositions[:, 0]
dataLenght = len(data)
for i in range(dataLenght):
    for j in range(4):
        data[i, j] = sensorPositions[int(data[i, j])]
depthOfInvestigations = (data[:, 1] - data[:, 3])*0.25

measurement = "ip"
plt.figure(figsize=[8, 4])
plt.scatter(surfacePosition, depthOfInvestigations, s=50, c=np.array(dataset[measurement]),
            cmap='Spectral_r').axes.invert_yaxis()
plt.xlabel('Surface Position [m]', fontdict=font_label)
plt.ylabel('Depth of Investigation [m]', fontdict=font_label)

plt.colorbar(orientation="vertical",
              pad=0.025, shrink=1, aspect=20)