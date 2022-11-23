import geoelectric as gelt

fileName = "Unsorted ABEM SBG.dat"
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
layers.append(data[38:74, apparentResistivityTokenPosition])
layers.append(data[74:109, apparentResistivityTokenPosition])
layers.append(data[109:143, apparentResistivityTokenPosition])
layers.append(data[143:175, apparentResistivityTokenPosition])
layers.append(data[175:207, apparentResistivityTokenPosition])
layers.append(data[207:238, apparentResistivityTokenPosition])
layers.append(data[238:267, apparentResistivityTokenPosition])
layers.append(data[267:294, apparentResistivityTokenPosition])
layers.append(data[294:320, apparentResistivityTokenPosition])
layers.append(data[320:346, apparentResistivityTokenPosition])
layers.append(data[346:369, apparentResistivityTokenPosition])
layers.append(data[369:392, apparentResistivityTokenPosition])
layers.append(data[392:413, apparentResistivityTokenPosition])
layers.append(data[413:433, apparentResistivityTokenPosition])
layers.append(data[433:453, apparentResistivityTokenPosition])
layers.append(data[453:469, apparentResistivityTokenPosition])
layers.append(data[469:483, apparentResistivityTokenPosition])
layers.append(data[483:496, apparentResistivityTokenPosition])
layers.append(data[496:507, apparentResistivityTokenPosition])
layers.append(data[507:513, apparentResistivityTokenPosition])
layers.append(data[513:519, apparentResistivityTokenPosition])
layers.append(data[519:, apparentResistivityTokenPosition])