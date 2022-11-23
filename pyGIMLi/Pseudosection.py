import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

fileName = 'unsortedAbemDD.dat'
data = pg.physics.ert.load(fileName)

x = pg.x(data)
A = np.array(x[data('a')])
B = np.array(x[data('b')])
M = np.array(x[data('m')])
N = np.array(x[data('n')])

apparentResistivity = np.array(data('rhoa'))
surfacePosition = N+((B-N)/2)
depthOfInvestigation = (B-N)*0.25

layerDepthOfInvestigation = []
for item in depthOfInvestigation:
    if item==3.75:
        mark = 11
     
    if item==6.25:
        mark = 10
        
    if item==7.5:
        mark = 9
        
    if item==8.75:
        mark = 8
        
    if item==11.25:
        mark = 7
        
    if item==12.5:
        mark = 6
        
    if item==17.5:
        mark = 5
        
    if item==18.75:
        mark = 4
        
    if item==22.5:
        mark = 3
        
    if item==26.25:
        mark = 2
        
    if item==33.75:
        mark = 1
     
    layerDepthOfInvestigation.append(mark)

plt.scatter(surfacePosition, layerDepthOfInvestigation, s=50, c=apparentResistivity,
            cmap='Spectral_r')
plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
           ['33.8', '26.3', '23.5', '18.8', '17.5', '12.5', '11.3', '8.8', '7.5', '6.3', '3.8'])

cbar = plt.colorbar(orientation="vertical",
                   pad=0.05, shrink=1, aspect=20)