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

os.chdir(r"C:\Users\braia\OneDrive - INSTITUTO TECNOLOGICO METROPOLITANO - ITM\Programs\pyGIMli")
data = pg.physics.ert.load('simple.dat')

manager = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=False)

start = 0.24
end = 0.44
N = 21 
p = []
n = []

lambdas = np.linspace(start, end, N)
for lam in lambdas:
    manager.invert(lam=lam)
    
    n.append(manager.inv.phiModel())   
    p.append(manager.inv.phiData())

n = np.array(n)
p = np.array(p)
dn = derivative(n, start, end, N)
ddn = derivative(dn, start, end, N)
dp = derivative(p, start, end, N)
ddp = derivative(dp, start, end, N)
ns = n**2
ps = p**2
dns = dn**2
dps = dp**2

r = ( p*n / ((dps*ns+ps*dns)**1.5) ) * (ddn*n*dp*p-ddp*p*dn*n-dns*dp*p+dps*dn*n)

K = np.log(p)
X = np.log(n)
right = max(r)
for i in range(N):
    if r[i]==right:
        score = i

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
plt.plot(K, X, 'darkblue', linewidth=3)
plt.title('L-curve', fontdict=font_title)
plt.axhline(X[score], color="black", linestyle="--")
plt.axvline(K[score], color="black", linestyle="--")
plt.xlabel('Residual Norm', fontdict=font_label)
plt.ylabel('Solution Norm', fontdict=font_label)

plt.figure()
plt.plot(lambdas, r, 'darkorange', linewidth=3) 
plt.title('Expected Curvature', fontdict=font_title)
plt.text(lambdas[score], r[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
plt.xlabel(r'Lambda $\lambda$', fontdict=font_label)
plt.ylabel(r'Curvature $\gamma$', fontdict=font_label)
plt.grid()