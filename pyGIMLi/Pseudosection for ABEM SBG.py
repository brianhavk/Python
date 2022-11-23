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

fileName = "Unsorted ABEM SBG.dat"
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
j=0; k=0
for i in range(dataLenght): #38
    # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+3 and data[i, 3] == j+4):
    if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+2 and data[i, 3] == j+3):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-2
sorted[k-j+1:,2] = sorted[k-j+1:,2]+1
sorted[k-j+1:,3] = sorted[k-j+1:,3]+1

j = 0
for i in range(dataLenght): #36
    # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+5 and data[i, 3] == j+6):
    if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+3 and data[i, 3] == j+4):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-4
sorted[k-j+1:,2] = sorted[k-j+1:,2]+2
sorted[k-j+1:,3] = sorted[k-j+1:,3]+2

j = 0        
for i in range(dataLenght): #35
    # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+6 and data[i, 3] == j+7):
    if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+3 and data[i, 3] == j+5):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-5
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+2

j = 0        
for i in range(dataLenght): #34
    # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+7 and data[i, 3] == j+8):
    if(data[i, 0] == j+1 and data[i, 1] == j+8 and data[i, 2] == j+4 and data[i, 3] == j+5):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-6
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+3     
        
j = 0       
for i in range(dataLenght): #32-WN
    # if(data[i, 0] == j+1 and data[i, 1] == j+2 and data[i, 2] == j+9 and data[i, 3] == j+10): 
    if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+4 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))        
sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
sorted[k-j+1:,2] = sorted[k-j+1:,2]+5
sorted[k-j+1:,3] = sorted[k-j+1:,3]+3

j = 0        
for i in range(dataLenght): #32-SBG
    # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+8 and data[i, 3] == j+10):
    if(data[i, 0] == j+1 and data[i, 1] == j+10 and data[i, 2] == j+5 and data[i, 3] == j+6):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-7
sorted[k-j+1:,2] = sorted[k-j+1:,2]+3
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

j = 0
for i in range(dataLenght): #31
    # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+9 and data[i, 3] == j+11):
    if(data[i, 0] == j+1 and data[i, 1] == j+11 and data[i, 2] == j+5 and data[i, 3] == j+7):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-8
sorted[k-j+1:,2] = sorted[k-j+1:,2]+4
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

j = 0
for i in range(dataLenght): #29
    # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+11 and data[i, 3] == j+13):
    if(data[i, 0] == j+1 and data[i, 1] == j+13 and data[i, 2] == j+5 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-10
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+4

j = 0
for i in range(dataLenght): #26-WN
    # if(data[i, 0] == j+1 and data[i, 1] == j+3 and data[i, 2] == j+14 and data[i, 3] == j+16):
    if(data[i, 0] == j+1 and data[i, 1] == j+16 and data[i, 2] == j+6 and data[i, 3] == j+11):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-13
sorted[k-j+1:,2] = sorted[k-j+1:,2]+8
sorted[k-j+1:,3] = sorted[k-j+1:,3]+5

j = 0
for i in range(dataLenght): #27
    # if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+12 and data[i, 3] == j+15):
    if(data[i, 0] == j+1 and data[i, 1] == j+15 and data[i, 2] == j+7 and data[i, 3] == j+9):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-11
sorted[k-j+1:,2] = sorted[k-j+1:,2]+5
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6

j = 0
for i in range(dataLenght): #26-SBG
    # if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+13 and data[i, 3] == j+16):
    if(data[i, 0] == j+1 and data[i, 1] == j+16 and data[i, 2] == j+7 and data[i, 3] == j+10):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))  
sorted[k-j+1:,1] = sorted[k-j+1:,1]-12
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6
        
j = 0
for i in range(dataLenght): #23-WN
    # if(data[i, 0] == j+1 and data[i, 1] == j+4 and data[i, 2] == j+16 and data[i, 3] == j+19):
    if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+7 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-15
sorted[k-j+1:,2] = sorted[k-j+1:,2]+9
sorted[k-j+1:,3] = sorted[k-j+1:,3]+6
        
j = 0
for i in range(dataLenght): #23-SBG
    # if(data[i, 0] == j+1 and data[i, 1] == j+5 and data[i, 2] == j+15 and data[i, 3] == j+19):
    if(data[i, 0] == j+1 and data[i, 1] == j+19 and data[i, 2] == j+9 and data[i, 3] == j+11):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-14
sorted[k-j+1:,2] = sorted[k-j+1:,2]+6
sorted[k-j+1:,3] = sorted[k-j+1:,3]+8
 
j = 0
for i in range(dataLenght): #20-WN
    # if(data[i, 0] == j+1 and data[i, 1] == j+5 and data[i, 2] == j+18 and data[i, 3] == j+22):
    if(data[i, 0] == j+1 and data[i, 1] == j+22 and data[i, 2] == j+8 and data[i, 3] == j+15):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-17
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+7
       
j = 0
for i in range(dataLenght): #21
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+16 and data[i, 3] == j+21):
    if(data[i, 0] == j+1 and data[i, 1] == j+21 and data[i, 2] == j+9 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-15
sorted[k-j+1:,2] = sorted[k-j+1:,2]+7
sorted[k-j+1:,3] = sorted[k-j+1:,3]+8

j = 0
for i in range(dataLenght): #20-SBG
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+17 and data[i, 3] == j+22):
    if(data[i, 0] == j+1 and data[i, 1] == j+22 and data[i, 2] == j+10 and data[i, 3] == j+13):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-16
sorted[k-j+1:,2] = sorted[k-j+1:,2]+7
sorted[k-j+1:,3] = sorted[k-j+1:,3]+9

j = 0
for i in range(dataLenght): #16
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+21 and data[i, 3] == j+26):
    if(data[i, 0] == j+1 and data[i, 1] == j+26 and data[i, 2] == j+11 and data[i, 3] == j+16):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-20
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+10

j = 0
for i in range(dataLenght): #14
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+23 and data[i, 3] == j+28):
    if(data[i, 0] == j+1 and data[i, 1] == j+28 and data[i, 2] == j+13 and data[i, 3] == j+16):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-22
sorted[k-j+1:,2] = sorted[k-j+1:,2]+10
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12

j = 0
for i in range(dataLenght): #13
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+24 and data[i, 3] == j+29):
    if(data[i, 0] == j+1 and data[i, 1] == j+29 and data[i, 2] == j+13 and data[i, 3] == j+17):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-23
sorted[k-j+1:,2] = sorted[k-j+1:,2]+11
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12
        
j = 0
for i in range(dataLenght): #11
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+26 and data[i, 3] == j+31):
    if(data[i, 0] == j+1 and data[i, 1] == j+31 and data[i, 2] == j+13 and data[i, 3] == j+19):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-25
sorted[k-j+1:,2] = sorted[k-j+1:,2]+13
sorted[k-j+1:,3] = sorted[k-j+1:,3]+12
        
j = 0
for i in range(dataLenght): #6
    # if(data[i, 0] == j+1 and data[i, 1] == j+6 and data[i, 2] == j+31 and data[i, 3] == j+36):
    if(data[i, 0] == j+1 and data[i, 1] == j+36 and data[i, 2] == j+15 and data[i, 3] == j+22):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-30
sorted[k-j+1:,2] = sorted[k-j+1:,2]+16
sorted[k-j+1:,3] = sorted[k-j+1:,3]+14

j = 0
for i in range(dataLenght): #6
    # if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+30 and data[i, 3] == j+36):
    if(data[i, 0] == j+1 and data[i, 1] == j+36 and data[i, 2] == j+16 and data[i, 3] == j+21):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-29
sorted[k-j+1:,2] = sorted[k-j+1:,2]+14
sorted[k-j+1:,3] = sorted[k-j+1:,3]+15
        
j = 0
for i in range(dataLenght): #5
    # if(data[i, 0] == j+1 and data[i, 1] == j+7 and data[i, 2] == j+31 and data[i, 3] == j+37):
    if(data[i, 0] == j+1 and data[i, 1] == j+37 and data[i, 2] == j+17 and data[i, 3] == j+21):
        j+=1; k+=1
        sorted = np.vstack((sorted, data[i]))
sorted[k-j+1:,1] = sorted[k-j+1:,1]-30
sorted[k-j+1:,2] = sorted[k-j+1:,2]+14
sorted[k-j+1:,3] = sorted[k-j+1:,3]+16

sorted = np.delete(sorted, 0, axis=0)
sorted[:,0] = sorted[:,0]-1
sorted[:,1] = sorted[:,1]-1
sorted[:,2] = sorted[:,2]-1
sorted[:,3] = sorted[:,3]-1

count = 0
for item in tokens:
    dataset[item] = pg.Vector(sorted[:, count])
    count += 1

ax, colorbar = pg.show(dataset, logScale=True, orientation="vertical", 
                       cMin=min(np.array(dataset["rhoa"])), 
                       cMax=max(np.array(dataset["rhoa"])))
colorbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
colorbar.set_label("Apparent Resistivity [$\Omega$m]", fontdict=font_bar)

# fullDepthOfInvestigations = []
# count = 0
# for item in depthOfInvestigations:
#     fullDepthOfInvestigations.append(item)
#     if(count == 20):
#         fullDepthOfInvestigations.append(item)
#     count +=1  
depthOfInvestigationLabels = ["%.2f" % i for i in depthOfInvestigations]
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], 
            depthOfInvestigationLabels,
            fontsize=8)
ax.set_xlabel("Surface Position [m]", fontdict=font_label)
ax.set_ylabel("Depth of Investigation [m]", fontdict=font_label) 
ax.set_title("Quasi-Pseudosection for ABEM Schlumberger Arrangement", fontdict=font_title)