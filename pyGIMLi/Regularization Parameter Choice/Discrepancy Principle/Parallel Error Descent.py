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

start = 1
end = 20
N = 20
for epoch in range(1, 2):  
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
        
    min_chi2 = min(pchi2)
    for i in range(N):
        if(pchi2[i] == min_chi2):
            index = i
    penultimate_lambda = lambdas[index]
        
    max_chi2 = max(lchi2)
    for i in range(N):
        if(lchi2[i] == max_chi2):
            index = i
    last_lambda = lambdas[index]
        
    plt.figure() 
    plt.plot(lambdas, pchi2, "darkblue", linewidth=3)
    plt.text(lambdas[index], pchi2[index], 
             r"$\lambda_O$: "+str(round(penultimate_lambda, 4)), fontdict=fontText)
    plt.title("Penultimate Error History", fontdict=fontTitle)
    plt.xlabel("Lambda $\lambda$", fontdict=fontLabel)
    plt.ylabel(r"$\chi^2$", fontdict=fontLabel)

    plt.figure() 
    plt.plot(lambdas, lchi2, "darkblue", linewidth=3)
    plt.text(lambdas[index], lchi2[index], 
             r"$\lambda_O$: "+str(round(last_lambda, 4)), fontdict=fontText)
    plt.title("Last Error History", fontdict=fontTitle)
    plt.xlabel("Lambda $\lambda$", fontdict=fontLabel)
    plt.ylabel(r"$\chi^2$", fontdict=fontLabel)
    
    
    delta_lambdas = abs(penultimate_lambda - last_lambda)
    if(delta_lambdas > 1):
        delta_lambdas = 1
    
    if(last_lambda < penultimate_lambda):
        start = last_lambda - delta_lambdas
        end = penultimate_lambda + delta_lambdas
    else:
        start =  penultimate_lambda - delta_lambdas
        end = last_lambda + delta_lambdas

    delta_range = end-start
    N = int(((10**epoch)*delta_range)/(2**epoch)) + 1
    if((10**epoch)>100):
        N = int(100*delta_range + 1)