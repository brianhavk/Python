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

#%% Fonts
fontTitle = {'family': 'serif',
              'color':  'darkred',
              'weight': 'normal',
              'size': 16,
              }
fontText = {'family': 'serif',
              'color':  'darkgreen',
              'weight': 'normal',
              'size': 16,
              }
fontLabel = {'family': 'serif',
              'color':  'darkblue',
              'weight': 'normal',
              'size': 16,
              } 

#%% Load Dataset and Prompting the ERT Inversion Manager
dataset = pg.physics.ert.load("simple.dat")
ERTManager = pg.physics.ert.ERTManager(dataset, verbose=True)

# start = 1
# end = 20
# n = 20

# ERTManager = pg.physics.ert.ERTManager(dataset)
# ρ = []
# η = []
# χ2 = []

# λs = np.linspace(start, end, n)
# for lam in λs:
#     ERTManager.invert(lam=lam)
    
#     η.append(ERTManager.inv.phiModel())   
#     ρ.append(ERTManager.inv.phiData())
#     χ2.append((ERTManager.inv.chi2History)[-1])

# η = np.array(η)
# ρ = np.array(ρ)
# dη = derivative(η, start, end, n)
# ddη = derivative(dη, start, end, n)
# dρ = derivative(ρ, start, end, n)
# ddρ = derivative(dρ, start, end, n)
# ηs = η**2
# ρs = ρ**2
# dηs = dη**2
# dρs = dρ**2

# γ = list( (ρ*η / ((dρs*ηs+ρs*dηs)**1.5)) * (ddη*η*dρ*ρ-ddρ*ρ*dη*η-dηs*dρ*ρ+dρs*dη*η) )

# K = np.log(ρ)
# X = np.log(η)

# γo = max(γ)
# index = γ.index(γo)
# λo = str(round(λs[index], 3))

# plt.figure() 
# plt.plot(ρ, η, "darkblue", linewidth=3)
# plt.title("L-curve", fontdict=fontTitle)
# plt.axhline(η[index], color="black", linestyle="--")
# plt.axvline(ρ[index], color="black", linestyle="--")
# plt.xlabel("Residual Norm $\Phi_d$", fontdict=fontLabel)
# plt.ylabel("Solution Norm $\Phi_m$", fontdict=fontLabel)

# plt.figure()
# plt.plot(λs, γ, "darkorange", linewidth=3) 
# plt.title("Expected Curvature", fontdict=fontTitle)
# plt.text(λs[index], γ[index], "$\lambda_O$: "+λo, fontdict=fontText)
# plt.xlabel("Lambda $\lambda$", fontdict=fontLabel)
# plt.ylabel("Curvature $\gamma$", fontdict=fontLabel)
# plt.grid()

#%% Base Algorithm
start = 1
end = 20
n = 20

ns = []
counter = 0
cycle = 1
λos = []
epochs = 3
for epoch in range(epochs):
    Φds = []
    Φms = []
    χ2 = []

    λs = np.linspace(start, end, n)
    for lam in λs:
        ERTManager.invert(lam=lam, robustData=True)
        
        Φms.append(ERTManager.inv.phiModel())   
        Φds.append(ERTManager.inv.phiData()) 
        χ2.append((ERTManager.inv.chi2History)[-1])

    ηs = np.array(Φms)
    ρs = np.array(Φds)
    dηs = derivative(ηs, start, end, n)
    ddηs = derivative(dηs, start, end, n)
    dρs = derivative(ρs, start, end, n)
    ddρs = derivative(dρs, start, end, n)
    ηs2 = ηs**2
    ρs2 = ρs**2
    dηs2 = dηs**2
    dρs2 = dρs**2

    γ = list( (ρs*ηs / ((dρs2*ηs2 + ρs2*dηs2)**1.5)) * 
             (ddηs*ηs*dρs*ρs - ddρs*ρs*dηs*ηs - dηs2*dρs*ρs + dρs2*dηs*ηs) )

    K = np.log(ρs)
    X = np.log(ηs)

    γo = max(γ)
    index = γ.index(γo)
    λ = λs[index]
    
    plt.figure() 
    plt.plot(ρs, ηs, "darkblue", linewidth=3)
    plt.title("L-curve", fontdict=fontTitle)
    plt.axhline(ηs[index], color="black", linestyle="--")
    plt.axvline(ρs[index], color="black", linestyle="--")
    plt.xlabel("Residual Norm $\Phi_d$", fontdict=fontLabel)
    plt.ylabel("Solution Norm $\Phi_m$", fontdict=fontLabel)

    plt.figure()
    plt.plot(λs, γ, "darkorange", linewidth=3) 
    plt.title("Expected Curvature", fontdict=fontTitle)
    plt.text(λs[index], γ[index], "$\lambda_O$: "+str(round(λ, epoch)), fontdict=fontText)
    plt.xlabel("Lambda $\lambda$", fontdict=fontLabel)
    plt.ylabel("Curvature $\gamma$", fontdict=fontLabel)
    plt.grid()
    
    #%% Save Optimum λs
    λos.append(λ)
    
    #%% Varibales Update
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
# Φdo = min(Φdos, key=lambda ϕd:abs(ϕd-N))
# λo = λos[Φdos.index(Φdo)]

#Δ