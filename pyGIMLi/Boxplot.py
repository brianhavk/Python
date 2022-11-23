import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

fileName = 'Linea-3 (Resistance in unified data format).dat'
data = pg.physics.ert.load(fileName)
inputFile = open(fileName)
file = inputFile.readlines(); inputFile.close()
dataMapLenght = len(data.dataMap())
tokenData = np.zeros((dataMapLenght,))
for i in file:
    j = str(i).split(sep='	')
    try:
        j = np.asarray(j[:dataMapLenght],dtype='float64')
        tokenData = np.vstack((tokenData,j))
    except:
        continue
tokenData = np.delete(tokenData, 0, axis=0)

tokens = data.tokenList().split()
tokens.remove("SensorIdx:"); tokens.remove("Data:")
counter=0;
for item in tokens:
    counter+=1
    if item=='rhoa':
        apparentResistivityToken = counter

sort = np.zeros((dataMapLenght,))
tokenLenght = len(tokenData)
j=0; k=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+3 and tokenData[i,1]==j+4 and tokenData[i,2]==j+2 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))
   
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+5 and tokenData[i,1]==j+6 and tokenData[i,2]==j+2 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))
        
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+5 and tokenData[i,1]==j+7 and tokenData[i,2]==j+3 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))   

j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+7 and tokenData[i,1]==j+8 and tokenData[i,2]==j+2 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))
       
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+7 and tokenData[i,1]==j+10 and tokenData[i,2]==j+4 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))

j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+9 and tokenData[i,1]==j+10 and tokenData[i,2]==j+2 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))
      
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+9 and tokenData[i,1]==j+11 and tokenData[i,2]==j+3 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i])) 
         
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+13 and tokenData[i,1]==j+15 and tokenData[i,2]==j+3 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))

j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+13 and tokenData[i,1]==j+16 and tokenData[i,2]==j+4 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))  

j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+17 and tokenData[i,1]==j+19 and tokenData[i,2]==j+3 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i])) 
       
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+19 and tokenData[i,1]==j+22 and tokenData[i,2]==j+4 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i]))
        
j=0
for i in range(tokenLenght):
    if(tokenData[i,0]==j+25 and tokenData[i,1]==j+28 and tokenData[i,2]==j+4 and tokenData[i,3]==j+1):
        j+=1; k+=1
        sort = np.vstack((sort, tokenData[i])) 
        
sort = np.delete(sort, 0, axis=0)
sort[:, 0] = sort[:, 0]-1
sort[:, 1] = sort[:, 1]-1
sort[:, 2] = sort[:, 2]-1
sort[:, 3] = sort[:, 3]-1

data = sort.copy()

pOne = data[:38, apparentResistivityToken-1]
pTwo = data[38:74, apparentResistivityToken-1]
pThree = data[74:109, apparentResistivityToken-1]
pFour = data[109:143, apparentResistivityToken-1]
pFive = data[143:175, apparentResistivityToken-1]
pSix = data[175:207, apparentResistivityToken-1]
pSeven = data[207:238, apparentResistivityToken-1]
pEight = data[238:265, apparentResistivityToken-1]
pNine = data[265:291, apparentResistivityToken-1]
pTen = data[291:314, apparentResistivityToken-1]
pEleven = data[314:334, apparentResistivityToken-1]
pTwelve = data[334:, apparentResistivityToken-1]

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

plt.title('Boxplot for Each Layer', fontdict=font_title)
plt.xlabel('Layer', fontdict=font_label)
plt.ylabel('Apparent Resistivity [$\Omega$m]', fontdict=font_label)
plt.boxplot([pOne, pTwo, pThree, pFour, pFive, pSix, pSeven, pEight, pNine, 
             pTen, pEleven, pTwelve])

# ZSpOne = gelt.ZScore(pOne)
# ZSpTwo = gelt.ZScore(pTwo)
# ZSpThree = gelt.ZScore(pThree)
# ZSpFour = gelt.ZScore(pFour)
# ZSpFive = gelt.ZScore(pFive)
# ZSpSix = gelt.ZScore(pSix)
# ZSpSeven = gelt.ZScore(pSeven)
# ZSpEight = gelt.ZScore(pEight)
# ZSpNine = gelt.ZScore(pNine)
# ZSpTen = gelt.ZScore(pTen)
# ZSpEleven = gelt.ZScore(pEleven)
# ZSpTwelve = gelt.ZScore(pTwelve)

# plt.boxplot([ZSpOne, ZSpTwo, ZSpThree, ZSpFour, ZSpFive, ZSpSix, ZSpSeven, 
#               ZSpEight, ZSpNine, ZSpTen, ZSpEleven, ZSpTwelve])