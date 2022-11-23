import geoelectric as gelt
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-20, 20, 41)
y = x**2

ndy = gelt.derivative(y, -20, 20, 41) #Numerical differentiation
sdy = 2*x                             #Symbolic differentiation 

plt.figure(figsize=(3,4))

plt.subplot(3, 1, 1)
plt.plot(x, y)
plt.title("Quadratic Function")

plt.subplot(3, 1, 2)
plt.plot(x, ndy, 'tab:green')
plt.title("Numerical differentiation of the function")

plt.subplot(3, 1, 3)
plt.plot(x, sdy, 'tab:red')
plt.title("Symbolic differentiation of the function")

plt.tight_layout()
