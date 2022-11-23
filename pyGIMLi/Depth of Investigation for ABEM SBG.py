import numpy as np
import pygimli as pg

fileName = "Unsorted ABEM SBG.dat"
dataset = pg.physics.ert.load(fileName)
profileSpatialResolution = dataset.size()

x = pg.x(dataset)
A = np.array(x[dataset("a")])
B = np.array(x[dataset("b")])
M = np.array(x[dataset("m")])
N = np.array(x[dataset("n")])

a = np.array(dataset["a"])
b = np.array(dataset["b"])
m = np.array(dataset["m"])
n = np.array(dataset["n"])

depthOfInvestigations = []
for i in range(profileSpatialResolution):
    if(a[i]==0 and b[i]==3 and m[i]==1 and n[i]==2):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
        
    if(a[i]==0 and b[i]==6 and m[i]==2 and n[i]==4):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
        
    if(a[i]==0 and b[i]==9 and m[i]==3 and n[i]==6):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
        
    if(a[i]==0 and b[i]==12 and m[i]==4 and n[i]==8):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
        
    if(a[i]==0 and b[i]==15 and m[i]==5 and n[i]==10):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
    
    if(a[i]==0 and b[i]==18 and m[i]==6 and n[i]==12):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
        
    if(a[i]==0 and b[i]==21 and m[i]==7 and n[i]==14):
        depthOfInvestigations.append((B[i]-A[i])*0.17)
        
    if(a[i]==0 and b[i]==5 and m[i]==2 and n[i]==3):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==7 and m[i]==3 and n[i]==4):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==9 and m[i]==4 and n[i]==5):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==10 and m[i]==4 and n[i]==6):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==14 and m[i]==6 and n[i]==8):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==18 and m[i]==8 and n[i]==10):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==15 and m[i]==6 and n[i]==9):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==21 and m[i]==9 and n[i]==12):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==27 and m[i]==12 and n[i]==15):
        depthOfInvestigations.append((B[i]-A[i])*0.19)

    if(a[i]==0 and b[i]==20 and m[i]==8 and n[i]==12):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==28 and m[i]==12 and n[i]==16):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==36 and m[i]==16 and n[i]==20):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==25 and m[i]==10 and n[i]==15):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
       
    if(a[i]==0 and b[i]==35 and m[i]==15 and n[i]==20):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==30 and m[i]==12 and n[i]==18):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
    if(a[i]==0 and b[i]==35 and m[i]==14 and n[i]==21):
        depthOfInvestigations.append((B[i]-A[i])*0.19)
        
depthOfInvestigations = list(depthOfInvestigations)
depthOfInvestigations.sort()  

# result = []
# for item in depthOfInvestigations:
#     if item not in result:
#         result.append(item)
# depthOfInvestigations = np.array(result.copy())

# depthOfInvestigations = np.around(depthOfInvestigations, 2)