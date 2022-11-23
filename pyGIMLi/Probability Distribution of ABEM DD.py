import numpy as np
import matplotlib.pyplot as plt

from geophysics import geoelectric as gelt
from scipy import interpolate

font_label = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 13,
              } 

fileName = "Unsorted ABEM DD.dat"

layers = gelt.layers(fileName)
counter = 1
count0, count1, count2, count3, count4, count5, count6 = 0, 0, 0, 0, 0, 0, 0
for array in layers:
    mean = np.mean(array)
    standardDesviation = np.std(array)
    probabilityDensity = ( 1/(standardDesviation*np.sqrt(2*np.pi)) ) * np.exp( (-1/2)*((array-mean)/standardDesviation)**2)

    sortedIndex = np.argsort(array)
    sortedArray = array[sortedIndex]
    sortedProbabilityDensity = probabilityDensity[sortedIndex]

    zScores = (sortedArray-mean)/standardDesviation
    anomalyDataArray = []
    anomalyDataPropabilityDensity = []
    count = 0
    for item in zScores:
        if(item>=3.0 or item<=-3.0):
            anomalyDataArray.append(sortedArray[count])
            anomalyDataPropabilityDensity.append(sortedProbabilityDensity[count])
        count += 1   
        
        if(item<=-3):
            count0 +=1
        if(item>-3 and item<=-2):
            count1 +=1
        if(item>-2 and item <=-1):
            count2 +=1
        if(item>-1 and item<1):
            count3 +=1  
        if(item>=1 and item<2):
            count4 +=1
        if(item>=2 and item<3):
            count5 +=1
        if(item>=3):
            count6 +=1
        
    interpolationSpline = interpolate.make_interp_spline(sortedArray, sortedProbabilityDensity)
    sortedArray = np.linspace(min(sortedArray), max(sortedArray), int(len(array))*10)
    sortedProbabilityDensity = interpolationSpline(sortedArray)

    ax1 = plt.subplot(1, 1, 1)
    ax1.plot(sortedArray, sortedProbabilityDensity, 
             linestyle="dashed", label=f"Layer {counter}")
    ax1.scatter(anomalyDataArray, anomalyDataPropabilityDensity, s=20)
    counter +=1 
ax1.set_xlabel("Apparent Resistivity", fontdict=font_label)
ax1.set_ylabel("Probability Density", fontdict=font_label)   
plt.legend(ncol=2)
plt.tight_layout()

standardDesviationList = [-3, -2, -1, 0, 1, 2, 3]
zScoreCount = [count0, count1, count2, count3, count4, count5, count6]
fig, ax2 = plt.subplots()
ax2.set_xlabel("Apparent Resistivity Standard Desviations", fontdict=font_label)
ax2.set_ylabel("Quantity", fontdict=font_label)      
bars = ax2.bar(standardDesviationList, zScoreCount, width=0.5, 
               color=plt.get_cmap("tab20c").colors)
ax2.bar_label(bars)
plt.tight_layout()