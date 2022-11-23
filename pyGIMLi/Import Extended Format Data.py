import numpy as np

fileName = "Extended ABEM DD.txt"
inputFile = open(fileName)
file = inputFile.readlines(); inputFile.close()

data = np.zeros((4,))
for i in file:
    j = str(i).split(sep='	')
    try:
        j = np.asarray(j[:4],dtype='float64')
        data = np.vstack((data,j))
    except:
        continue
data = np.delete(data, 0, axis=0)