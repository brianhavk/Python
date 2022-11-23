from geophysics import geoelectric as gelt

fileName = "simple.dat"
gelt.atypicalDataVisualization.boxplot(fileName)

fileName = "ABEM DD.dat"
gelt.atypicalDataVisualization.boxplot(fileName)

fileName = "ABEM GDE.dat"
gelt.atypicalDataVisualization.boxplot(fileName, token="ip")

fileName = "ABEM SBG.dat"
gelt.atypicalDataVisualization.boxplot(fileName, byLayers=True)

fileName = "ABEM WN.dat"
gelt.atypicalDataVisualization.boxplot(fileName, byLayers=True, token="ip1")