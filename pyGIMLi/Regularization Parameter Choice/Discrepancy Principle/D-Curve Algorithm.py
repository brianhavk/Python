# -*- coding: utf-8 -*-
"""
Created: Brayan Quiceno
License: Grupo de Geofísica y Ciencias de la Computación - GGC3
         Institución Universitaria ITM
         Medellín, Antioquia, Colombia
"""
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
text = {'family': 'serif',
              'color':  'darkgreen',
              'weight': 'normal',
              'size': 12,
              }
fontLabel = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 16,
              } 

#%% Load Dataset and Prompting the ERT Inversion Manager
dataset = pg.physics.ert.load('simple.dat')
ERTManager = pg.physics.ert.ERTManager(dataset, verbose=True)

#%% Iterations

# start = 1
# end = 20
# n = 20

# N = dataset.size()
# Φds = []

# λs = np.linspace(start, end, n)
# for lam in λs:
#     ERTmanager.invert(lam=lam)
    
#     Φds.append(ERTmanager.inv.phiData()) 

# Φd = min(Φds, key=lambda ϕd:abs(ϕd-N))
# λ = λs[Φds.index(Φd)]
    
# plt.figure() 
# plt.plot(λs, Φds, "darkblue", linewidth=3)

# plt.axhline(N, color="black", label="N")
# plt.vlines(λ, ymin=min(Φds), ymax=Φd, color="black", linestyle="--")
# plt.hlines(Φd, xmin=min(λs), xmax=λ, color="black", linestyle="--")
# plt.text(λ+(λ*0.1), Φd-(λ*0.1), "$\lambda_O$: "+str(round(λ, 4)), fontdict=fontText)
# plt.title("D-Curve in Epoch 0", fontdict=fontTitle)
# plt.xlabel("Regularization Paramter $\lambda$", fontdict=fontLabel)
# plt.ylabel("Residual Norm $\Phi_d$", fontdict=fontLabel)

# plt.xlim(min(λs), max(λs))
# plt.ylim(min(Φds), N+4)
# plt.legend(loc ="lower right")

#%% Epochs
start = 1
end = 10
n = 10

N = dataset.size()
Φdos = []
λos = []
ns = []
counter = 0
cycle = 1
epochs = 1
for epoch in range(epochs):
    Φds = []

    λs = np.linspace(start, end, n)
    for lam in λs:
        ERTManager.invert(lam=lam)
        
        Φds.append(ERTManager.inv.phiData()) 

    Φd = min(Φds, key=lambda ϕd:abs(ϕd-N))
    λ = λs[Φds.index(Φd)]
    
    #%% Plot information
    plt.figure() 
    plt.plot(λs, Φds, "darkblue", linewidth=3)

    plt.axhline(N, color="black", label="N")
    plt.vlines(λ, ymin=min(Φds), ymax=Φd, color="black", linestyle="--")
    plt.hlines(Φd, xmin=min(λs), xmax=λ, color="black", linestyle="--")
    plt.scatter(λ, Φd, s=15, color="black")
    plt.title(f"D-Curve in Epoch {epoch+1}", fontdict=fontTitle)
    plt.xlabel("Regularization Parameter $\lambda$", fontdict=fontLabel)
    plt.ylabel("Residual Norm $\Phi_d$", fontdict=fontLabel)

    plt.xlim(min(λs), max(λs))
    plt.ylim(min(Φds), N+1)
    plt.legend(title=r"$\lambda_O$: "+str(round(λ, epoch)), loc="lower right")
    plt.tight_layout()
    
    #%% Save Optimum λ
    Φdos.append(Φd)
    λos.append(λ)
    
    #%% Variables Update
    start = λ - 5/(10**(epoch+1))
    end = λ + 5/(10**(epoch+1))
     
    try:
        if(counter == 2):
            n = 1
            counter = 0
            cycle += 1
                        
        if(λos[-1] == λos[-2]):
            n += (10**cycle)*((2*counter)+1)
            counter += 1 
            
        if(λos[-1] != λos[-2]):
            n = 11
            counter = 0
            cycle = 1     
    except:
        continue
    
    ns.append(n)
#%% Selection of Optimum λ 
Φdo = min(Φdos, key=lambda ϕd:abs(ϕd-N))
λo = λos[Φdos.index(Φdo)]