import numpy as np
import pandas as pd
import seaborn as sns

from geophysics import geoelectric as gelt

Filename = "Unsorted ABEM GDE.dat"
Dataset, Data = gelt.sortMatrix(Filename)
Data = np.delete(Data, (0, 1, 2, 3, 4, 5, 9, 10, 11, 13, 14), axis=1)

SortIndex = np.argsort(Data[:, 0])
Data = Data[SortIndex]

df = pd.DataFrame(Data, columns=['Global Window', 'Window 1', 'Window 2', 
                  'Apparent Resistivity'])
sns.heatmap(df.corr(), annot=True)
