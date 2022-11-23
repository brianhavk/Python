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

#%% Functions
def derivative(y, start, end, N):
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

epochs = 2
for epoch in range(epochs):
    Φds = []
    Φms = []
    
    λs = np.linspace(start, end, n)
    for lam in λs:
        ERTManager.invert(lam=lam)
        
        Φds.append(ERTManager.inv.phiData())
        Φms.append(ERTManager.inv.phiModel())
    
    ρ = np.array(Φds)
    η = np.array(Φms)
    
    dρ = derivative(ρ, start, end, n)
    ddρ = derivative(dρ, start, end, n)
    dη = derivative(η, start, end, n)
    ddη = derivative(dη, start, end, n)
        
    ζ = (ρ*dη)/(dρ*η)
    
    η2 = η**2
    ρ2 = ρ**2
    dη2 = dη**2
    ζ2 = ζ**2
    
    product = (((η*ddη)/dη2)-((ddρ*η)/(dη*dρ))) * (ζ2/((1+ζ2)**1.5))
    division = ((-1*ζ2)+ζ)/((1+ζ2)**1.5)
    γ = product + division
    
    #%% Save Optimum λ
    index = int((np.where(γ==max(γ)))[0])
    λ = λs[index]
    λos.append(λ)
    
    #%% Plot Information
    plt.figure() 
    plt.plot(Φds, Φms, "darkblue", linewidth=3)
    plt.axhline(Φms[int((np.where(λs==λ))[0])], color="black", linestyle="--")
    plt.axvline(Φds[int((np.where(λs==λ))[0])], color="black", linestyle="--")
    plt.xlabel("Residual Norm $\Phi_d$", fontdict=label)
    plt.ylabel("Solution Norm $\Phi_m$", fontdict=label)
    plt.title(f"L-Curve in Epoch {epoch+1}", fontdict=title)
    plus = abs(min(Φds) - max(Φds))*0.01
    plt.xlim(min(Φds)-plus, max(Φds)+plus)
    plt.ylim(min(Φms)-plus, max(Φms)+plus)
    plt.tight_layout()

    plt.figure() 
    plt.plot(λs, γ, "darkblue", linewidth=3)
    plt.vlines(λ, ymin=min(γ), ymax=max(γ), color="black", linestyle="--")
    plt.hlines(max(γ), xmin=min(λs), xmax=λ, color="black", linestyle="--")
    plt.scatter(λ, max(γ), s=15, color="black")
    plt.xlabel(r"Regularization Parameter $\lambda$", fontdict=label)
    plt.ylabel(r"Curvature $\gamma$", fontdict=label)
    plt.title(f"Expected Curvature in Epoch {epoch+1}", fontdict=title)
    plt.xlim(min(λs), max(λs))
    plt.ylim(min(γ), max(γ)*1.05)
    plt.legend(title=r"$\lambda_O$: "+str(round(λ, epoch+adjustment)), 
               loc="lower right")
    plt.tight_layout()
    
    #%% Variables Update
    if(index==1): start = λs[index-1]
    else: start = λs[index-2]  
    
    if(index==(len(λs)-2)): end = λs[index+1] 
    else: end = λs[index+2]
    
    n = int(((end-start)*10))+1
    
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