import geoelectric as gelt
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

fileName = "Unsorted ABEM DD.dat"
layers = gelt.layers.apparentResistivity(fileName)
array = layers[0]

mean = np.mean(array)
standardDesviation = np.std(array)
probabilityDensity = ( 1/(standardDesviation*np.sqrt(2*np.pi)) ) * np.exp( (-1/2)*((array-mean)/standardDesviation)**2)

sortedIndex = np.argsort(array)
sortedArray = array[sortedIndex]
sortedProbabilityDensity = probabilityDensity[sortedIndex]

interpolationSpline = interpolate.make_interp_spline(sortedArray, sortedProbabilityDensity)
sortedArray = np.linspace(min(sortedArray), max(sortedArray), int(len(array))*10)
sortedProbabilityDensity = interpolationSpline(sortedArray)

zScores = (sortedArray-mean)/standardDesviation

lowerCleanDataPosition = 0
count = 0
for item in zScores:
    if(item>=-2.0):
        lowerCleanDataPosition = count
        break
    count += 1 

upperCleanDataPosition = int(len(sortedArray))
count = 0
for item in zScores:
    if(item>=2.0):
        upperCleanDataPosition = count
        break
    count += 1   

lowerAnomalyDataPosition = 0
count = 0
for item in zScores:
    if(item>=-3.0):
        lowerAnomalyDataPosition = count
        break
    count += 1 

upperAnomalyDataPosition = int(len(sortedArray))
count = 0
for item in zScores:
    if(item>=3.0):
        upperAnomalyDataPosition = count
        break
    count += 1   
 
font_label = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 10,
              }   

ax1 = plt.subplot(212)
ax1.plot(sortedArray, sortedProbabilityDensity, color="darkblue", linestyle="dashed")
ax1.fill_between(sortedArray[:lowerAnomalyDataPosition], sortedProbabilityDensity[:lowerAnomalyDataPosition], color="darkblue", alpha=0.5)
ax1.fill_between(sortedArray[upperAnomalyDataPosition:], sortedProbabilityDensity[upperAnomalyDataPosition:], color="darkblue", alpha=0.5)
ax1.set_xlabel("Apparent Resistivity", fontdict=font_label)
ax1.set_ylabel("Probability Density", fontdict=font_label)

ax2 = plt.subplot(221)
ax2.plot(sortedArray[:lowerCleanDataPosition], sortedProbabilityDensity[:lowerCleanDataPosition], color="darkblue", linestyle="dashed")
ax2.fill_between(sortedArray[:lowerAnomalyDataPosition], sortedProbabilityDensity[:lowerAnomalyDataPosition], color="darkblue", alpha=0.5)
ax2.set_xlabel("Apparent Resistivity", fontdict=font_label)
ax2.set_ylabel("Probability Density", fontdict=font_label)

ax3 = plt.subplot(222)
ax3.plot(sortedArray[upperCleanDataPosition:], sortedProbabilityDensity[upperCleanDataPosition:], color="darkblue", linestyle="dashed")
ax3.fill_between(sortedArray[upperAnomalyDataPosition:], sortedProbabilityDensity[upperAnomalyDataPosition:], color="darkblue", alpha=0.5)
ax3.set_xlabel("Apparent Resistivity", fontdict=font_label)

plt.tight_layout()