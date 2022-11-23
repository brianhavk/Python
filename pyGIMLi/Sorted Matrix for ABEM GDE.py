import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM GDE.dat"
dataset = pg.physics.ert.load(fileName)
inputFile = open(fileName)
file = inputFile.readlines(); inputFile.close()
lenghtDataMap = len(dataset.dataMap())
data = np.zeros((lenghtDataMap,))
for i in file:
    j = str(i).split(sep='	')
    try:
        j = np.asarray(j[:lenghtDataMap],dtype='float64')
        data = np.vstack((data,j))
    except:
        continue
data = np.delete(data, 0, axis=0)

tokens = dataset.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")

sorted = np.zeros((lenghtDataMap,))
dataLenght = len(data)
j=0; k=0
for i in range(dataLenght): #38 (31-1-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+2 and data[i, 3] == j+3):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #38 (31-1-Left) 
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+9 and data[i, 3] == j+10):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i])) 

j = 0
for i in range(dataLenght): #36 (31-2-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+3 and data[i, 3] == j+4):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(dataLenght): #36 (31-2-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+8 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #35 (21-1-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+3 and data[i, 3] == j+5):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #35 (21-1-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+17 and data[i, 3] == j+19):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #34 (31-3-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+4 and data[i, 3] == j+5):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #34 (31-3-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+7 and data[i, 3] == j+8):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #32 (11-1-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+4 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #32 (11-1-Left) (32 - DD-7-1)
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+25 and data[i, 3] == j+28):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #32 (31-4-Right) (32 - DD-5-2)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+6):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #32 (31-4-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+6 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #31 (21-2-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+5 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #31 (21-2-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+15 and data[i, 3] == j+17):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #29 (1-1-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+5 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #29 (1-1-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+33 and data[i, 3] == j+37):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #27 (21-3-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+7 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #27 (21-3-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+13 and data[i, 3] == j+15):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #26 (11-2-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+7 and data[i, 3] == j+10):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #26 (11-2-Left) 
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+22 and data[i, 3] == j+25):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #23 (21-4-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+11):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #23 (21-4-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+11 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #21 (1-2-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+9 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #21 (1-2-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+29 and data[i, 3] == j+33):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #20 (11-3-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+10 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #20 (11-3-Left) 
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+19 and data[i, 3] == j+22):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #14 (11-4-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+16):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #14 (11-4-Left) 
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+16 and data[i, 3] == j+19):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #13 (1-3-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+13 and data[i, 3] == j+17):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #13 (1-3-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+25 and data[i, 3] == j+29):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #5 (1-4-Right)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+17 and data[i, 3] == j+21):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(len(data)): #5 (1-4-Left)
    if(data[i, 0] == j+1 and data[i, 1] == j+41 and data[i, 2] == j+21 and data[i, 3] == j+25):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

sorted = np.delete(sorted, 0, axis=0)
sorted[:, 0] = sorted[:, 0]-1
sorted[:, 1] = sorted[:, 1]-1
sorted[:, 2] = sorted[:, 2]-1
sorted[:, 3] = sorted[:, 3]-1

count = 0
for item in tokens:
    dataset[item] = pg.Vector(sorted[:, count])
    count += 1  