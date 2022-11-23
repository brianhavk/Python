# -*- coding: utf-8 -*-
"""
Created: Brayan Quiceno
License: Grupo de Geofísica y Ciencias de la Computación - GGC3
         Institución Universitaria ITM
         Medellín, Antioquia, Colombia
"""
#%% Libraries
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy

#%% Function
def dct1D(x, q):
    N = len(x)
    
    DCT = []
    for k in range(1, q+1):
        # Kronecker Delta δ #
        if k==1: δ=1        #
        else: δ=0           #
        #####################
    
        summation = 0
        for n in range(1, N+1):
            index = x[n-1]*(1/math.sqrt(1+δ))*math.cos((math.pi*(2*n-1)*(k-1))/(2*N))
            summation += index
        DCT.append(math.sqrt(2/N)*summation)
    return DCT

#%% Main Code
if __name__ == "__main__":

    data = np.array([0, 0, 0, 20, 0, 0, 0, 0, 0, 20, 50, 20, 0, 0, 0, 7, 50, 
                     90, 50, 7, 0,0, 0, 20, 50, 20, 0, 0, 0, 0, 0, 20, 0, 0,0])
    
    plt.figure()
    y = dct1D(data, 20)
    plt.plot(data, label="Original Data")
    plt.plot(y, label="Original Data in DCT Space")
    plt.title("Discrete Cosine Transform by Lopane")
    plt.legend()
    
    plt.figure()
    y = scipy.fftpack.dct(data, norm="ortho")
    plt.plot(data, label="Original Data")
    plt.plot(y, label="Original Data in DCT Space")
    plt.title("Discrete Cosine Transform Using Scipy Library")
    plt.legend()