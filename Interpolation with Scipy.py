from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4])
y = np.array([75, 0, 25, 100])
x_curvado = np.linspace(1, 4, 300)
a_BSpline = interpolate.make_interp_spline(x, y)
y_curvado = a_BSpline(x_curvado)

plt.plot(x, y)
plt.plot(x_curvado, y_curvado)