# -*- coding: utf-8 -*-
"""
Functions for pyGIMLi
Created: Brayan A. Quiceno
License: Grupo de Geofísica y Ciencias de la Computación GGC3
         Institución Universitaria ITM
         Medellín, Antioquia, Colombia
"""
#%% Required Libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pybert as pb
import pygimli as pg

from scipy import interpolate

#%% Fonts
font_title = {'family': 'serif',
              'color':  'darkred',
              'weight': 'normal',
              'size': 13,
              }
font_text = {'family': 'serif',
              'color':  'darkgreen',
              'weight': 'normal',
              'size': 14,
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

#%% Startup function, where the essential parameters are calculated
def beginning(filename):
    dataset = pb.importData(filename)
  
    if(np.mean(np.array(dataset["rhoa"])) == 0):
        dataset['r'] = abs(dataset['r'])
        dataset['valid'] = pg.Vector(np.ones(int(dataset.size())))
        dataset['k'] = pg.physics.ert.createGeometricFactors(dataset)
        dataset['rhoa'] = dataset['r']*dataset['k'] 
    else:
        dataset['rhoa'] = abs(dataset['rhoa'])
        dataset['valid'] = pg.Vector(np.ones(int(dataset.size())))
        dataset['k'] = pg.physics.ert.createGeometricFactors(dataset)
    dataset['err'] = pg.physics.ert.estimateError(dataset)

    return dataset

#%% Calculation of depth constant
def depthConstant(dataset):
    x = pg.x(dataset)
    A = np.array(x[dataset('a')])[0]
    B = np.array(x[dataset('b')])[0]
    M = np.array(x[dataset('m')])[0]
    N = np.array(x[dataset('n')])[0]
    
    if(N>M>B>A):  #Convencional Dipolo-Dipolo array
        constant=0.25
    
    if(N<M<A<B):  #Non-convencional Dipolo-Dipolo array
        constant=0.25 
    
    if((N-M)==(M-B)==(B-A)):  #Non-convencional Dipolo-Dipolo array
        constant=0.17
    
    return constant

#%% Depth of investigation list
def depthOfInvestigation(dataset, **kwargs):
    profileSpatialResolution = dataset.size()
    x = pg.x(dataset)
    
    full = False
    for key, value in kwargs.items():
        if(key == "full"):
            full = value
    
    if(profileSpatialResolution == 348):
        B = np.array(x[dataset("b")])
        N = np.array(x[dataset("n")])

        depthOfInvestigations = (B-N)*0.25
        depthOfInvestigations = list(depthOfInvestigations)
        if(full == False):
            depthOfInvestigations.sort()  

            result = []
            for item in depthOfInvestigations:
                if item not in result:
                    result.append(item)
            depthOfInvestigations = np.array(result.copy())
    
    if(profileSpatialResolution == 512):
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
    
    if(profileSpatialResolution == 524):
        A = np.array(x[dataset("a")])
        B = np.array(x[dataset("b")])

        a = np.array(dataset["a"])
        b = np.array(dataset["b"])
        m = np.array(dataset["m"])
        n = np.array(dataset["n"])

        depthOfInvestigations = []
        for i in range(profileSpatialResolution):
            if(a[i]==0 and b[i]==3 and m[i]==1 and n[i]==2):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
                
            if(a[i]==0 and b[i]==6 and m[i]==2 and n[i]==4):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
                
            if(a[i]==0 and b[i]==9 and m[i]==3 and n[i]==6):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
                
            if(a[i]==0 and b[i]==12 and m[i]==4 and n[i]==8):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
                
            if(a[i]==0 and b[i]==15 and m[i]==5 and n[i]==10):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
            
            if(a[i]==0 and b[i]==18 and m[i]==6 and n[i]==12):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
                
            if(a[i]==0 and b[i]==21 and m[i]==7 and n[i]==14):
                depthOfInvestigations.append((B[i]-A[i])*0.17)
                
            if(a[i]==0 and b[i]==5 and m[i]==2 and n[i]==3):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==7 and m[i]==3 and n[i]==4):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==9 and m[i]==4 and n[i]==5):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==10 and m[i]==4 and n[i]==6):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==14 and m[i]==6 and n[i]==8):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==18 and m[i]==8 and n[i]==10):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==15 and m[i]==6 and n[i]==9):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==21 and m[i]==9 and n[i]==12):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==27 and m[i]==12 and n[i]==15):
                depthOfInvestigations.append((B[i]-A[i])*0.19)

            if(a[i]==0 and b[i]==20 and m[i]==8 and n[i]==12):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==28 and m[i]==12 and n[i]==16):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==36 and m[i]==16 and n[i]==20):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==25 and m[i]==10 and n[i]==15):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
               
            if(a[i]==0 and b[i]==35 and m[i]==15 and n[i]==20):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==30 and m[i]==12 and n[i]==18):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
            if(a[i]==0 and b[i]==35 and m[i]==14 and n[i]==21):
                depthOfInvestigations.append((B[i]-A[i])*0.19)
                
        depthOfInvestigations = list(depthOfInvestigations)
        depthOfInvestigations.sort()  
    
    if(profileSpatialResolution == 190):
        A = np.array(x[dataset("a")])
        B = np.array(x[dataset("b")])

        depthOfInvestigations = (B-A)*0.17
        depthOfInvestigations = list(depthOfInvestigations)
        depthOfInvestigations.sort()  

        result = []
        for item in depthOfInvestigations:
            if item not in result:
                result.append(item)
        depthOfInvestigations = np.array(result.copy())
        
    depthOfInvestigations = np.around(depthOfInvestigations, 2)
    
    return depthOfInvestigations

#%% Calcules the numerical derivative
def derivative(y, start, end, N):
    derivative = np.zeros(N)
    dx = (end-start)/(N-1)
    for i in range(N):
        if i==0:
            derivative[i] = (y[i+1]-y[i])/dx
        elif i==N-1:
            derivative[i] = (y[i]-y[i-1])/dx   
        else: 
            derivative[i] = (y[i+1]-y[i-1])/(2*dx)
    
    return derivative

#%% Four-point sensitivities functions
def getABMN(scheme, idx):
    """ Get coordinates of four-point cfg with id `idx` from DataContainerERT
    `scheme`."""
    coords = {}
    for elec in "abmn":
        elec_id = int(scheme(elec)[idx])
        elec_pos = scheme.sensorPosition(elec_id)
        coords[elec] = elec_pos.x(), elec_pos.y()
    return coords

def plotABMN(ax, scheme, idx):
    """ Visualize four-point configuration on given axes. """
    coords = getABMN(scheme, idx)
    for elec in coords:
        x, y = coords[elec]
        if elec in "ab":
            color = "red"
        else:
            color = "blue"
        ax.plot(x, y, marker=".", color=color, ms=10)
        ax.annotate(elec.upper(), xy=(x, y), ha="center", fontsize=10, bbox=dict(
            boxstyle="round", fc=(0.8, 0.8, 0.8), ec=color), xytext=(0, 20),
                    textcoords='offset points', arrowprops=dict(
                        arrowstyle="wedge, tail_width=.5", fc=color, ec=color,
                        patchA=None, alpha=0.75))
        ax.plot(coords["a"][0],)

#%% Values for each layer
def layers(fileName, **kwargs):
    dataset, data = sortMatrix(fileName)
    profileSpatialResolution = dataset.size()

    token = "rhoa"
    for key, value in kwargs.items():
        if(key == "token"):
            token = value

    tokens = dataset.tokenList().split()
    tokens.remove("SensorIdx:"); tokens.remove("Data:")
    counter=0;
    for item in tokens:
        if item==token:
            selectedTokenPosition = counter
        counter+=1

    layers = []
    if(profileSpatialResolution == 171):
        dataset = pg.physics.ert.load(fileName)
        measurement = np.array(dataset[token])
        layers.append(measurement[:18])
        layers.append(measurement[18:35])
        layers.append(measurement[35:51])
        layers.append(measurement[51:66])
        layers.append(measurement[66:80])
        layers.append(measurement[80:93])
        layers.append(measurement[93:105])
        layers.append(measurement[105:116])
        layers.append(measurement[116:126])
        layers.append(measurement[126:135])
        layers.append(measurement[135:143])
        layers.append(measurement[143:150])
        layers.append(measurement[150:156])
        layers.append(measurement[156:161])
        layers.append(measurement[161:165])
        layers.append(measurement[165:168])
        layers.append(measurement[168:170])
        layers.append(measurement[170:])
    
    if(profileSpatialResolution == 348):
        layers.append(data[:38, selectedTokenPosition])
        layers.append(data[38:74, selectedTokenPosition])
        layers.append(data[74:109, selectedTokenPosition])
        layers.append(data[109:143, selectedTokenPosition])
        layers.append(data[143:175, selectedTokenPosition])
        layers.append(data[175:207, selectedTokenPosition])
        layers.append(data[207:238, selectedTokenPosition])
        layers.append(data[238:265, selectedTokenPosition])
        layers.append(data[265:291, selectedTokenPosition])
        layers.append(data[291:314, selectedTokenPosition])
        layers.append(data[314:334, selectedTokenPosition])
        layers.append(data[334:, selectedTokenPosition])

    if(profileSpatialResolution == 512):
        layers.append(data[:62, selectedTokenPosition])
        layers.append(data[62:124, selectedTokenPosition])
        layers.append(data[124:166, selectedTokenPosition])
        layers.append(data[166:228, selectedTokenPosition])
        layers.append(data[228:250, selectedTokenPosition])
        layers.append(data[250:312, selectedTokenPosition])
        layers.append(data[312:354, selectedTokenPosition])
        layers.append(data[354:356, selectedTokenPosition])
        layers.append(data[356:398, selectedTokenPosition])
        layers.append(data[398:420, selectedTokenPosition])
        layers.append(data[420:462, selectedTokenPosition])
        layers.append(data[462:464, selectedTokenPosition])
        layers.append(data[464:486, selectedTokenPosition])
        layers.append(data[486:508, selectedTokenPosition])
        layers.append(data[508:510, selectedTokenPosition])
        layers.append(data[510:, selectedTokenPosition])
        
    if(profileSpatialResolution == 524):
        layers.append(data[:38, selectedTokenPosition])
        layers.append(data[38:74, selectedTokenPosition])
        layers.append(data[74:109, selectedTokenPosition])
        layers.append(data[109:143, selectedTokenPosition])
        layers.append(data[143:175, selectedTokenPosition])
        layers.append(data[175:207, selectedTokenPosition])
        layers.append(data[207:238, selectedTokenPosition])
        layers.append(data[238:267, selectedTokenPosition])
        layers.append(data[267:294, selectedTokenPosition])
        layers.append(data[294:320, selectedTokenPosition])
        layers.append(data[320:346, selectedTokenPosition])
        layers.append(data[346:369, selectedTokenPosition])
        layers.append(data[369:392, selectedTokenPosition])
        layers.append(data[392:413, selectedTokenPosition])
        layers.append(data[413:433, selectedTokenPosition])
        layers.append(data[433:453, selectedTokenPosition])
        layers.append(data[453:469, selectedTokenPosition])
        layers.append(data[469:483, selectedTokenPosition])
        layers.append(data[483:496, selectedTokenPosition])
        layers.append(data[496:507, selectedTokenPosition])
        layers.append(data[507:513, selectedTokenPosition])
        layers.append(data[513:519, selectedTokenPosition])
        layers.append(data[519:, selectedTokenPosition])

    if(profileSpatialResolution == 190):
        layers.append(data[:38, selectedTokenPosition])
        layers.append(data[38:73, selectedTokenPosition])
        layers.append(data[73:105, selectedTokenPosition])
        layers.append(data[105:134, selectedTokenPosition])
        layers.append(data[134:157, selectedTokenPosition])
        layers.append(data[157:174, selectedTokenPosition])
        layers.append(data[174:185, selectedTokenPosition])
        layers.append(data[185:, selectedTokenPosition])

    return layers

#%% Calculation of paraDepth
def maxDepth(dataset):
    x=pg.x(dataset)
    A=np.array(x[dataset('a')])
    B=np.array(x[dataset('b')])
    M=np.array(x[dataset('m')])
    N=np.array(x[dataset('n')])
    
    if(N[0]>M[0]>B[0]>A[0]):  #Convencional Dipolo-Dipolo array
        depth=max(np.array((N-A)*depthConstant(dataset)))
    
    if(N[0]<M[0]<A[0]<B[0]):  #Non-convencional Dipolo-Dipolo array
        depth=max(np.array((B-N)*depthConstant(dataset)))
        
    return depth

#%% Show the data distribution for any value
def showMeasurementDistribution(fileName, **kwargs):
    dataset = pg.physics.ert.load(fileName)
    arrangementHeader = header.arrangement(dataset)
    
    token = "rhoa"
    for key, value in kwargs.items():
        if(key == "token"):
            token = value
    
    measurementHeader = header.measurement(token)
    dataset, data = sortMatrix(fileName)
    profileSpatialResolution = dataset.size()
    
    if(profileSpatialResolution == 348):
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

        surfacePositions = data[:, 3]+( (data[:, 1] - data[:, 3])/2 )

        sensorPositions = np.array(dataset.sensorPositions())
        sensorPositions = sensorPositions[:, 0]
        dataLenght = len(data)
        for i in range(dataLenght):
            for j in range(4):
                data[i, j] = sensorPositions[int(data[i, j])]
        depthOfInvestigations = (data[:, 1] - data[:, 3])*0.25
        size = 50
        
    if(profileSpatialResolution == 512):
        x = pg.x(dataset)
        M = np.array(x[dataset("m")])
        N = np.array(x[dataset("n")])
        surfacePositions = (M+N)/2

        depthOfInvestigations = list(depthOfInvestigation(dataset))
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
        size = 30
        
    if(profileSpatialResolution == 524):
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

        surfacePositions = data[:, 1] + ((data[:, 0]-data[:, 1])/2)

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
        size = 30
        
    if(profileSpatialResolution == 190):
        tokens = dataset.tokenList().split()
        tokens.remove("SensorIdx:"); tokens.remove("Data:")
        count = 0;
        
        surfacePositions = data[:, 0]+( (data[:, 1] - data[:, 0])/2 )

        sensorPositions = np.array(dataset.sensorPositions())
        sensorPositions = sensorPositions[:, 0]
        dataLenght = len(data)
        for i in range(dataLenght):
            for j in range(4):
                data[i, j] = sensorPositions[int(data[i, j])]
        depthOfInvestigations = (data[:, 1] - data[:, 0])*0.17
        size = 50
    
    fig, ax = plt.subplots(figsize=[8, 4])
    plt.scatter(surfacePositions, depthOfInvestigations, s=size, edgecolors="k",
                c=np.array(dataset[token]),
                cmap='Spectral_r').axes.invert_yaxis()
    ax.set_xlabel("Surface Position [m]", fontdict=font_label)
    ax.set_ylabel("Depth of Investigation [m]", fontdict=font_label)

    ax.set_title(f"Measurement Distribution of {arrangementHeader}", fontdict=font_title)
    if(profileSpatialResolution == 512):
        ax.set_ylabel("Relative Depth of Investigation [m]", fontdict=font_label)

    colorbar = plt.colorbar(orientation="vertical",
                  pad=0.025, shrink=1, aspect=20)
    colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    colorbar.set_label(f"{measurementHeader}", fontdict=font_bar)
    
    return ax, colorbar
    
#%% Show the quasi-pseudosection for any value
def showQuasiPseudosection(fileName, **kwargs):
    dataset = pg.physics.ert.load(fileName)
    arrangementHeader = header.arrangement(dataset)
    inputFile = open(fileName)
    file = inputFile.readlines(); inputFile.close()
    lenghtDataMap = len(dataset.dataMap())
    profileSpatialResolution = dataset.size()
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
    
    vals = dataset["rhoa"]
    for key, value in kwargs.items():
        if(key == "vals"):
            vals = value
            
    for item in tokens:
        if(np.array_equal(np.array(dataset[item]), np.array(vals))):
            token = item
    measurementHeader = header.measurement(token) 
     
    depthOfInvestigations = depthOfInvestigation(dataset)
    
    if(profileSpatialResolution == 348):
        sorted = np.zeros((lenghtDataMap,))
        dataLenght = len(data)
        j = 0; k = 0
        for i in range(dataLenght): #38
            if(data[i, 0] == j+3 and data[i, 1] == j+4 and data[i, 2] == j+2 and data[i, 3] == j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #36
            if(data[i,0]==j+5 and data[i,1]==j+6 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #35
          # if(data[i,0]==j+6 and data[i,1]==j+7 and data[i,2]==j+2 and data[i,3]==j+1):
            if(data[i,0]==j+5 and data[i,1]==j+7 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))   
        sorted[k-j+1:,0]=sorted[k-j+1:,0]+1
        sorted[k-j+1:,2]=sorted[k-j+1:,2]-1

        j = 0
        for i in range(dataLenght): #34
            if(data[i,0]==j+7 and data[i,1]==j+8 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #32
          # if(data[i,0]==j+9 and data[i,1]==j+10 and data[i,2]==j+2 and data[i,3]==j+1):
            if(data[i,0]==j+7 and data[i,1]==j+10 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,0]=sorted[k-j+1:,0]+2
        sorted[k-j+1:,2]=sorted[k-j+1:,2]-2

        j = 0
        for i in range(dataLenght): #32
          # if(data[i,0]==j+7 and data[i,1]==j+10 and data[i,2]==j+4 and data[i,3]==j+1):
            if(data[i,0]==j+9 and data[i,1]==j+10 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,0]=sorted[k-j+1:,0]-2
        sorted[k-j+1:,2]=sorted[k-j+1:,2]+2 

        j = 0
        for i in range(dataLenght): #31
          # if(data[i,0]==j+8 and data[i,1]==j+11 and data[i,2]==j+4 and data[i,3]==j+1):
            if(data[i,0]==j+9 and data[i,1]==j+11 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i])) 
        sorted[k-j+1:,0]=sorted[k-j+1:,0]-1
        sorted[k-j+1:,2]=sorted[k-j+1:,2]+1
                 
        j = 0
        for i in range(dataLenght): #27
          # if(data[i,0]==j+12 and data[i,1]==j+15 and data[i,2]==j+4 and data[i,3]==j+1):
            if(data[i,0]==j+13 and data[i,1]==j+15 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,0]=sorted[k-j+1:,0]-1
        sorted[k-j+1:,2]=sorted[k-j+1:,2]+1

        j = 0
        for i in range(dataLenght): #26
            if(data[i,0]==j+13 and data[i,1]==j+16 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))  

        j = 0
        for i in range(dataLenght): #23
          # if(data[i,0]==j+16 and data[i,1]==j+19 and data[i,2]==j+4 and data[i,3]==j+1):
            if(data[i,0]==j+17 and data[i,1]==j+19 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i])) 
        sorted[k-j+1:,0]=sorted[k-j+1:,0]-1
        sorted[k-j+1:,2]=sorted[k-j+1:,2]+1
                
        j = 0
        for i in range(dataLenght): #20
            if(data[i,0]==j+19 and data[i,1]==j+22 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #14
            if(data[i,0]==j+25 and data[i,1]==j+28 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i])) 
                
        sorted = np.delete(sorted, 0, axis=0)
        sorted[:, 0] = sorted[:, 0]-1
        sorted[:, 1] = sorted[:, 1]-1
        sorted[:, 2] = sorted[:, 2]-1
        sorted[:, 3] = sorted[:, 3]-1

        count = 0
        for item in tokens:
            dataset[item] = pg.Vector(sorted[:, count])
            count += 1
    
    if(profileSpatialResolution == 512):
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

    if(profileSpatialResolution == 524):
        sorted = np.zeros((lenghtDataMap,))
        dataLenght = len(data)
        j=0; k=0
        for i in range(dataLenght): #38
            # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+3 and data[i, 3] == j+4):
            if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+2 and data[i, 3] == j+3):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-2
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+1
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+1

        j = 0
        for i in range(dataLenght): #36
            # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+5 and data[i, 3] == j+6):
            if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+3 and data[i, 3] == j+4):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-4
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+2
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+2

        j = 0        
        for i in range(dataLenght): #35
            # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+6 and data[i, 3] == j+7):
            if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+3 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-5
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+2

        j = 0        
        for i in range(dataLenght): #34
            # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+7 and data[i, 3] == j+8):
            if(data[i, 0] == j+1 and data[i, 1] == j+8 and data[i, 2] == j+4 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-6
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+3     
                
        j = 0       
        for i in range(dataLenght): #32-WN
            # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+9 and data[i, 3] == j+10): 
            if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+4 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))        
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+5
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+3

        j = 0        
        for i in range(dataLenght): #32-SBG
            # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+8 and data[i, 3] == j+10):
            if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+5 and data[i, 3] == j+6):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-7
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

        j = 0
        for i in range(dataLenght): #31
            # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+9 and data[i, 3] == j+11):
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+4
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

        j = 0
        for i in range(dataLenght): #29
            # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+11 and data[i, 3] == j+13):
            if(data[i, 0] == j+1 and data[i, 1] == j+13 and data[i, 2] == j+5 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-10
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

        j = 0
        for i in range(dataLenght): #26-WN
            # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+14 and data[i, 3] == j+16):
            if(data[i, 0] == j+1 and data[i, 1] == j+16 and data[i, 2] == j+6 and data[i, 3] == j+11):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-13
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+8
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+5

        j = 0
        for i in range(dataLenght): #27
            # if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+12 and data[i, 3] == j+15):
            if(data[i, 0] == j+1 and data[i, 1] == j+15 and data[i, 2] == j+7 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-11
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+5
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+6

        j = 0
        for i in range(dataLenght): #26-SBG
            # if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+13 and data[i, 3] == j+16):
            if(data[i, 0] == j+1 and data[i, 1] == j+16 and data[i, 2] == j+7 and data[i, 3] == j+10):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))  
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-12
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+6
                
        j = 0
        for i in range(dataLenght): #23-WN
            # if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+16 and data[i, 3] == j+19):
            if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+7 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-15
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+9
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+6
                
        j = 0
        for i in range(dataLenght): #23-SBG
            # if(data[i, 0] == j+1 and data[i, 1] == j+5 and data[i, 2] == j+15 and data[i, 3] == j+19):
            if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+9 and data[i, 3] == j+11):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-14
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+8
         
        j = 0
        for i in range(dataLenght): #20-WN
            # if(data[i, 0] == j+1 and data[i, 1] == j+5 and data[i, 2] == j+18 and data[i, 3] == j+22):
            if(data[i, 0] == j+1 and data[i, 1] == j+22 and data[i, 2] == j+8 and data[i, 3] == j+15):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-17
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+7
               
        j = 0
        for i in range(dataLenght): #21
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+16 and data[i, 3] == j+21):
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-15
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+7
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+8

        j = 0
        for i in range(dataLenght): #20-SBG
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+17 and data[i, 3] == j+22):
            if(data[i, 0] == j+1 and data[i, 1] == j+22 and data[i, 2] == j+10 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-16
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+7
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+9

        j = 0
        for i in range(dataLenght): #16
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+21 and data[i, 3] == j+26):
            if(data[i, 0] == j+1 and data[i, 1] == j+26 and data[i, 2] == j+11 and data[i, 3] == j+16):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-20
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+10

        j = 0
        for i in range(dataLenght): #14
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+23 and data[i, 3] == j+28):
            if(data[i, 0] == j+1 and data[i, 1] == j+28 and data[i, 2] == j+13 and data[i, 3] == j+16):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-22
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+12

        j = 0
        for i in range(dataLenght): #13
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+24 and data[i, 3] == j+29):
            if(data[i, 0] == j+1 and data[i, 1] == j+29 and data[i, 2] == j+13 and data[i, 3] == j+17):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-23
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+11
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+12
                
        j = 0
        for i in range(dataLenght): #11
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+26 and data[i, 3] == j+31):
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+19):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-25
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+13
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+12
                
        j = 0
        for i in range(dataLenght): #6
            # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+31 and data[i, 3] == j+36):
            if(data[i, 0] == j+1 and data[i, 1] == j+36 and data[i, 2] == j+15 and data[i, 3] == j+22):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-30
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+16
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+14

        j = 0
        for i in range(dataLenght): #6
            # if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+30 and data[i, 3] == j+36):
            if(data[i, 0] == j+1 and data[i, 1] == j+36 and data[i, 2] == j+16 and data[i, 3] == j+21):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-29
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+14
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+15
                
        j = 0
        for i in range(dataLenght): #5
            # if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+31 and data[i, 3] == j+37):
            if(data[i, 0] == j+1 and data[i, 1] == j+37 and data[i, 2] == j+17 and data[i, 3] == j+21):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        sorted[k-j+1:,1] = sorted[k-j+1:,1]-30
        sorted[k-j+1:,2] = sorted[k-j+1:,2]+14
        sorted[k-j+1:,3] = sorted[k-j+1:,3]+16

        sorted = np.delete(sorted, 0, axis=0)
        sorted[:,0] = sorted[:,0]-1
        sorted[:,1] = sorted[:,1]-1
        sorted[:,2] = sorted[:,2]-1
        sorted[:,3] = sorted[:,3]-1

        count = 0
        for item in tokens:
            dataset[item] = pg.Vector(sorted[:, count])
            count += 1
    
    
    if(profileSpatialResolution == 190):
        dataset, sorted = sortMatrix(fileName)
       
    fig, ax0 = plt.subplots(1, sharex=True)    
    ax, colorbar = pg.show(dataset, ax=ax0, orientation="vertical", **kwargs)
    colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    colorbar.set_label(f"{measurementHeader}", fontdict=font_bar)
    ax.set_xlabel("Surface Position [m]", fontdict=font_label)
    ax.set_ylabel("Depth of Investigation [m]", fontdict=font_label) 
    ax.set_title(f"Quasi-Pseudosection of {arrangementHeader}", fontdict=font_title)
    
    if(profileSpatialResolution == 348):
        fullDepthOfInvestigations = []
        count = 0
        for item in depthOfInvestigations:
            fullDepthOfInvestigations.append(item)
            if(count == 4):
                fullDepthOfInvestigations.append(item)
            count +=1  
        depthOfInvestigationLabels = ["%.2f" % i for i in fullDepthOfInvestigations]
        ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
                      depthOfInvestigationLabels)
    
    if(profileSpatialResolution == 512):
        depthOfInvestigationLabels = ["%.2f" % i for i in depthOfInvestigations]
        ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                    depthOfInvestigationLabels,
                    fontsize=12)
        ax.set_ylabel("Relative Depth of Investigation [m]", fontdict=font_label) 
    
    if(profileSpatialResolution == 524):
        depthOfInvestigationLabels = ["%.2f" % i for i in depthOfInvestigations]
        ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], 
                    depthOfInvestigationLabels,
                    fontsize=8)
    
    if(profileSpatialResolution == 190):
        depthOfInvestigarionLabels = ["%.2f" % i for i in depthOfInvestigations]
        ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7], 
                    depthOfInvestigarionLabels,
                    fontsize=10)

    return ax, colorbar
    
#%% Updates the dataset after sorting
def sortMatrix(fileName):
    dataset = pg.physics.ert.load(fileName)
    lenghtDataMap = len(dataset.dataMap())
    profileSpatialResolution = dataset.size()
    inputFile = open(fileName)
    file = inputFile.readlines(); inputFile.close()
    data = np.zeros((lenghtDataMap,))
    for i in file:
        j = str(i).split(sep='	')
        try:
            j = np.asarray(j[:lenghtDataMap],dtype='float64')
            data = np.vstack((data,j))
        except:
            continue
    data = np.delete(data, 0, axis=0)

    tokens = dataset.tokenList().split()
    tokens.remove("SensorIdx:"); tokens.remove("Data:")

    sorted = np.zeros((lenghtDataMap,))
    dataLenght = len(data)
    j=0; k=0
    
    if(profileSpatialResolution == 348):
        for i in range(dataLenght): #38
            if(data[i,0]==j+3 and data[i,1]==j+4 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j=0
        for i in range(dataLenght): #36
            if(data[i,0]==j+5 and data[i,1]==j+6 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j=0
        for i in range(dataLenght): #35
            if(data[i,0]==j+5 and data[i,1]==j+7 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))   

        j = 0
        for i in range(dataLenght): #34
            if(data[i,0]==j+7 and data[i,1]==j+8 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #32
            if(data[i,0]==j+7 and data[i,1]==j+10 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #32
            if(data[i,0]==j+9 and data[i,1]==j+10 and data[i,2]==j+2 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
               
        j = 0
        for i in range(dataLenght): #31
            if(data[i,0]==j+9 and data[i,1]==j+11 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i])) 
                 
        j = 0
        for i in range(dataLenght): #27
            if(data[i,0]==j+13 and data[i,1]==j+15 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #26
            if(data[i,0]==j+13 and data[i,1]==j+16 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))  

        j = 0
        for i in range(dataLenght): #23
            if(data[i,0]==j+17 and data[i,1]==j+19 and data[i,2]==j+3 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i])) 
                
        j = 0
        for i in range(dataLenght): #20
            if(data[i,0]==j+19 and data[i,1]==j+22 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #14
            if(data[i,0]==j+25 and data[i,1]==j+28 and data[i,2]==j+4 and data[i,3]==j+1):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
    if(profileSpatialResolution == 512):
        for i in range(dataLenght): #38 (31-1-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+2 and data[i, 3] == j+3):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #38 (31-1-Left) 
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+9 and data[i, 3] == j+10):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i])) 

        j = 0
        for i in range(dataLenght): #36 (31-2-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+3 and data[i, 3] == j+4):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #36 (31-2-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+8 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #35 (21-1-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+3 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #35 (21-1-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+17 and data[i, 3] == j+19):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #34 (31-3-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+4 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #34 (31-3-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+7 and data[i, 3] == j+8):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #32 (11-1-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+4 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #32 (11-1-Left) (32 - DD-7-1)
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+25 and data[i, 3] == j+28):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #32 (31-4-Right) (32 - DD-5-2)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+6):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #32 (31-4-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+6 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #31 (21-2-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+5 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #31 (21-2-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+15 and data[i, 3] == j+17):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #29 (1-1-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+5 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #29 (1-1-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+33 and data[i, 3] == j+37):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #27 (21-3-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+7 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #27 (21-3-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+13 and data[i, 3] == j+15):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #26 (11-2-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+7 and data[i, 3] == j+10):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #26 (11-2-Left) 
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+22 and data[i, 3] == j+25):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #23 (21-4-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+11):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #23 (21-4-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+11 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #21 (1-2-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+9 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #21 (1-2-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+29 and data[i, 3] == j+33):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #20 (11-3-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+10 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #20 (11-3-Left) 
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+19 and data[i, 3] == j+22):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #14 (11-4-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+16):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #14 (11-4-Left) 
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+16 and data[i, 3] == j+19):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #13 (1-3-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+13 and data[i, 3] == j+17):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #13 (1-3-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+25 and data[i, 3] == j+29):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #5 (1-4-Right)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+17 and data[i, 3] == j+21):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(len(data)): #5 (1-4-Left)
            if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+21 and data[i, 3] == j+25):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        
    if(profileSpatialResolution == 524):
        for i in range(dataLenght): #38
            if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+2 and data[i, 3] == j+3):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #36
            if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+3 and data[i, 3] == j+4):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0        
        for i in range(dataLenght): #35
            if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+3 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0        
        for i in range(dataLenght): #34
            if(data[i, 0] == j+1 and data[i, 1] == j+8 and data[i, 2] == j+4 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
          
        j = 0        
        for i in range(dataLenght): #32-WN
            if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+4 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0       
        for i in range(dataLenght): #32-SBG
            if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+5 and data[i, 3] == j+6):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))        

        j = 0
        for i in range(dataLenght): #31
            if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #29
            if(data[i, 0] == j+1 and data[i, 1] == j+13 and data[i, 2] == j+5 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #26-WN
            if(data[i, 0] == j+1 and data[i, 1] == j+16 and data[i, 2] == j+6 and data[i, 3] == j+11):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #27
            if(data[i, 0] == j+1 and data[i, 1] == j+15 and data[i, 2] == j+7 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #26-SBG
            if(data[i, 0] == j+1 and data[i, 1] == j+16 and data[i, 2] == j+7 and data[i, 3] == j+10):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))  
                
        j = 0
        for i in range(dataLenght): #23-WN
            if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+7 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #23-SBG
            if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+9 and data[i, 3] == j+11):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #20-WN
            if(data[i, 0] == j+1 and data[i, 1] == j+22 and data[i, 2] == j+8 and data[i, 3] == j+15):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #21
            if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #20-SBG
            if(data[i, 0] == j+1 and data[i, 1] == j+22 and data[i, 2] == j+10 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #16
            if(data[i, 0] == j+1 and data[i, 1] == j+26 and data[i, 2] == j+11 and data[i, 3] == j+16):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #14
            if(data[i, 0] == j+1 and data[i, 1] == j+28 and data[i, 2] == j+13 and data[i, 3] == j+16):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #13
            if(data[i, 0] == j+1 and data[i, 1] == j+29 and data[i, 2] == j+13 and data[i, 3] == j+17):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #11
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+19):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #6
            if(data[i, 0] == j+1 and data[i, 1] == j+36 and data[i, 2] == j+15 and data[i, 3] == j+22):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #6
            if(data[i, 0] == j+1 and data[i, 1] == j+36 and data[i, 2] == j+16 and data[i, 3] == j+21):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
        j = 0
        for i in range(dataLenght): #5
            if(data[i, 0] == j+1 and data[i, 1] == j+37 and data[i, 2] == j+17 and data[i, 3] == j+21):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
                
    if(profileSpatialResolution == 190):
        for i in range(dataLenght): #38
            if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+2 and data[i, 3] == j+3):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #35
            if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+3 and data[i, 3] == j+5):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0        
        for i in range(dataLenght): #32
            if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+4 and data[i, 3] == j+7):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0        
        for i in range(dataLenght): #29
            if(data[i, 0] == j+1 and data[i, 1] == j+13 and data[i, 2] == j+5 and data[i, 3] == j+9):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))    
                
        j = 0       
        for i in range(dataLenght): #23
            if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+7 and data[i, 3] == j+13):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))        

        j = 0        
        for i in range(dataLenght): #17
            if(data[i, 0] == j+1 and data[i, 1] == j+25 and data[i, 2] == j+9 and data[i, 3] == j+17):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #11
            if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+11 and data[i, 3] == j+21):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))

        j = 0
        for i in range(dataLenght): #6
            if(data[i, 0] == j+1 and data[i, 1] == j+37 and data[i, 2] == j+13 and data[i, 3] == j+25):
                j+=1; k+=1
                sorted = np.vstack((sorted, data[i]))
        
    sorted = np.delete(sorted, 0, axis=0)
    sorted[:, 0] = sorted[:, 0]-1
    sorted[:, 1] = sorted[:, 1]-1
    sorted[:, 2] = sorted[:, 2]-1
    sorted[:, 3] = sorted[:, 3]-1

    count = 0
    for item in tokens:
        dataset[item] = pg.Vector(sorted[:, count])
        count += 1
    
    return dataset, sorted

#%% Surface position function
def surfacePosition(dataset, **kwargs):
    full = False
    for key, value in kwargs.items():
        if(key == "full"):
            full = value

    profileSpatialResolution = dataset.size()

    x = pg.x(dataset)
    A = np.array(x[dataset('a')])
    B = np.array(x[dataset('b')])
    N = np.array(x[dataset('n')])
    
    if(profileSpatialResolution == 348):
        surfacePosition = np.array(((B-N)/2) + N)
    
    if(full == False):
        surfacePosition.sort()  

        result = []
        for item in surfacePosition:
            if item not in result:
                result.append(item)
        surfacePosition = np.array(result.copy())
    
    return surfacePosition

#%% Atypical data functions
class atypicalDataVisualization:
    def boxplot(fileName, **kwargs):
        token = "rhoa"
        byLayers = False
        for key, value in kwargs.items():
            if(key == "token"):
                token = value
            if(key == "byLayers"):
                byLayers = value
        
        dataset = pg.physics.ert.load(fileName)
        arrangementHeader = header.arrangement(dataset)
        measurementHeader = header.measurement(token)
        
        if(byLayers == False):
            plt.title(f"Boxplot of {arrangementHeader} Data", fontdict=font_title)
            plt.xlabel("Set", fontdict=font_label)
            plt.boxplot(np.array(dataset[token]))  
        else:
            layerS = layers(fileName, token=token)
            plt.title(f"Boxplot for Each Layer of {arrangementHeader}", fontdict=font_title)
            plt.xlabel("Layer", fontdict=font_label)
            plt.boxplot(layerS)
            
        plt.ylabel(f"{measurementHeader}", fontdict=font_label)
        plt.show()
        
    def probabilityDistribution(layers, **kwargs):
        title = "Profile Standard Deviations"
        if(str(type(layers)) != "<class 'list'>"):
            layer = []
            layer.append(layers)
            layers = layer.copy()
            title = "Layer Standard Deviations"
            
        filtering = False
        for key, value in kwargs.items():
            if(key == "filtering"):
                filtering = value
        
        fig1, ax1 = plt.subplots()
        counter = 0
        count0, count1, count2, count3, count4 = 0, 0, 0, 0, 0
        count5, count6, count7, count8 = 0, 0, 0, 0        
        for array in layers:
            counter +=1
            mean = np.mean(array)
            standardDesviation = np.std(array)
            probabilityDensity = ( 1/(standardDesviation*np.sqrt(2*np.pi)) ) * np.exp( (-1/2)*((array-mean)/standardDesviation)**2)

            sortedIndex = np.argsort(array)
            sortedArray = array[sortedIndex]
            sortedProbabilityDensity = probabilityDensity[sortedIndex]

            zScores = (sortedArray-mean)/standardDesviation
            anomalyDataArray = []
            anomalyDataProbabilityDensity = []
            count = 0
            for item in zScores:
                if(item>=4.0 or item<=-4.0):
                    anomalyDataArray.append(sortedArray[count])
                    anomalyDataProbabilityDensity.append(sortedProbabilityDensity[count])
                count += 1   
                
                if(item<=-4):
                    count0 +=1
                if(item>-4 and item<=-3):
                    count1 +=1
                if(item>-3 and item<=-2):
                    count2 +=1
                if(item>-2 and item<=-1):
                    count3 +=1
                if(item>-1 and item<1):
                    count4 +=1  
                if(item>=1 and item<2):
                    count5 +=1
                if(item>=2 and item<3):
                    count6 +=1
                if(item>=3 and item<4):
                    count7 +=1
                if(item>=4):
                    count8 +=1
      
            if(len(anomalyDataArray)==0 and filtering==True):
                continue
            
            try:
                interpolationSpline = interpolate.make_interp_spline(sortedArray, sortedProbabilityDensity)
                sortedArray = np.linspace(min(sortedArray), max(sortedArray), int(len(array))*10)
                sortedProbabilityDensity = interpolationSpline(sortedArray)

                ax1.plot(sortedArray, sortedProbabilityDensity, 
                         linestyle="dashed", label=f"Layer {counter}")
            except:
                try:
                    interpolatedProbabilityDensity = interpolate.interp1d(sortedArray, sortedProbabilityDensity)
                    sortedArray = np.linspace(min(sortedArray), max(sortedArray), int(len(array))*10)
                    
                    ax1.plot(interpolatedProbabilityDensity(sortedArray), 
                             linestyle="dashed", label=f"Layer {counter}")
                except:
                    ax1.plot(sortedArray, sortedProbabilityDensity, 
                             linestyle="dashed", label=f"Layer {counter}")
            try:
                ax1.scatter(anomalyDataArray, anomalyDataProbabilityDensity, s=20)
            except:
                continue
        try:
            ax1.set_xlabel("Apparent Resistivity", fontdict=font_label)
            ax1.set_ylabel("Probability Density", fontdict=font_label)
            ax1.set_title("Probability Distribution for Each Layer", fontdict=font_title)
            ax1.legend(ncol = 2)
            ax1.tight_layout()
        except:
            pass
                
        if(filtering==True):
            try:
                ax1.set_title("Probability Distribution of Layers with Atipical Data", fontdict=font_title)
            except:
                pass
        
        standardDesviationList = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        zScoreCount = [count0, count1, count2, count3, count4, 
                       count5, count6, count7, count8]
        fig2, ax2 = plt.subplots()
        ax2.set_xlabel("Apparent Resistivity Standard Desviations", fontdict=font_label)
        ax2.set_ylabel("Quantity", fontdict=font_label)   
        ax2.set_title(title, fontdict=font_title)
        bars = ax2.bar(standardDesviationList, zScoreCount, width=0.5, 
                       color=plt.get_cmap("tab20c").colors)
        ax2.bar_label(bars)
        plt.xticks(standardDesviationList)
        plt.tight_layout()
        plt.show()
        
        try:
            return ax1, ax2
        except:
            return ax2

class atypicalDataDetection:
    def zScore(data, threshold):
        mean = np.mean(data)
        std = np.std(data)
        
        atypicalData = []
        zScoreList = []
        for i in data:
            zScore = abs((i - mean)/std)
            if(np.abs(zScore) >= threshold):
                atypicalData.append(i) 
                zScoreList.append(zScore)
                
        return atypicalData, zScoreList

class atypicalDataCorrection:
    def standardization(filename, **kwargs):
        token = "rhoa"
        for key, value in kwargs.items():
            if(key == "token"):
                token = value
        
        dataset = pg.physics.ert.load(filename)
        surfacePositionList = surfacePosition(dataset, full=True)
        depthOfInvestigationList = depthOfInvestigation(dataset, full=True)
        profileSpatialResolution = dataset.size()

        tokenData = np.array(dataset[token])

        threshold = 4
        Layers = layers(filename)
        for layer in Layers:
            atypicalData = atypicalDataDetection.zScore(layer, threshold)
            
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
        filename = f"Standardisation {filename}.dat"
        dataset.save(filename)
        
        return atypicalData
#%%
def ZScore(data):
    mean = np.mean(data)
    std = np.std(data)
    
    zScoreList = []
    for item in data:
        standardScore = abs((item - mean)/std)
        zScoreList.append(standardScore) 
        
    return zScoreList
    
#%% Functions to detect and correct outliers

#     def alpha(data):
#         x = pg.x(data)
#         B = np.array(x[data('b')])
#         N = np.array(x[data('n')])
#         AppR = np.array(data['rhoa'])
#         Pos = np.array(((B-N)/2) + N)
#         Depth = np.array((B-N)*depthConstant(data))
#         Lenght=int(data.size())
#         Offset = (np.array(data.sensorPositions())[:,0])[1]

#         depth_r = []
#         for item in Depth:
#             if item not in depth_r:
#                 depth_r.append(item)
#         depth_r = np.array(depth_r)

#         pos_r = []
#         for item in Pos:
#             if item not in pos_r:
#                 pos_r.append(item)
#         pos_r = np.array(pos_r)

#         Distances = []
#         for i in range (len(pos_r)):
#             try:
#                 distance = np.abs(pos_r[i] - pos_r[i+1])
#                 Distances.append(distance)
#             except:
#                 continue 

#         distances_r = []
#         for item in Distances:
#             if item not in distances_r:
#                 distances_r.append(item)
#         distances_r = np.array(distances_r)
#         distances_r = np.fromiter((element for element in distances_r if element <= Offset), dtype=distances_r.dtype)

#         container = []
#         flag = 0
#         for item in depth_r:
#             for i in range( Lenght ):
#                 if ( Depth[i]==item ):
#                     container.append(AppR[i])
#             extension = np.array(container[flag:len(container)])
            
#             mean = np.mean(extension)
#             std = np.std(extension)
            
#             for i in extension:
#                 standardScore = abs((i - mean)/std)
#                 if ( np.abs(standardScore) > 4 ):
#                     atypicalDataAlpha.append(i) 
            
#             flag = len(container) 

#         for item in atypicalDataAlpha:
#             Sap=0; Cou=0
#             for i in range(Lenght):
#                 if (AppR[i]==item):
                    
#                     depth_e = (B[i]-N[i])*depthConstant(data)
#                     for p in range(len(depth_r)):
#                         if(depth_r[p] == depth_e):
#                             l = p

#                     for j in range(Lenght):
#                         try:
#                             if (Pos[j]==(Pos[i]) and Depth[j]==depth_r[l-1]):
#                                 Sap = AppR[j] + Sap
#                                 Cou = 1 + Cou
#                         except:
#                             continue
                            
#                     for j in range(Lenght):
#                         try:
#                             if (Pos[j]==(Pos[i]) and Depth[j]==depth_r[l+1]):
#                                 Sap = AppR[j] + Sap
#                                 Cou = 1 + Cou
#                         except:
#                             continue
                    
#                     for item in distances_r:
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]-item) and Depth[j]==depth_r[l]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou 
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]+item) and Depth[j]==depth_r[l]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou 
#                             except:
#                                 continue
                        
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]-item) and Depth[j]==depth_r[l-1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]+item) and Depth[j]==depth_r[l-1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]-item) and Depth[j]==depth_r[l+1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]+item) and Depth[j]==depth_r[l+1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue

#                     AppR[i] = (Sap)/(Cou)  
#                     break
        
#         data['rhoa'] = pg.Vector(AppR)    
#         return data
    
    
#     def beta(data):
#         x = pg.x(data)
#         B = np.array(x[data('b')])
#         N = np.array(x[data('n')])
#         AppR = np.array(data['rhoa'])
#         Pos = np.array(((B-N)/2) + N)
#         Depth = np.array((B-N)*depthConstant(data))
#         Lenght=int(data.size())
#         Offset = (np.array(data.sensorPositions())[:,0])[1]

#         depth_r = []
#         for item in Depth:
#             if item not in depth_r:
#                 depth_r.append(item)
#         depth_r = np.array(depth_r)

#         pos_r = []
#         for item in Pos:
#             if item not in pos_r:
#                 pos_r.append(item)
#         pos_r = np.array(pos_r)

#         Distances = []
#         for i in range (len(pos_r)):
#             try:
#                 distance = np.abs(pos_r[i] - pos_r[i+1])
#                 Distances.append(distance)
#             except:
#                 continue 

#         distances_r = []
#         for item in Distances:
#             if item not in distances_r:
#                 distances_r.append(item)
#         distances_r = np.array(distances_r)
#         distances_r = np.fromiter((element for element in distances_r if element <= Offset), dtype=distances_r.dtype)

#         container = []
#         flag = 0
#         for item in depth_r:
#             for i in range( Lenght ):
#                 if ( Depth[i]==item ):
#                     container.append(AppR[i])
#             extension = np.array(container[flag:len(container)])
            
#             mean = np.mean(extension)
#             std = np.std(extension)
            
#             for i in extension:
#                 standardScore = abs((i - mean)/std)
#                 if ( np.abs(standardScore) > 3.5 ):
#                     atypicalDataBeta.append(i) 
            
#             flag = len(container) 

#         for item in atypicalDataBeta:
#             Sap=0; Cou=0
#             for i in range(Lenght):
#                 if (AppR[i]==item):
                    
#                     depth_e = (B[i]-N[i])*depthConstant(data)
#                     for p in range(len(depth_r)):
#                         if(depth_r[p] == depth_e):
#                             l = p

#                     for j in range(Lenght):
#                         try:
#                             if (Pos[j]==(Pos[i]) and Depth[j]==depth_r[l-1]):
#                                 Sap = AppR[j] + Sap
#                                 Cou = 1 + Cou
#                         except:
#                             continue
                            
#                     for j in range(Lenght):
#                         try:
#                             if (Pos[j]==(Pos[i]) and Depth[j]==depth_r[l+1]):
#                                 Sap = AppR[j] + Sap
#                                 Cou = 1 + Cou
#                         except:
#                             continue
                    
#                     for item in distances_r:
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]-item) and Depth[j]==depth_r[l]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou 
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]+item) and Depth[j]==depth_r[l]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou 
#                             except:
#                                 continue
                        
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]-item) and Depth[j]==depth_r[l-1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]+item) and Depth[j]==depth_r[l-1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]-item) and Depth[j]==depth_r[l+1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue
                                
#                         for j in range(Lenght):
#                             try:
#                                 if (Pos[j]==(Pos[i]+item) and Depth[j]==depth_r[l+1]):
#                                     Sap = AppR[j] + Sap
#                                     Cou = 1 + Cou
#                             except:
#                                 continue

#                     AppR[i] = (Sap+AppR[i])/(Cou+1)  
#                     break
        
#         data['rhoa'] = pg.Vector(AppR)    
#         return data
    
#%% Determinate the name of the arrengement
class header:
    def arrangement(dataset):
        profileSpatialResolution = dataset.size()
        
        if(profileSpatialResolution == 171):
            header = "Simple Example"

        if(profileSpatialResolution == 348):
            header = "ABEM Dipole-Dipole Arrangement"
            
        if(profileSpatialResolution == 512):
            header = "ABEM Gradient Arrangement"

        if(profileSpatialResolution == 524):
            header = "ABEM Schlumberger Arrangement"
            
        if(profileSpatialResolution == 190):
            header = "ABEM Wenner Arrangement"

        return header
    
    def measurement(token):
        if(token == "err"):
            header = "Relative Measurement Error [%\100]"
        if(token == 'i'):
            header = "Current [mA]"
        if(token[0]=='i' and token[1]=='p'):
            header = "Chargeability [mV/V]"
        if(token == "iperr"):
            token = "Absolute IP Measure Error [mA]"
        if(token == 'k'):
            header = "Geometric Factor [m]"
        if(token == 'r'):
            header = "Resistance [$\Omega$]"
        if(token == "rhoa"):
            header = "Apparent Resistivity [$\Omega$m]"
        if(token == 'u'):
            header = "Voltaje [V]"
        
        return header
             
#%% 
class lambdaChoice:
    class lCurve:
        def KR1st(data, start, end, N, **kwargs):
            mgr = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=False)
            p = []
            n = []
            chi2 = []

            lambdas = np.linspace(start, end, N)
            for lam in lambdas:
                mgr.invert(lam=lam, **kwargs)
                
                n.append(mgr.inv.phiModel())   
                p.append(mgr.inv.phiData())
                chi2.append((mgr.inv.chi2History)[-1])

            n = np.array(n)
            p = np.array(p)
            dn = derivative(n, start, end, N)
            l = p/(lambdas*n)
            ls = l**2

            r = ( (n/(lambdas*abs(dn))) * (ls/((ls+1)**1.5)) ) - ((l+ls)/((ls+1)**1.5)) 

            K = np.log(p)
            X = np.log(n)
            right = max(r)
            for i in range(N):
                if r[i]==right:
                    score = i

            Optimun_Lambda = str(round(lambdas[score], 3))

            plt.figure() 
            plt.plot(K, X, 'darkblue', linewidth=3)
            plt.title('L-curve', fontdict=font_title)
            plt.axhline(X[score], color="black", linestyle="--")
            plt.axvline(K[score], color="black", linestyle="--")
            plt.xlabel('Residual Norm', fontdict=font_label)
            plt.ylabel('Solution Norm', fontdict=font_label)

            plt.figure()
            plt.plot(lambdas, r, 'darkorange', linewidth=3) 
            plt.title('Expected Curvature', fontdict=font_title)
            plt.text(lambdas[score], r[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
            plt.xlabel(r'Lambda $\lambda$', fontdict=font_label)
            plt.ylabel(r'Curvature $\gamma$', fontdict=font_label)
            plt.grid()
            
            return lambdas[score], chi2
        
        
        def KR2nd(data, start, end, N, **kwargs):
            mgr = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=False)
            p = []
            n = []
            chi2 = []

            lambdas = np.linspace(start, end, N)
            for lam in lambdas:
                mgr.invert(lam=lam, **kwargs)
                
                n.append(mgr.inv.phiModel())   
                p.append(mgr.inv.phiData())
                chi2.append((mgr.inv.chi2History)[-1])

            n = np.array(n)
            p = np.array(p)
            dn = derivative(n, start, end, N)
            ps = p**2
            ns = n**2
            lambdas_s = lambdas**2 


            r = ( (n*p)/np.abs(dn) ) * ( (n*p)+(lambdas*dn*p)+(lambdas_s*dn*n)
                                        /
                                         (ps+(lambdas_s*ns))**(3/2) ) 

            K = np.log(p)
            X = np.log(n)
            right = max(r)
            for i in range(N):
                if r[i]==right:
                    score = i

            Optimun_Lambda = str(round(lambdas[score], 3))  

            plt.figure() 
            plt.plot(K, X, 'darkblue', linewidth=3)
            plt.title('L-curve', fontdict=font_title)
            plt.axhline(X[score], color="black", linestyle="--")
            plt.axvline(K[score], color="black", linestyle="--")
            plt.xlabel('Residual Norm', fontdict=font_label)
            plt.ylabel('Solution Norm', fontdict=font_label)

            plt.figure()
            plt.plot(lambdas, r, 'darkorange', linewidth=3) 
            plt.title('Expected Curvature', fontdict=font_title)
            plt.text(lambdas[score], r[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
            plt.xlabel(r'Lambda $\lambda$', fontdict=font_label)
            plt.ylabel(r'Curvature $\gamma$', fontdict=font_label)
            plt.grid()
            
            return lambdas[score], chi2
        
        
        def KR3rd(data, start, end, N, **kwargs):
            mgr = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=False)
            p = []
            n = []
            chi2 = []
            
            lambdas = np.linspace(start, end, N)
            for lam in lambdas:
                mgr.invert(lam=lam, **kwargs)
                
                n.append(mgr.inv.phiModel())   
                p.append(mgr.inv.phiData())
                chi2.append((mgr.inv.chi2History)[-1])

            n = np.array(n)
            p = np.array(p)
            dn = derivative(n, start, end, N)
            ddn = derivative(dn, start, end, N)
            dp = derivative(p, start, end, N)
            ddp = derivative(dp, start, end, N)
            ns = n**2
            ps = p**2
            dns = dn**2
            dps = dp**2

            r = ( p*n / ((dps*ns+ps*dns)**1.5) ) * (ddn*n*dp*p-ddp*p*dn*n-dns*dp*p+dps*dn*n) 

            K = np.log(p)
            X = np.log(n)
            right = max(r)
            for i in range(N):
                if r[i]==right:
                    score = i

            Optimun_Lambda = str(round(lambdas[score], 3)) 

            plt.figure() 
            plt.plot(K, X, 'darkblue', linewidth=3)
            plt.title('L-curve', fontdict=font_title)
            plt.axhline(X[score], color="black", linestyle="--")
            plt.axvline(K[score], color="black", linestyle="--")
            plt.xlabel('Residual Norm', fontdict=font_label)
            plt.ylabel('Solution Norm', fontdict=font_label)

            plt.figure()
            plt.plot(lambdas, r, 'darkorange', linewidth=3) 
            plt.title('Expected Curvature', fontdict=font_title)
            plt.text(lambdas[score], r[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
            plt.xlabel(r'Lambda $\lambda$', fontdict=font_label)
            plt.ylabel(r'Curvature $\gamma$', fontdict=font_label)
            plt.grid()
            
            return lambdas[score], chi2


        def KR4th(data, start, end, N, **kwargs):
            mgr = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=False)
            p = []
            n = []
            chi2 = []

            lambdas = np.linspace(start, end, N)
            for lam in lambdas:
                mgr.invert(lam=lam, **kwargs)
                
                n.append(mgr.inv.phiModel())   
                p.append(mgr.inv.phiData())
                chi2.append((mgr.inv.chi2History)[-1])

            n = np.array(n)
            p = np.array(p)
            dn = derivative(n, start, end, N)
            ddn = derivative(dn, start, end, N)
            dp = derivative(p, start, end, N)
            ddp = derivative(dp, start, end, N)
            l = (p*dn)/(dp*n)
            ns = n**2
            ps = p**2
            ls = l**2 

            r = ( 1/((abs(dp*n)**3)*((1+ls)**1.5)) ) * ( ddn*ns*dp*ps-ddp*ps*dn*ns-ls*((dp*n)**3)+l*((dp*n)**3) ) 

            right = max(r)
            for i in range(N):
                if r[i]==right:
                    score = i

            Optimun_Lambda = str(round(lambdas[score], 3))  

            plt.figure() 
            plt.plot(p, n, 'darkblue', linewidth=3)
            plt.title('L-curve', fontdict=font_title)
            plt.axhline(n[score], color="black", linestyle="--")
            plt.axvline(p[score], color="black", linestyle="--")
            plt.xlabel('Residual Norm', fontdict=font_label)
            plt.ylabel('Solution Norm', fontdict=font_label)

            plt.figure()
            plt.plot(lambdas, r, 'darkorange', linewidth=3) 
            plt.title('Expected Curvature', fontdict=font_title)
            plt.text(lambdas[score], r[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
            plt.xlabel(r'Lambda $\lambda$', fontdict=font_label)
            plt.ylabel(r'Curvature $\gamma$', fontdict=font_label)
            plt.grid()
            
            return lambdas[score], chi2