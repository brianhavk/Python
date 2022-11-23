import math
import numpy as np
import pygimli as pg

dataset = pg.physics.ert.load("simple.dat")
ERTmanager = pg.physics.ert.ERTManager(dataset, verbose=True)
ERTmanager.invert()

Φd = ERTmanager.inv.phiData()

ρa = np.array(dataset["rhoa"])
err = np.array(ERTmanager.checkError(dataset["err"])) #np.array(ERTmanager.estimateError())
                               #np.array(dataset["err"])
                               #np.array(ERTmanager.checkError(dataset["err"]))
                               #np.array(ERTmanager.checkData())

relrms = ERTmanager.inv.relrms()
εi = np.log(1+(relrms/ρa))
# di = np.log(ρai)
# fim = np.array(ERTmanager.inv.response)

# phiModel = 0.0
# for i in range(dataset.size()):
#     phiModel = ((di[i]-fim[i])/εi[i])**2 + phiModel



# pa = ρa/(err+1)
# era = abs(pa - paa)

# era = err*ρa 




# s = err*np.mean(ρa)
# #nl = ((err*100)-1e-6)/ρa 
# nl = (err*100)/(1e-6+ρa)
# ε = np.linalg.norm(nl)



response = np.array(ERTmanager.inv.response)
δd = abs(response - ρa)
t = np.linalg.norm(δd)
d = ρa 
δlogd = np.log(1+δd/d)
ε = np.linalg.norm(δlogd)


# response = np.array(ERTmanager.inv.response)
# model = np.array(ERTmanager.inv.model)
# e = np.linalg.norm(ρa)*0.01

