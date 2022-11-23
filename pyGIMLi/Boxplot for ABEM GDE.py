import matplotlib.pyplot as plt

from geophysics import geoelectric as gelt

font_title = {'family': 'serif',
              'color':  'darkred',
              'weight': 'normal',
              'size': 13,
              }
font_label = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 13,
              } 

fileName = "Unsorted ABEM GDE.dat"
layers = gelt.layers.apparentResistivity(fileName)

plt.title("Boxplot for Each Layer", fontdict=font_title)
plt.xlabel("Layer", fontdict=font_label)
plt.ylabel("Apparent Resistivity [$\Omega$m]", fontdict=font_label)
plt.boxplot(layers)
