import matplotlib.pyplot as plt
import numpy as np
import os
import pygimli as pg

def derivative(y, start, end, N):
    import numpy as np
    derivative = np.zeros(N)
    dx = (end-start)/(N-1)
    for i in range(N):
        if i==0:
            derivative[i] = (y[i+1]-y[i])/dx
        elif i==N-1:
            derivative[i] = (y[i]-y[i-1])/dx   
        else: 
            derivative[i] = (y[i+1]-y[i-1])/(2*dx)
    
    return derivative

os.chdir(r"C:\Users\braia\OneDrive - INSTITUTO TECNOLOGICO METROPOLITANO - ITM\Documents\Programs\pyGIMli")
data = pg.physics.ert.load('simple.dat')

#os.chdir(r"C:\Users\Usuario\OneDrive - INSTITUTO TECNOLOGICO METROPOLITANO - ITM\Documentos\Programas\pyGIMli")
manager = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=True)

start = 0.1
end = 0.5
N = 41
p = []
n = []

lambdas = np.linspace(start, end, N)
for lam in lambdas:
    manager.invert(lam=lam)
    
    n.append(manager.inv.phiData())
    p.append(manager.inv.phiModel())   

p = np.array(p)
n = np.array(n)
plog = np.log(p)
nlog = np.log(n)
dplog = derivative(plog, start, end, N)
dnlog = derivative(nlog, start, end, N)
lambdas_squared = lambdas**2 

r = -1/(((1+lambdas_squared)**(3/2))*dnlog)

K = np.log(p)
X = np.log(n)

right = max(r)
for i in range(N):
    if r[i]==right:
        score = i
print(lambdas[score], r[score])
print(K[score], X[score])
Optimun_Lambda = str(round(lambdas[score], 3))

font_title = {'family': 'serif',
              'color':  'darkred',
              'weight': 'normal',
              'size': 16,
              }
font_text = {'family': 'serif',
              'color':  'darkgreen',
              'weight': 'normal',
              'size': 14,
              }
font_label = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 16,
              }   

plt.figure()
plt.subplot(2, 1, 1) 
plt.plot(K, X, 'darkblue', linewidth=3)
plt.title('L-curve', fontdict=font_title)
plt.subplot(2, 1, 2) 
plt.plot(X, K, 'darkblue', linewidth=3)
plt.title('Carsten curve', fontdict=font_title)
plt.tight_layout(w_pad=1.0, h_pad=5.0)

plt.figure()
plt.plot(lambdas, r, 'darkorange', linewidth=3) 
plt.title('Expected Curvature', fontdict=font_title)
plt.text(lambdas[score], r[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
plt.xlabel(r'$\lambda$', fontdict=font_label)
plt.ylabel('Curvature', fontdict=font_label)
plt.grid()

