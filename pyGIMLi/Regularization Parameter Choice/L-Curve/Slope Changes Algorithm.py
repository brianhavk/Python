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
label = {'family': 'serif',
         'color': 'darkblue',
         'weight': 'normal',
         'size': 14} 

text = {'family': 'serif',
        'color':  'darkgreen',
        'weight': 'normal',
        'size': 14}

title = {'family': 'serif',
         'color':  'darkred',
         'weight': 'normal',
         'size': 16}


#%% Load Dataset and Prompting the ERT Inversion Manager
dataset = pg.physics.ert.load("simple.dat")
ERTManager = pg.physics.ert.ERTManager(dataset, verbose=True)

#%% Iterations
# start = 1
# end = 10
# n = 10

# ERTManager = pg.physics.ert.ERTManager(dataset)
# ρs = []
# ηs = []

# λs = np.linspace(start, end, n)
# for λ in λs:
#     ERTManager.invert(lam=λ)
    
#     ρs.append(ERTManager.inv.phiData())
#     ηs.append(ERTManager.inv.phiModel())   

# m = []
# for i in range(n):
#     try: m.append((ηs[i+1]-ηs[i])/(ρs[i+1]-ρs[i]))
#     except: continue

# ξ = []
# for i in range(len(m)):
#     try: ξ.append(abs(m[i]/m[i+1]))
#     except: continue

# index = ξ.index(max(ξ))
# λo = (λs[1:n-1])[index]

# plt.figure() 
# plt.plot(ρs, ηs, "darkblue", linewidth=3)
# plt.xlabel("Residual Norm $\Phi_d$", fontdict=label)
# plt.ylabel("Solution Norm $\Phi_m$", fontdict=label)

# plt.figure() 
# plt.plot(λs[1:n-1], ξ, "darkblue", linewidth=3)
# plt.xlabel(r"Regularization Parameter $\lambda$", fontdict=label)
# plt.ylabel(r"Slope Changes $\xi$", fontdict=label)

#%% Epochs
start = 0.2
end = 1
n = 9

N = dataset.size()
Φdos = []
λos = []
adjustment = 1
counter = 0
cycle = 1
ns = []

if(start<1): adjustment = 2

epochs = 1
for epoch in range(epochs):
    Φds = []
    Φms = []
    
    λs = np.linspace(start, end, n)
    for lam in λs:
        ERTManager.invert(lam=lam)
        
        Φds.append(ERTManager.inv.phiData())
        Φms.append(ERTManager.inv.phiModel())
        
    ms = []
    for i in range(n):
        try: ms.append((Φms[i+1]-Φms[i])/(Φds[i+1]-Φds[i]))
        except: continue

    ξs = []
    for i in range(len(ms)):
        try: ξs.append(abs(ms[i]-ms[i+1]))
        except: continue
    
    #%% Save Optimum λ
    index = ξs.index(max(ξs))
    λ = (λs[1:n-1])[index]
    λos.append(λ)
    
    #%% Plot Information
    plt.figure() 
    plt.plot(Φds, Φms, "darkblue", linewidth=3)
    plt.axhline(Φms[int((np.where(λs==λ))[0])], color="black", linestyle="--")
    plt.axvline(Φds[int((np.where(λs==λ))[0])], color="black", linestyle="--")
    plt.xlabel("Residual Norm $\Phi_d$", fontdict=label)
    plt.ylabel("Solution Norm $\Phi_m$", fontdict=label)
    plt.title(f"L-Curve in Epoch {epoch+1}", fontdict=title)
    plt.xlim(min(Φds), max(Φds))
    plt.ylim(min(Φms), max(Φms))
    plt.tight_layout()

    plt.figure() 
    plt.plot(λs[1:n-1], ξs, "darkblue", linewidth=3)
    plt.vlines(λ, ymin=min(ξs), ymax=max(ξs), color="black", linestyle="--")
    plt.hlines(max(ξs), xmin=min(λs), xmax=λ, color="black", linestyle="--")
    plt.scatter(λ, max(ξs), s=15, color="black")
    plt.xlabel(r"Regularization Parameter $\lambda$", fontdict=label)
    plt.ylabel(r"Slope Changes $\xi$", fontdict=label)
    plt.title(f"Expected Changes in Epoch {epoch+1}", fontdict=title)
    plt.xlim(min(λs), max(λs))
    plt.ylim(min(ξs), max(ξs)*1.05)
    plt.legend(title=r"$\lambda_O$: "+str(round(λ, epoch)), loc="lower right")
    plt.tight_layout()
    
    #%% Variables Update
    start = λ - 0.05
    end = λ + 0.05
    n = 11
    
    # start = λ - 5/(10**(epoch+adjustment))
    # end = λ + 5/(10**(epoch+adjustment))
     
    # try:
    #     if(counter == 2):
    #         n = 1
    #         counter = 0
    #         cycle += 1 
            
    #     if(λos[-1] == λos[-2]):
    #         n += (10**cycle)*((2*counter)+1)
    #         counter += 1 
            
    #     if(λos[-1] != λos[-2]):
    #         n = 11
    #         counter = 0
    #         cycle = 1     
    # except:
    #     continue
    
    # ns.append(n)