import matplotlib.pyplot as plt
import numpy as np
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

data = pg.physics.ert.load("simple.dat")
manager = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False)


start = 1
end = 10
N = 10
Rn = []
Sn = []

lambdas = np.linspace(start, end, N)
for lam in lambdas:
    manager.invert(lam=lam, paraMaxCellSize=1, robustData=True, 
                   paraDepth=33.8, paraBoundary=0, stopAtChi1=True)
    
    Rn.append(manager.inv.phiData())
    Sn.append(manager.inv.phiModel())   
    
Rn = np.array(Rn)
Sn = np.array(Sn)
dSn = derivative(Sn, start, end, N)
Rn_squared = np.array(Rn)**2
Sn_squared = np.array(Sn)**2
lambdas_squared = lambdas**2

k = (-1)*((Rn*Sn)/dSn)*(((lambdas*Rn*dSn) + (lambdas_squared*Sn*dSn) + (Rn*Sn)) /
                        ((Rn_squared + (lambdas_squared*Sn_squared))**(3/2)))
     
plt.figure()
plt.subplot(2, 1, 1) 
plt.plot(np.log(Rn), np.log(Sn))

plt.subplot(2, 1, 2) 
plt.plot(Rn, Sn)

right = max(k)
for i in range(N):
    if k[i]==right:
        score = i
print(lambdas[score], k[score])
Optimun_Lambda = str(round(lambdas[score], 2))

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
plt.plot(lambdas, k, 'darkorange', linewidth=3) 
plt.title('Expected Curvature', fontdict=font_title)
plt.text(lambdas[score], k[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
plt.xlabel(r'$\lambda$', fontdict=font_label)
plt.ylabel('Curvature', fontdict=font_label)
plt.grid()