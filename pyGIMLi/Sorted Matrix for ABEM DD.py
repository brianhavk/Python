import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM DD.dat"
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
for i in range(dataLenght): #38
    if(data[i,0]==j+3 and data[i,1]==j+4 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
        
j=0
for i in range(dataLenght): #36
    if(data[i,0]==j+5 and data[i,1]==j+6 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
        
j=0
for i in range(dataLenght): #35
    if(data[i,0]==j+5 and data[i,1]==j+7 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))   

j = 0
for i in range(dataLenght): #34
    if(data[i,0]==j+7 and data[i,1]==j+8 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
        
j = 0
for i in range(dataLenght): #32
    if(data[i,0]==j+7 and data[i,1]==j+10 and data[i,2]==j+4 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(dataLenght): #32
    if(data[i,0]==j+9 and data[i,1]==j+10 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
       
j = 0
for i in range(dataLenght): #31
    if(data[i,0]==j+9 and data[i,1]==j+11 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i])) 
         
j = 0
for i in range(dataLenght): #27
    if(data[i,0]==j+13 and data[i,1]==j+15 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(dataLenght): #26
    if(data[i,0]==j+13 and data[i,1]==j+16 and data[i,2]==j+4 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))  

j = 0
for i in range(dataLenght): #23
    if(data[i,0]==j+17 and data[i,1]==j+19 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i])) 
        
j = 0
for i in range(dataLenght): #20
    if(data[i,0]==j+19 and data[i,1]==j+22 and data[i,2]==j+4 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))

j = 0
for i in range(dataLenght): #14
    if(data[i,0]==j+25 and data[i,1]==j+28 and data[i,2]==j+4 and data[i,3]==j+1):
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