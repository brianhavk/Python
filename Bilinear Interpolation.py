import numpy as np

x1, x2 = 0, 4
y1, y2 = 1, 3

Q11 = 12
Q21 = -4
Q12 = 0
Q22 = 8

x = 1
y = 2

xVector = np.array([(x2-x), (x-x1)])
QMatrix = np.array([[Q11, Q12], [Q21, Q22]])
yMatrix = np.array([[y2-y], [y-y1]])
P = int(1/((x2-x1)*(y2-y1)) * np.matmul(np.matmul(xVector, QMatrix), yMatrix))
print(P)