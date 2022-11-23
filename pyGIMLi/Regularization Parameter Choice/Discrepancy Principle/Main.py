#%% Libraries and Functions
import matplotlib.pyplot as plt
import numpy as np
import pygimli as pg

#%% Fonts
fontTitle = {'family': 'serif',
              'color':  'darkred',
              'weight': 'normal',
              'size': 16,
              }
fontText = {'family': 'serif',
              'color':  'darkgreen',
              'weight': 'normal',
              'size': 14,
              }
fontLabel = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 16,
              } 

#%% Main Code
dataset = pg.physics.ert.load('simple.dat')
ERTmanager = pg.physics.ert.ERTManager(dataset, verbose=True)

start = 0.39
end = 0.49
N = 101
p = []
n = []
lchi2 = []
pchi2 = []

lambdas = np.linspace(start, end, N)
for lam in lambdas:
    ERTmanager.invert(lam=lam)
    
    p.append(ERTmanager.inv.phiData())
    n.append(ERTmanager.inv.phiModel())   
    lchi2.append((ERTmanager.inv.chi2History)[-1])
    pchi2.append((ERTmanager.inv.chi2History)[-2])

plt.figure() 
plt.plot(lambdas, p, 'darkblue', linewidth=3)
plt.axhline(171, color="black", linestyle="--")
plt.title('D-Curve', fontdict=fontTitle)
plt.xlabel(r'Lambda $\lambda$', fontdict=fontLabel)
plt.ylabel('Residual Norm', fontdict=fontLabel)

plt.figure() 
plt.plot(p, n, 'darkblue', linewidth=3)
#plt.axhline(n[10], color="black", linestyle="--")
#plt.axvline(p[10], color="black", linestyle="--")
plt.title('L-Curve', fontdict=fontTitle)
plt.xlabel("Residual Norm", fontdict=fontLabel)
plt.ylabel('Solution Norm', fontdict=fontLabel)

min_chi2 = min(pchi2)
for i in range(N):
    if(pchi2[i] == min_chi2):
        index = i
penultimate_lambda = lambdas[index]
plt.figure() 
plt.plot(lambdas, pchi2, "darkblue", linewidth=3)
plt.text(lambdas[index], pchi2[index], 
         r"$\lambda_O$: "+str(round(penultimate_lambda, 4)), fontdict=fontText)
plt.title("Penultimate Error History", fontdict=fontTitle)
plt.xlabel("Lambda $\lambda$", fontdict=fontLabel)
plt.ylabel(r"$\chi^2$", fontdict=fontLabel)

# max_chi2 = max(lchi2)
# for i in range(N):
#     if(lchi2[i] == max_chi2):
#         index = i
# last_lambda = lambdas[index]
# plt.figure() 
# plt.plot(lambdas, lchi2, "darkblue", linewidth=3)
# plt.text(lambdas[index], lchi2[index], 
#          r"$\lambda_O$: "+str(round(last_lambda, 4)), fontdict=fontText)
# plt.title("Last Error History", fontdict=fontTitle)
# plt.xlabel("Lambda $\lambda$", fontdict=fontLabel)
# plt.ylabel(r"$\chi^2$", fontdict=fontLabel)