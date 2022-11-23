from geophysics import geoelectric as gelt

fileName = "Unsorted ABEM GDE.dat"
dataset, data = gelt.sortMatrix(fileName)

token = "rhoa"

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
counter=0;
for item in tokens:
    if item==token:
        selectedTokenPosition = counter
    counter+=1

layers = []
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