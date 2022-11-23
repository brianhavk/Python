from geophysics import geoelectric as gelt

font_bar = {'family': 'serif',
            'color':  'black',
            'weight': 'medium',
            'size': 12,
            }

fileName = "ABEM DD.dat"
gelt.showMeasurementDistribution(fileName)

fileName = "ABEM GDE.dat"
gelt.showMeasurementDistribution(fileName)

fileName = "ABEM SBG.dat"
gelt.showMeasurementDistribution(fileName)

fileName = "ABEM WN.dat"
gelt.showMeasurementDistribution(fileName, token="ip")

