import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pygimli as pg

from geophysics import geoelectric as gelt

font_title = {'family': 'serif',
              'color':  'darkred',
              'weight': 'normal',
              'size': 13,
              }
font_label = {'family': 'serif',
                          'color':  'darkblue',
                          'weight': 'normal',
                          'size': 13,
                          }
font_bar = {'family': 'serif',
                          'color':  'black',
                          'weight': 'medium',
                          'size': 12,
                          }

fileName = "Unsorted ABEM GDE.dat"
dataset, data = gelt.sortMatrix(fileName)

x = pg.x(dataset)
M = np.array(x[dataset("m")])
N = np.array(x[dataset("n")])
surfacePositions = (M+N)/2

depthOfInvestigations = list(gelt.depthOfInvestigation(dataset))
for i in range(61):
    depthOfInvestigations.append(depthOfInvestigations[0])
for i in range(61):
    depthOfInvestigations.append(depthOfInvestigations[1])
for i in range(41):
    depthOfInvestigations.append(depthOfInvestigations[2])
for i in range(61):
    depthOfInvestigations.append(depthOfInvestigations[3])
for i in range(21):
    depthOfInvestigations.append(depthOfInvestigations[4])
for i in range(61):
    depthOfInvestigations.append(depthOfInvestigations[5])    
for i in range(41):
    depthOfInvestigations.append(depthOfInvestigations[6])
for i in range(1):
    depthOfInvestigations.append(depthOfInvestigations[7])   
for i in range(41):
    depthOfInvestigations.append(depthOfInvestigations[8])
for i in range(21):
    depthOfInvestigations.append(depthOfInvestigations[9])
for i in range(41):
    depthOfInvestigations.append(depthOfInvestigations[10])
for i in range(1):
    depthOfInvestigations.append(depthOfInvestigations[11])
for i in range(21):
    depthOfInvestigations.append(depthOfInvestigations[12])
for i in range(21):
    depthOfInvestigations.append(depthOfInvestigations[13])
for i in range(1):
    depthOfInvestigations.append(depthOfInvestigations[14])
for i in range(1):
    depthOfInvestigations.append(depthOfInvestigations[15])
depthOfInvestigations.sort()

lenghtDataMap = len(dataset.dataMap())
dataLenght = len(data)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
count = 0;
for item in tokens:
    if(item=='err'):
        rmeTokenPosition = count
    if(item=='valid'):
        validTokenPosition = count
    count +=1

### Layer One ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
    if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+1 and data[i, 3] == j+2):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(len(data)):
    if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+8 and data[i, 3] == j+9):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[7:55]
layerOneAverage = []
for i in range(24):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[24+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerOneAverage.append(measurements)

### Layer Two ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+2 and data[i, 3] == j+3):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+7 and data[i, 3] == j+8):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[5:57]
layerTwoAverage = []
for i in range(26):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[26+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerTwoAverage.append(measurements)

### Layer Three ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+2 and data[i, 3] == j+4):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+16 and data[i, 3] == j+18):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[14:28]
layerThreeAverage = []
for i in range(7):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[7+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerThreeAverage.append(measurements)

### Layer Four ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+3 and data[i, 3] == j+4):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+6 and data[i, 3] == j+7):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[3:59]
layerFourAverage = []
for i in range(28):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[28+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerFourAverage.append(measurements)

### Layer Six ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+4 and data[i, 3] == j+5):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+10 and data[i, 2] == j+5 and data[i, 3] == j+6):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[1:61]
layerSixAverage = []
for i in range(30):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[30+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerSixAverage.append(measurements)

complementary = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(len(data)): 
    if(data[i, 0] == j and data[i, 1] == j+30 and data[i, 2] == j+3 and data[i, 3] == j+6):
        j+=1; k+=1
        complementary = np.vstack((complementary, data[i]))
j = 0
for i in range(len(data)): 
    if(data[i, 0] == j and data[i, 1] == j+30 and data[i, 2] == j+24 and data[i, 3] == j+27):
        j+=1; k+=1
        complementary = np.vstack((complementary, data[i]))
complementary = np.delete(complementary, 0, axis=0)

layerSixFiveOneAverage = []
for i in range(31):
    if(i == 0):
        measurements1 = temporal[i, rmeTokenPosition:validTokenPosition]
        measurements2 = complementary[i, rmeTokenPosition:validTokenPosition]
        measurements = (measurements1+measurements2)/2
        layerSixFiveOneAverage.append(measurements)
    if(i>0 and i<11):
        measurements1 = complementary[i, rmeTokenPosition:validTokenPosition]
        measurements2 = layerSixAverage[i-1]
        measurements = (measurements1+measurements2)/2
        layerSixFiveOneAverage.append(measurements)
    if(i >= 11):
        layerSixFiveOneAverage.append(layerSixAverage[i-1])
        
layerSixFiveTwoAverage = []
for i in range(31):
    if(i < 20):
        layerSixFiveTwoAverage.append(layerSixAverage[i])
    if(i>=20 and i<30):
        measurements1 = complementary[i-9, rmeTokenPosition:validTokenPosition]
        measurements2 = layerSixAverage[i]
        measurements = (measurements1+measurements2)/2
        layerSixFiveTwoAverage.append(measurements)
    if(i == 30):
        measurements1 = temporal[i+31, rmeTokenPosition:validTokenPosition]
        measurements2 = complementary[i-9, rmeTokenPosition:validTokenPosition]
        measurements = (measurements1+measurements2)/2
        layerSixFiveTwoAverage.append(measurements)

### Layer Seven ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+4 and data[i, 3] == j+6):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+14 and data[i, 3] == j+16):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[10:32]
layerSevenAverage = []
for i in range(11):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[11+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerSevenAverage.append(measurements)

### Layer Nine ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+6 and data[i, 3] == j+8):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+12 and data[i, 3] == j+14):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[6:36]
layerNineAverage = []
for i in range(15):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[15+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerNineAverage.append(measurements)

### Layer Eleven ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+8 and data[i, 3] == j+10):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+20 and data[i, 2] == j+10 and data[i, 3] == j+12):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[2:40]
layerElevenAverage = []
for i in range(19):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[19+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerElevenAverage.append(measurements)

### Layer Thirteen ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+30 and data[i, 2] == j+9 and data[i, 3] == j+12):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+30 and data[i, 2] == j+18 and data[i, 3] == j+21):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[9:13]
layerThirteenAverage = []
for i in range(2):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[2+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerThirteenAverage.append(measurements)

### Layer Fourteen ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+30 and data[i, 2] == j+12 and data[i, 3] == j+15):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j and data[i, 1] == j+30 and data[i, 2] == j+15 and data[i, 3] == j+18):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
temporal = np.delete(temporal, 0, axis=0)

dataMedia = temporal[3:19]
layerFourteenAverage = []
for i in range(8):
    measurements1 = dataMedia[i, rmeTokenPosition:validTokenPosition]
    measurements2 = dataMedia[8+i, rmeTokenPosition:validTokenPosition]
    measurements = (measurements1+measurements2)/2
    layerFourteenAverage.append(measurements)

data[7:31, rmeTokenPosition:validTokenPosition] = layerOneAverage
data[31:55, rmeTokenPosition:validTokenPosition] = layerOneAverage
data[67:93, rmeTokenPosition:validTokenPosition] = layerTwoAverage
data[93:119, rmeTokenPosition:validTokenPosition] = layerTwoAverage
data[138:145, rmeTokenPosition:validTokenPosition] = layerThreeAverage
data[145:152, rmeTokenPosition:validTokenPosition] = layerThreeAverage
data[169:197, rmeTokenPosition:validTokenPosition] = layerFourAverage
data[197:225, rmeTokenPosition:validTokenPosition] = layerFourAverage
data[250:281, rmeTokenPosition:validTokenPosition] = layerSixFiveOneAverage
data[281:312, rmeTokenPosition:validTokenPosition] = layerSixFiveTwoAverage
data[322:333, rmeTokenPosition:validTokenPosition] = layerSevenAverage
data[333:344, rmeTokenPosition:validTokenPosition] = layerSevenAverage
data[362:377, rmeTokenPosition:validTokenPosition] = layerNineAverage
data[377:392, rmeTokenPosition:validTokenPosition] = layerNineAverage
data[422:441, rmeTokenPosition:validTokenPosition] = layerElevenAverage
data[441:460, rmeTokenPosition:validTokenPosition] = layerElevenAverage
data[473:475, rmeTokenPosition:validTokenPosition] = layerThirteenAverage
data[475:477, rmeTokenPosition:validTokenPosition] = layerThirteenAverage
data[489:497, rmeTokenPosition:validTokenPosition] = layerFourteenAverage
data[497:505, rmeTokenPosition:validTokenPosition] = layerFourteenAverage
pos = 0
for item in tokens:
    dataset[item] = pg.Vector(data[:, pos])
    pos += 1

measurement = "ip"
plt.figure(figsize=[8, 4])
plt.scatter(surfacePositions, depthOfInvestigations, s=30, 
            c=np.array(dataset[measurement]), 
            cmap='Spectral_r').axes.invert_yaxis()
plt.title("Data Distribution of ABEM Gradient Arrangement", fontdict=font_title)
plt.xlabel("Surface Position [m]", fontdict=font_label)
plt.ylabel("Relative Depth of Investigation [m]", fontdict=font_label)

colorbar = plt.colorbar(orientation="vertical",
              pad=0.025, shrink=1, aspect=20)
colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
colorbar.set_label("Apparent Resistivity [$\Omega$m]", fontdict=font_bar)