# -*- coding: utf-8 -*-
"""
Created: Brayan Quiceno
License: Grupo de Geofísica y Ciencias de la Computación - GGC3
         Institución Universitaria ITM
         Medellín, Antioquia, Colombia
"""
#%% Libraries
import pygimli as pg

#%% Load Dataset and Inversion
filepath = "Unsorted ABEM SBG.dat"
dataset = pg.physics.ert.load(filepath)

dataset["k"] = pg.physics.ert.createGeometricFactors(dataset)
dataset["err"] = pg.physics.ert.estimateError(dataset)

ERTManager = pg.physics.ert.ERTManager(dataset)
ERTManager.invert()
ERTManager.showResult()