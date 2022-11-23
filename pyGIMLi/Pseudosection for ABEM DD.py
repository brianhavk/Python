import geoelectric as gelt
import matplotlib.ticker as ticker
import numpy as np
import pygimli as pg

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

depthOfInvestigations = gelt.depthOfInvestigation(dataset)

sorted = np.zeros((lenghtDataMap,))
dataLenght = len(data)
j = 0; k = 0
for i in range(dataLenght): #38
    if(data[i, 0] == j+3 and data[i, 1] == j+4 and data[i, 2] == j+2 and data[i, 3] == j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
        
j = 0
for i in range(dataLenght): #36
    if(data[i,0]==j+5 and data[i,1]==j+6 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
        
j = 0
for i in range(dataLenght): #35
  # if(data[i,0]==j+6 and data[i,1]==j+7 and data[i,2]==j+2 and data[i,3]==j+1):
    if(data[i,0]==j+5 and data[i,1]==j+7 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))   
sorted[k-j+1:,0]=sorted[k-j+1:,0]+1
sorted[k-j+1:,2]=sorted[k-j+1:,2]-1

j = 0
for i in range(dataLenght): #34
    if(data[i,0]==j+7 and data[i,1]==j+8 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
        
j = 0
for i in range(dataLenght): #32
  # if(data[i,0]==j+9 and data[i,1]==j+10 and data[i,2]==j+2 and data[i,3]==j+1):
    if(data[i,0]==j+7 and data[i,1]==j+10 and data[i,2]==j+4 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0]=sorted[k-j+1:,0]+2
sorted[k-j+1:,2]=sorted[k-j+1:,2]-2

j = 0
for i in range(dataLenght): #32
  # if(data[i,0]==j+7 and data[i,1]==j+10 and data[i,2]==j+4 and data[i,3]==j+1):
    if(data[i,0]==j+9 and data[i,1]==j+10 and data[i,2]==j+2 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0]=sorted[k-j+1:,0]-2
sorted[k-j+1:,2]=sorted[k-j+1:,2]+2 

j = 0
for i in range(dataLenght): #31
  # if(data[i,0]==j+8 and data[i,1]==j+11 and data[i,2]==j+4 and data[i,3]==j+1):
    if(data[i,0]==j+9 and data[i,1]==j+11 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i])) 
sorted[k-j+1:,0]=sorted[k-j+1:,0]-1
sorted[k-j+1:,2]=sorted[k-j+1:,2]+1
         
j = 0
for i in range(dataLenght): #27
  # if(data[i,0]==j+12 and data[i,1]==j+15 and data[i,2]==j+4 and data[i,3]==j+1):
    if(data[i,0]==j+13 and data[i,1]==j+15 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,0]=sorted[k-j+1:,0]-1
sorted[k-j+1:,2]=sorted[k-j+1:,2]+1

j = 0
for i in range(dataLenght): #26
    if(data[i,0]==j+13 and data[i,1]==j+16 and data[i,2]==j+4 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))  

j = 0
for i in range(dataLenght): #23
  # if(data[i,0]==j+16 and data[i,1]==j+19 and data[i,2]==j+4 and data[i,3]==j+1):
    if(data[i,0]==j+17 and data[i,1]==j+19 and data[i,2]==j+3 and data[i,3]==j+1):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i])) 
sorted[k-j+1:,0]=sorted[k-j+1:,0]-1
sorted[k-j+1:,2]=sorted[k-j+1:,2]+1
        
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
  
ax, colorbar = pg.show(dataset, logScale=True, orientation="vertical", 
                       cMin=min(np.array(dataset["rhoa"])), 
                       cMax=max(np.array(dataset["rhoa"])))
colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
colorbar.set_label("Apparent Resistivity [$\Omega$m]", fontdict=font_bar)

fullDepthOfInvestigations = []
count = 0
for item in depthOfInvestigations:
    fullDepthOfInvestigations.append(item)
    if(count == 4):
        fullDepthOfInvestigations.append(item)
    count +=1  
depthOfInvestigationLabels = ["%.2f" % i for i in fullDepthOfInvestigations]
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
              depthOfInvestigationLabels)
ax.set_xlabel("Electrode Position on the Surface [m]", fontdict=font_label)
ax.set_ylabel("Depth of Investigation [m]", fontdict=font_label)
ax.set_title("Quasi-Pseudosection for ABEM Dipole-Dipole Arrangement", fontdict=font_title)
