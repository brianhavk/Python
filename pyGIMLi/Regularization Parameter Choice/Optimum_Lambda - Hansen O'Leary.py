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

data = pg.physics.ert.load('Linea-3 (Resistance of unified data format).dat')
manager = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False)

start = 1
end = 10                                                                                                                              
N = 10
Rn = []
Sn = []

lambdas = np.linspace(start, end, N)
for lam in lambdas:
    manager.invert(lam=lam)
    
    Rn.append(manager.inv.phiData())
    Sn.append(manager.inv.phiModel())   
    
Rn = np.array(Rn)
Sn = np.array(Sn)
Rn_log = np.log(Rn)
Sn_log = np.log(Sn)
dRn_log = derivative(Rn_log, start, end, N)
dRn_log_squared = dRn_log**2
ddRn_log = derivative(dRn_log, start, end, N)
dSn_log = derivative(Sn_log, start, end, N)
dSn_log_squared = dSn_log**2
ddSn_log = derivative(dSn_log, start, end, N)

k = ( ((dRn_log*ddSn_log) - (ddRn_log*dSn_log)) 
      / 
      (((dRn_log_squared + dSn_log_squared))**(3/2)) )

right = max(k)
for i in range(N):
    if k[i]==right:
        score = i
print(lambdas[score], k[score])
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
plt.plot(Rn_log, Sn_log, 'darkblue', linewidth=3)
plt.title('L-curve', fontdict=font_title)
plt.subplot(2, 1, 2) 
plt.plot(Sn, Rn, 'darkblue', linewidth=3)
plt.title('Carsten curve', fontdict=font_title)
plt.tight_layout(w_pad=1.0, h_pad=5.0)

plt.figure()
plt.plot(lambdas, k, 'darkorange', linewidth=3) 
plt.title('Expected Curvature', fontdict=font_title)
plt.text(lambdas[score], k[score], r'$\lambda_O$: '+Optimun_Lambda, fontdict=font_text)
plt.xlabel(r'$\lambda$', fontdict=font_label)
plt.ylabel('Curvature', fontdict=font_label)
plt.grid()
