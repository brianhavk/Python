import geoelectric as gelt
import numpy as np

data = gelt.sortMatrix.abemDD("unsortedAbemDD.dat")

firstLayer = np.array(data['rhoa'])[0:38]
firstLayer = list(firstLayer); firstLayer.sort()

Q1 = np.percentile(firstLayer, 25)
Q3 = np.percentile(firstLayer, 75)
IQR = Q3-Q1
minimum = Q1-(1.5*IQR)
maximum = Q3+(1.5*IQR)

data = np.array(data['rhoa'])
layers = np.asarray([[1, 2],
                  [3, 4]])

# for layer in data:
    
#     Q1 = np.percentile(layer, 25)
#     Q3 = np.percentile(layer, 75)
#     IQR = Q3-Q1
#     minimum = Q1-(1.5*IQR)
#     maximum = Q3+(1.5*IQR)
    
