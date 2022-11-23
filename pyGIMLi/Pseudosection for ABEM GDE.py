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
dataset = pg.physics.ert.load(fileName)
inputFile = open(fileName)
file = inputFile.readlines(); inputFile.close()
lenghtDataMap = len(dataset.dataMap())
data = np.zeros((lenghtDataMap,))
for i in file:
    j = str(i).split(sep='	')
    try:
        j = np.asarray(j[:lenghtDataMap],dtype='float64')
        data = np.vstack((data,j))
    except:
        continue
data = np.delete(data, 0, axis=0)

dataLenght = len(data)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")

depthOfInvestigations = gelt.depthOfInvestigation(dataset)

count = 0;
for item in tokens:
    if(item=='err'):
        rmeTokenPosition = count
        
    if(item=='valid'):
        validTokenPosition = count
        
    count +=1

"""Average Stage"""
### Layer One ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+2 and data[i, 3] == j+3):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(len(data)):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+9 and data[i, 3] == j+10):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+3 and data[i, 3] == j+4):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+8 and data[i, 3] == j+9):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+3 and data[i, 3] == j+5):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+17 and data[i, 3] == j+19):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+4 and data[i, 3] == j+5):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+7 and data[i, 3] == j+8):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+6):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+6 and data[i, 3] == j+7):
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

### Layer Seven ###
temporal = np.zeros((lenghtDataMap,))
j=0; k=0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+5 and data[i, 3] == j+7):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+15 and data[i, 3] == j+17):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+7 and data[i, 3] == j+9):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+13 and data[i, 3] == j+15):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+11):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+11 and data[i, 3] == j+13):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+10 and data[i, 3] == j+13):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+19 and data[i, 3] == j+22):
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
      if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+16):
        j+=1; k+=1
        temporal = np.vstack((temporal, data[i]))
j = 0
for i in range(dataLenght): 
      if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+16 and data[i, 3] == j+19):
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

"""            Sorted Stage                   """
sorted = np.zeros((lenghtDataMap,))
dataLenght = len(data)
j=0; k=0
for i in range(dataLenght): #38 (31-1-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+3 and data[i, 3] == j+4):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+2 and data[i, 3] == j+3):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-9
sorted[k-j+1:,2] = sorted[k-j+1:,2]+1
sorted[k-j+1:,3] = sorted[k-j+1:,3]+1
sorted = sorted[:8]; k=7

j = 0
for i in range(len(data)): #38 (31-1-Left) 
  # if(data[i, 0] == j+8 and data[i, 1] == j+9 and data[i, 2] == j+10 and data[i, 3] == j+11):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+9 and data[i, 3] == j+10):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+7
sorted[k-j+1:,1] = sorted[k-j+1:,1]-2
sorted[k-j+1:,2] = sorted[k-j+1:,2]+1
sorted[k-j+1:,3] = sorted[k-j+1:,3]+1 
sorted[8:32, rmeTokenPosition:validTokenPosition] = layerOneAverage

j = 0
for i in range(dataLenght): #36 (31-2-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+5 and data[i, 3] == j+6:
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+3 and data[i, 3] == j+4):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-9
sorted[k-j+1:,2] = sorted[k-j+1:,2]+2
sorted[k-j+1:,3] = sorted[k-j+1:,3]+2
sorted = sorted[0:44]; k=43

j = 0
for i in range(dataLenght): #36 (31-2-Left)
  # if(data[i, 0] == j+6 and data[i, 1] == j+7 and data[i, 2] == j+10 and data[i, 3] == j+11:
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+8 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+5
sorted[k-j+1:,1] = sorted[k-j+1:,1]-4
sorted[k-j+1:,2] = sorted[k-j+1:,2]+2
sorted[k-j+1:,3] = sorted[k-j+1:,3]+2
sorted[44:70, rmeTokenPosition:validTokenPosition] = layerTwoAverage

j = 0
for i in range(len(data)): #35 (21-1-Right)
    # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+6 and data[i, 3] == j+7):
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+3 and data[i, 3] == j+5):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-19
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+2
sorted = sorted[0:89]; k=88

j = 0
for i in range(len(data)): #35 (21-1-Left)
    # if(data[i, 0] == j+15 and data[i, 1] == j+16 and data[i, 2] == j+20 and data[i, 3] == j+21):
      if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+17 and data[i, 3] == j+19):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+14
sorted[k-j+1:,1] = sorted[k-j+1:,1]-5
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+2
sorted[89:96, rmeTokenPosition:validTokenPosition] = layerThreeAverage

j = 0
for i in range(len(data)): #34 (31-3-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+7 and data[i, 3] == j+8):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+4 and data[i, 3] == j+5):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-9
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+3
sorted = sorted[0:113]; k=112

j = 0
for i in range(len(data)): #34 (31-3-Left)
  # if(data[i, 0] == j+4 and data[i, 1] == j+5 and data[i, 2] == j+10 and data[i, 3] == j+11):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+7 and data[i, 3] == j+8):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+3
sorted[k-j+1:,1] = sorted[k-j+1:,1]-6
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+3
sorted[113:141, rmeTokenPosition:validTokenPosition] = layerFourAverage

j = 0
for i in range(len(data)): #32 (11-1-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+9 and data[i, 3] == j+10):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+4 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-29
sorted[k-j+1:,2] = sorted[k-j+1:,2]+5
sorted[k-j+1:,3] = sorted[k-j+1:,3]+3

j = 0
for i in range(len(data)): #32 (11-1-Left) (32 - DD-7-1)
  # if(data[i, 0] == j+22 and data[i, 1] == j+23 and data[i, 2] == j+30 and data[i, 3] == j+31):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+25 and data[i, 3] == j+28):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+21
sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
sorted[k-j+1:,2] = sorted[k-j+1:,2]+5
sorted[k-j+1:,3] = sorted[k-j+1:,3]+3

j = 0
for i in range(len(data)): #32 (31-4-Right) (32 - DD-5-2)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+8 and data[i, 3] == j+10):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+6):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4
sorted = sorted[0:167]; k=166

j = 0
for i in range(len(data)): #32 (31-4-Left)
  # if(data[i, 0] == j+2 and data[i, 1] == j+4 and data[i, 2] == j+9 and data[i, 3] == j+11):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+6 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+1
sorted[k-j+1:,1] = sorted[k-j+1:,1]-7
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4
sorted[167:197, rmeTokenPosition:validTokenPosition] = layerSixAverage

j = 0
for i in range(len(data)): #31 (21-2-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+9 and data[i, 3] == j+11):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+5 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-18
sorted[k-j+1:,2] = sorted[k-j+1:,2]+4
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4
sorted = sorted[0:208]; k=207

j = 0
for i in range(len(data)): #31 (21-2-Left)
  # if(data[i, 0] == j+11 and data[i, 1] == j+13 and data[i, 2] == j+19 and data[i, 3] == j+21):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+15 and data[i, 3] == j+17):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+10
sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
sorted[k-j+1:,2] = sorted[k-j+1:,2]+4
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4
sorted[208:219, rmeTokenPosition:validTokenPosition] = layerSevenAverage

j = 0
for i in range(len(data)): #29 (41-1-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j11 and data[i, 3] == j+13):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+5 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-38
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

j = 0
for i in range(len(data)): #29 (1-1-Left)
  # if(data[i, 0] == j+29 and data[i, 1] == j+31 and data[i, 2] == j+39 and data[i, 3] == j+41):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+33 and data[i, 3] == j+37):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+28
sorted[k-j+1:,1] = sorted[k-j+1:,1]-10
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

j = 0
for i in range(len(data)): #27 (1-3-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+13 and data[i, 3] == j+15):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+7 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-18
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6
sorted = sorted[0:237]; k=236

j = 0
for i in range(len(data)): #27 (21-3-Left)
  # if(data[i, 0] == j+7 and data[i, 1] == j+9 and data[i, 2] == j+19 and data[i, 3] == j+21):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+13 and data[i, 3] == j+15):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+6
sorted[k-j+1:,1] = sorted[k-j+1:,1]-12
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6
sorted[237:252, rmeTokenPosition:validTokenPosition] = layerNineAverage

j = 0
for i in range(len(data)): #26 (11-2-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+14 and data[i, 3] == j+16):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+7 and data[i, 3] == j+10):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-28
sorted[k-j+1:,2] = sorted[k-j+1:,2]+7
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6

j = 0
for i in range(len(data)): #26 (11-2-Left) 
  # if(data[i, 0] == j+16 and data[i, 1] == j+18 and data[i, 2] == j+29 and data[i, 3] == j+31):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+22 and data[i, 3] == j+25):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+15
sorted[k-j+1:,1] = sorted[k-j+1:,1]-13
sorted[k-j+1:,2] = sorted[k-j+1:,2]+7
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6

j = 0
for i in range(len(data)): #23 (21-4-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+17 and data[i, 3] == j+19):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+11):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-18
sorted[k-j+1:,2] = sorted[k-j+1:,2]+8
sorted[k-j+1:,3] = sorted[k-j+1:,3]+8
sorted = sorted[0:282]; k=281

j = 0
for i in range(len(data)): #23 (21-4-Left)
  # if(data[i, 0] == j+3 and data[i, 1] == j+5 and data[i, 2] == j+19 and data[i, 3] == j+21):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+11 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+2
sorted[k-j+1:,1] = sorted[k-j+1:,1]-16
sorted[k-j+1:,2] = sorted[k-j+1:,2]+8
sorted[k-j+1:,3] = sorted[k-j+1:,3]+8
sorted[282:301, rmeTokenPosition:validTokenPosition] = layerElevenAverage

j = 0
for i in range(len(data)): #21 (1-2-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+19 and data[i, 3] == j+21):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+9 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-38
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+8

j = 0
for i in range(len(data)): #21 (1-2-Left)
  # if(data[i, 0] == j+21 and data[i, 1] == j+23 and data[i, 2] == j+39 and data[i, 3] == j+41):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+29 and data[i, 3] == j+33):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+20
sorted[k-j+1:,1] = sorted[k-j+1:,1]-18
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+8

j = 0
for i in range(len(data)): #20 (11-3-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+20 and data[i, 3] == j+22):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+10 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-28
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+9
sorted = sorted[0:314]; k=313

j = 0
for i in range(len(data)): #20 (11-3-Left) 
  # if(data[i, 0] == j+10 and data[i, 1] == j+12 and data[i, 2] == j+29 and data[i, 3] == j+31):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+19 and data[i, 3] == j+22):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+9
sorted[k-j+1:,1] = sorted[k-j+1:,1]-19
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+9
sorted[314:316, rmeTokenPosition:validTokenPosition] = layerThirteenAverage

j = 0
for i in range(len(data)): #14 (11-4-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+26 and data[i, 3] == j+28):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+16):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-28
sorted[k-j+1:,2] = sorted[k-j+1:,2]+13
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12
sorted = sorted[0:328]; k=327

j = 0
for i in range(len(data)): #14 (11-4-Left) 
  # if(data[i, 0] == j+4 and data[i, 1] == j+6 and data[i, 2] == j+29 and data[i, 3] == j+31):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+16 and data[i, 3] == j+19):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+3
sorted[k-j+1:,1] = sorted[k-j+1:,1]-25
sorted[k-j+1:,2] = sorted[k-j+1:,2]+13
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12
sorted[328:336, rmeTokenPosition:validTokenPosition] = layerFourteenAverage

j = 0
for i in range(len(data)): #13 (1-3-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+27 and data[i, 3] == j+29):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+13 and data[i, 3] == j+17):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-38
sorted[k-j+1:,2] = sorted[k-j+1:,2]+14
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12

j = 0
for i in range(len(data)): #13 (1-3-Left)
  # if(data[i, 0] == j+13 and data[i, 1] == j+15 and data[i, 2] == j+39 and data[i, 3] == j+41):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+25 and data[i, 3] == j+29):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+12
sorted[k-j+1:,1] = sorted[k-j+1:,1]-26
sorted[k-j+1:,2] = sorted[k-j+1:,2]+14
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12

j = 0
for i in range(len(data)): #5 (1-4-Right)
  # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+35 and data[i, 3] == j+37):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+17 and data[i, 3] == j+21):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-38
sorted[k-j+1:,2] = sorted[k-j+1:,2]+18
sorted[k-j+1:,3] = sorted[k-j+1:,3]+16

j = 0
for i in range(len(data)): #5 (1-4-Left)
  # if(data[i, 0] == j+5 and data[i, 1] == j+7 and data[i, 2] == j+39 and data[i, 3] == j+41):
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+21 and data[i, 3] == j+25):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0] = sorted[k-j+1:,0]+4
sorted[k-j+1:,1] = sorted[k-j+1:,1]-34
sorted[k-j+1:,2] = sorted[k-j+1:,2]+18
sorted[k-j+1:,3] = sorted[k-j+1:,3]+16

sorted = np.delete(sorted, 0, axis=0)
sorted[:,0] = sorted[:,0]-1
sorted[:,1] = sorted[:,1]-1
sorted[:,2] = sorted[:,2]-1
sorted[:,3] = sorted[:,3]-1

dataset.resize(342)
count = 0
for item in tokens:
    dataset[item] = pg.Vector(sorted[:, count])
    count += 1  

ax, colorbar = pg.show(dataset, orientation="vertical")
colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
colorbar.set_label("Apparent Resistivity [$\Omega$m]", fontdict=font_bar)

depthOfInvestigationLabels = ["%.2f" % i for i in depthOfInvestigations]
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
            depthOfInvestigationLabels,
            fontsize=12)
ax.set_xlabel("Surface Position [m]", fontdict=font_label)
ax.set_ylabel("Depth of Investigation [m]", fontdict=font_label) 
ax.set_title("Quasi-Pseudosection for ABEM Gradient Arrangement", fontdict=font_title)