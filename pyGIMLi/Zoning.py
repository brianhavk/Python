import pygimli as pg
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(r"C:\Users\braia\OneDrive - INSTITUTO TECNOLOGICO METROPOLITANO - ITM\Documents\Programs\pyGIMli\Margento\1. Junio 2019\Formats")
file = 'Linea-3 (Resistance in unified data format).dat'
data = pg.load(file)

a = np.asarray(data['a']); b = np.array(data['b']); m = np.array(data['m'])
n = np.array(data['n']); err = np.array(data['err']); i = np.array(data['i'])
ip = np.array(data['ip']); ip1 = np.array(data['ip1']); ip2 = np.array(data['ip2'])
ip3 = np.array(data['ip3']); ip4 = np.array(data['ip4']); ip5 = np.array(data['ip5'])
ip6 = np.array(data['ip6']); ip7 = np.array(data['ip7']); ip8 = np.array(data['ip8'])
iperr = np.array(data['iperr']); k = np.array(data['k']); r = np.array(data['r'])
rhoa = np.array(data['rhoa']); u = np.array(data['u']); valid = np.array(data['valid'])

information = np.zeros((348, 21))
information = np.vstack((a, b, m, n, err, i, ip, ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip8, iperr, k, r, rhoa, u, valid))

'''##########  Zoning  ##########'''

copy = np.zeros((348, 21))

guide = np.zeros((0, 21)); k = 0
for i in range(0, 348):
    count = information[:,i]
    if(count[3]==0):
        guide = np.vstack((guide, count))
        k += 1

j = 0; k = 0
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+2 and count[1]==j+3 and count[2]==j+1 and count[3]==j):
        copy[k] = count
        j += 1; k += 1
    if i == 347:
        j = 0

for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+4 and count[1]==j+5 and count[2]==j+1 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0

for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+4 and count[1]==j+6 and count[2]==j+2 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0
        
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+6 and count[1]==j+7 and count[2]==j+1 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0

for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+6 and count[1]==j+9 and count[2]==j+3 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0
        
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+8 and count[1]==j+9 and count[2]==j+1 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0

for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+8 and count[1]==j+10 and count[2]==j+2 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0
 
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+12 and count[1]==j+14 and count[2]==j+2 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0
        
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+12 and count[1]==j+15 and count[2]==j+3 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0
        
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+16 and count[1]==j+18 and count[2]==j+2 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0        
    
for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+18 and count[1]==j+21 and count[2]==j+3 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0

for i in range(0, 348):
    count = information[:,i]
    if(count[0]==j+24 and count[1]==j+27 and count[2]==j+3 and count[3]==j):
        copy[k] = count
        j += 1;  k += 1
    if i == 347:
        j = 0

data['a'] = pg.Vector(copy[:,0]); data['b'] = pg.Vector(copy[:,1])
data['m'] = pg.Vector(copy[:,2]); data['n'] = pg.Vector(copy[:,3])
data['err'] = pg.Vector(copy[:,4]); data['i'] = pg.Vector(copy[:,5])
data['ip'] = pg.Vector(copy[:,6]); data['ip1'] = pg.Vector(copy[:,7])
data['ip2'] = pg.Vector(copy[:,8]); data['ip3'] = pg.Vector(copy[:,9])
data['ip4'] = pg.Vector(copy[:,10]); data['ip5'] = pg.Vector(copy[:,11])
data['ip6'] = pg.Vector(copy[:,12]); data['ip7'] = pg.Vector(copy[:,13])
data['ip8'] = pg.Vector(copy[:,14]); data['iperr'] = pg.Vector(copy[:,15])
data['k'] = pg.Vector(copy[:,16]); data['r'] = pg.Vector(copy[:,17])
data['rhoa'] = pg.Vector(copy[:,18]); data['u'] = pg.Vector(copy[:,19])
data['valid'] = pg.Vector(copy[:,20])
data.save('example.dat')


# '''##############################  Abscissas  ##############################'''
# Snrs_Value = np.array(data.sensorPositions()); Snrs_Value = Snrs_Value[:,0]

# for i in range(348):
#     for j in range(4):
#         copy[i, j] = Snrs_Value[int(copy[i, j])]

# abscissas = np.zeros((348,))
# for i in range(348):
#     abscissas[i] = copy[i, 3] + ((copy[i, 1] - copy[i, 3])/2)
# x = abscissas.copy(); abscissas.sort()
# abscissas_labels = ["%.2f" % i for i in abscissas]

# '''################################  Depth  ################################'''
# for i in range(12):
#     for j in range(4):
#         guide[i, j] = Snrs_Value[int(guide[i, j])]
        
# depth = np.zeros((12,))
# for i in range(12):
#     depth[i] = (guide[i, 1]-guide[i, 3])*0.25
    
# depth_ticks = []
# for i in range(len(depth)):
#     depth_ticks.append(i)
# depth.sort() 
# depth = ["%.2f" % i for i in depth]

# '''############################  ABMN Position  ############################'''
# def getABMN(scheme, idx):
#     """ Get coordinates of four-point cfg with id `idx` from DataContainerERT
#     `scheme`."""
#     coords = {}
#     for elec in "abmn":
#         elec_id = int(scheme(elec)[idx])
#         elec_pos = scheme.sensorPosition(elec_id)
#         coords[elec] = elec_pos.x(), elec_pos.y()
#     return coords


# def plotABMN(ax, scheme, idx):
#     """ Visualize four-point configuration on given axes. """
#     coords = getABMN(scheme, idx)
#     for elec in coords:
#         x, y = coords[elec]
#         if elec in "ab":
#             color = "blue"
#         else:
#             color = "red"
#         ax.plot(x, y, marker=".", color=color, ms=5)
#         ax.annotate(elec.upper(), xy=(x, y), size=12, ha="center", fontsize=10, bbox=dict(
#             boxstyle="round", fc=(0.8, 0.8, 0.8), ec=color), xytext=(0, 15),
#                     textcoords='offset points', arrowprops=dict(
#                         arrowstyle="wedge, tail_width=.5", fc=color, ec=color,
#                         patchA=None, alpha=0.75))
#         ax.plot(coords["a"][0],)

#figure, axis = plt.subplots(1, 1)
#idx = 0

# plotABMN(axis, data, idx)
# pg.show(data, ax=axis)

# for idx in range(0, 1):
#     fig, axis = plt.subplots(1, 1, sharex=True)
#     plotABMN(axis, data, idx)
    
#     coordinates = np.delete(copy[idx], (4,5,6,7,8,9,10,11,12,13,14,15,16,17,
#                                           18, 19, 20), axis=0)
#     world = pg.meshtools.createWorld(start=[min(coordinates)-5, 0], 
#                                       end=[max(coordinates)+5, -2])
#     mesh = pg.meshtools.createMesh(world, area=.05, quality=33)
    
#     ax, cbar = pg.show(mesh, ax=axis)
#     ax.set_ylim(-2, 3.5)
#     ax.set_xlim(min(coordinates)-5, max(coordinates)+5)
#     if idx<=37: 
#         smp = 1; pos = idx
#     if(idx>37 and idx<=73): 
#         smp = 2; pos = idx-37
#     if(idx>73 and idx<=107): 
#         smp = 3; pos = idx-73
#     if(idx>107 and idx<=139): 
#         smp = 4; pos = idx-107
#     if(idx>139 and idx<=174): 
#         smp = 5; pos = idx-139
#     if(idx>174 and idx<=205): 
#         smp = 6; pos = idx-174
#     if(idx>205 and idx<=232): 
#         smp = 7; pos = idx-205
#     if(idx>232 and idx<=255): 
#         smp = 8; pos = idx-232
#     if(idx>255 and idx<=287): 
#         smp = 9; pos = idx-255
#     if(idx>287 and idx<=313): 
#         smp = 10; pos = idx-287
#     if(idx>313 and idx<=333): 
#         smp = 11; pos = idx-313
#     if(idx>333 and idx<=347): 
#         smp = 12; pos = idx-333
#     ax.set_title('Position of electrodes in the measurent range '
#                   +str(smp)+','+str(pos))


# sm = copy[:,18][0:107]
# print(min(sm), max(sm))
# # #f(x)=a(b^x)

# p1 = 3.31
# p2 = 1559

# b = (p2/p1)**(1/14)
# a = p1/(b**1)

# for x in range(18):
#     res = a*(b**x)
#     print(res)