import matplotlib.ticker as ticker
import numpy as np
import pygimli as pg

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
font_bar = {'family': 'serif',
                          'color':  'black',
                          'weight': 'medium',
                          'size': 12,
                          }

fileName = "Unsorted ABEM WN.dat"
dataset, sorted = gelt.sortMatrix(fileName)

depthOfInvestigations = gelt.depthOfInvestigation(dataset)

ax, colorbar = pg.show(dataset, logScale=True, orientation="vertical", 
                       cMin=min(np.array(dataset["rhoa"])), 
                       cMax=max(np.array(dataset["rhoa"])))
colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
colorbar.set_label("Apparent Resistivity [$\Omega$m]", fontdict=font_bar)

depthOfInvestigarionLabels = ["%.2f" % i for i in depthOfInvestigations]
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7], 
            depthOfInvestigarionLabels,
            fontsize=10)
ax.set_xlabel("Surface Position [m]", fontdict=font_label)
ax.set_ylabel("Depth of Investigation [m]", fontdict=font_label)
ax.set_title("Quasi-Pseudosection of ABEM Wenner Arrangement", fontdict=font_title)