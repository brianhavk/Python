import numpy as np

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1000]
threshold = 3
mean = np.mean(data)
std = np.std(data)

atypicalData = []
for item in data:
    zScore = (item - mean)/std
    if(np.abs(zScore) >= threshold):
        atypicalData.append(item)