from geophysics import geoelectric as gelt 

fileName = "Unsorted ABEM DD.dat"
dataset, data = gelt.sortMatrix(fileName)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
counter=0;
for item in tokens:
    if item=='rhoa':
        apparentResistivityTokenPosition = counter
    counter+=1
    
layers = []
layers.append(data[:38, apparentResistivityTokenPosition])
layers.append(data[38:74, apparentResistivityTokenPosition])
layers.append(data[74:109, apparentResistivityTokenPosition])
layers.append(data[109:143, apparentResistivityTokenPosition])
layers.append(data[143:175, apparentResistivityTokenPosition])
layers.append(data[175:207, apparentResistivityTokenPosition])
layers.append(data[207:238, apparentResistivityTokenPosition])
layers.append(data[238:265, apparentResistivityTokenPosition])
layers.append(data[265:291, apparentResistivityTokenPosition])
layers.append(data[291:314, apparentResistivityTokenPosition])
layers.append(data[314:334, apparentResistivityTokenPosition])
layers.append(data[334:, apparentResistivityTokenPosition])