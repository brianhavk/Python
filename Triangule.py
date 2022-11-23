import numpy as np
import math
import matplotlib.pyplot as plt

electrodePosition = np.array([[2, 3, 1, 0],
                              [4, 5, 1, 0],
                              [6, 7, 1, 0],
                              [8, 9, 1, 0],
                              [4, 6, 2, 0], 
                              [8, 10, 2, 0], 
                              [12, 14, 2,0],
                              [16, 18, 2, 0],
                              [6, 9, 3, 0],
                              [12, 15, 3, 0],
                              [18, 21, 3, 0],
                              [24, 27, 3, 0]])

A = electrodePosition[:, 0]
B = electrodePosition[:, 1]
M = electrodePosition[:, 2]
N = electrodePosition[:, 3]


deltaMN = (M-N)/2
deltaBA = (B-A)/2 + A
midPoint = (deltaBA+deltaMN)/2

a = midPoint - deltaMN
hypotenuse = a/math.cos(math.radians(45))

# for i in range(12):
#     x = np.array([deltaMN[i], midPoint[i], deltaBA[i]]) 
#     y = np.array([0, hypotenuse[i], 0])
#     plt.figure()    
#     plt.plot(x, y) 
#     plt.gca().invert_yaxis()    
#     plt.show()