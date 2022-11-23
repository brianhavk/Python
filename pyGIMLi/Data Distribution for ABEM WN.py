import matplotlib.pyplot as plt
import numpy as np

from geophysics import geoelectric as gelt

font_label = {'family': 'serif',
                          'color':  'darkblue',
                          'weight': 'normal',
                          'size': 13,
                          }

fileName = 'Unsorted ABEM WN.dat'
dataset, data = gelt.sortMatrix(fileName)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
count = 0;
for item in tokens:
    if(item=='rhoa'):
        apparentResistivityTokenPosition = count
    count +=1

surfacePosition = data[:, 0]+( (data[:, 1] - data[:, 0])/2 )

sensorPositions = np.array(dataset.sensorPositions())
sensorPositions = sensorPositions[:, 0]
dataLenght = len(data)
for i in range(dataLenght):
    for j in range(4):
        data[i, j] = sensorPositions[int(data[i, j])]
depthOfInvestigations = (data[:, 1] - data[:, 0])*0.17

measurement = "ip"
plt.figure(figsize=[8, 4])
plt.scatter(surfacePosition, depthOfInvestigations, s=50, c=np.array(dataset[measurement]),
            cmap='Spectral_r').axes.invert_yaxis()
plt.xlabel('Surface Position [m]', fontdict=font_label)
plt.ylabel('Depth of Investigation [m]', fontdict=font_label)

plt.colorbar(orientation="vertical",
             pad=0.025, shrink=1, aspect=20)