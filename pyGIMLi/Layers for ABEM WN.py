import geoelectric as gelt

fileName = "Unsorted ABEM WN.dat"
dataset, data = gelt.sortedMatrix(fileName)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
counter=0;
for item in tokens:
    if item=='rhoa':
        apparentResistivityTokenPosition = counter
    counter+=1

layers = []
layers.append(data[:38, apparentResistivityTokenPosition])
layers.append(data[38:73, apparentResistivityTokenPosition])
layers.append(data[73:105, apparentResistivityTokenPosition])
layers.append(data[105:134, apparentResistivityTokenPosition])
layers.append(data[134:157, apparentResistivityTokenPosition])
layers.append(data[157:174, apparentResistivityTokenPosition])
layers.append(data[174:185, apparentResistivityTokenPosition])
layers.append(data[185:, apparentResistivityTokenPosition])