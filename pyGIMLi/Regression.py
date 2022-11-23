import matplotlib.pyplot as plt
import seaborn as sns

from geophysics import geoelectric as gelt

Filename = "Unsorted ABEM DD.dat"
Dataset, Data = gelt.sortMatrix(Filename)
Depth_of_Investigation = gelt.depthOfInvestigation(Dataset, All=True)
Apparent_Resistivity = list(Dataset["rhoa"])

plt.scatter(Depth_of_Investigation, Apparent_Resistivity)
plt.show()

# sns.jointplot(Depth_of_Investigation, Apparent_Resistivity, kind="hex")
