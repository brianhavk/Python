import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import pygimli as pg

# data=pd.read_excel("data_mauro.xlsx")

# formaciones=data["Formación"].unique()
# formaciones

# pozos=data["Pozo"].unique()
# pozos

# hojas=[]
# for i in pozos:
#     hojas.append(data[data["Pozo"]==i].copy())
    
# def grafica(datos,unicos,save=False):
    
#     datos=datos.append({"Formación":int(7)},ignore_index=True)
#     # extrae los valores unicos de las formaciones
#     leyendas=dict(enumerate(unicos))
#     leyendas_inv=dict((v, k) for k, v in leyendas.items())
    
#     #se toqueniza la información
#     info_tok=datos.replace(leyendas_inv)
    
#     #datos a graficar
#     graficar=info_tok["Formación"].copy()
#     dat_graf=graficar.values    
#     dat_graf=np.reshape(dat_graf,[dat_graf.shape[0],1])
#     dat_graf=np.hstack([dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf])
    
#     rango=list(range(0,len(datos),round(len(datos)/10)))
#     valores=np.round(info_tok[["Prof  Perf"]].iloc[rango].values.T[0],2)
    
#     # se crea el esquema del grafico
    
#     plt.figure(figsize=(2,len(datos)))
#     im = plt.imshow(dat_graf, interpolation='none',cmap='gist_heat_r')

#     #im = plt.imshow(dat_graf, interpolation='none',cmap='gist_heat_r')
    
#     plt.title(datos["Pozo"].iloc[0], fontsize=12, fontfamily='serif')
#     plt.xticks([5], ["Formaciones"], fontsize=7, fontfamily='serif')
#     plt.yticks(rango,valores,rotation=20)
    
    
    
    
#     # se optienen los colores de la grafica
#     colors = [ im.cmap(im.norm(value)) for value in range(len(unicos))]
    
    

#     values=list(unicos[np.unique(dat_graf[:-1,:].astype(int))])
#     indices=[]
#     for i in values:
#       indices.append(list(unicos).index(i))

  

#     patches = [ mpatches.Patch(color=colors[i], label="{l}".format(l=unicos[i]) ) for i in indices ]
    
#     # put those patched as legend-handles into the legend
#     plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    
#     if save==True:
        
#         plt.savefig((datos["Pozo"].iloc[0]+".png"),dpi=300,bbox_inches='tight')
        
#     plt.show()
    
# pozos_graficar=["PM 171","PM 172","PM 180","PM 170","PM 179"]
# # for i in pozos_graficar:
# #     grafica(hojas[np.where(pozos==i)[0][0]],formaciones,False)



# unicos = formaciones
# datos = hojas[166]
# datos=datos.append({"Formación":int(7)},ignore_index=True)
# # extrae los valores unicos de las formaciones
# leyendas=dict(enumerate(unicos))
# leyendas_inv=dict((v, k) for k, v in leyendas.items())

# #se toqueniza la información
# info_tok=datos.replace(leyendas_inv)

# #datos a graficar
# graficar=info_tok["Formación"].copy()
# dat_graf=graficar.values    
# dat_graf=np.reshape(dat_graf,[dat_graf.shape[0],1])
# dat_graf=np.hstack([dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf,dat_graf])

# rango=list(range(0,len(datos),round(len(datos)/10)))
# valores=np.round(info_tok[["Prof  Perf"]].iloc[rango].values.T[0],2)

# plt.figure(figsize=(2,len(datos)))
# im = plt.imshow(dat_graf, interpolation='none',cmap='gist_heat_r')

# #im = plt.imshow(dat_graf, interpolation='none',cmap='gist_heat_r')

# plt.title(datos["Pozo"].iloc[0], fontsize=12, fontfamily='serif')
# plt.xticks([5], ["Formaciones"], fontsize=7, fontfamily='serif')
# plt.yticks(rango,valores,rotation=20)


#########################

data= pg.load('Linea-3 (Resistance of unified data format).dat')

x = pg.x(data)
distal_electrode = x[data('b')]
proximal_electrode = x[data('n')]
delta_position = (distal_electrode - proximal_electrode)
delta_position = np.array(delta_position)

score_position = []
for i in range(len(delta_position)):
    if delta_position[i] == max(delta_position):
        score_position.append(i)

x = np.array(x)
distal_electrode = np.array(distal_electrode)
proximal_electrode = np.array(proximal_electrode)     
abscissas = proximal_electrode + (distal_electrode - proximal_electrode)/2
rhoa = np.array(data['rhoa'])

VES_right_depth = []; VES_right_rhoa = []
VES_left_depth = []; VES_left_rhoa = []
electrode_spacing = x[1]-x[0]
i = score_position[1]
for j in range(len(delta_position)): 
    
    if(abscissas[j] == (proximal_electrode[i] + (distal_electrode[i] - proximal_electrode[i])/2) 
       or 
       abscissas[j] == ((proximal_electrode[i] + (distal_electrode[i] - proximal_electrode[i])/2) + electrode_spacing/2)):
        VES_right_depth.append((distal_electrode[j] - proximal_electrode[j])/4)
        VES_right_rhoa.append(rhoa[j])
        
    if(abscissas[j] == (proximal_electrode[i] + (distal_electrode[i] - proximal_electrode[i])/2) 
       or 
       abscissas[j] == ((proximal_electrode[i] + (distal_electrode[i] - proximal_electrode[i])/2) - electrode_spacing/2)):
        VES_left_depth.append((distal_electrode[j] - proximal_electrode[j])/4)
        VES_left_rhoa.append(rhoa[j])

VES_right_depth_order = VES_right_depth.copy(); VES_right_depth_order.sort()
VES_right_depth_ = []; VES_right_rhoa_ = []
for i in range(len(VES_right_depth)):
    for j in range(len(VES_right_depth)):
        if(VES_right_depth[j] == VES_right_depth_order[i]):
          VES_right_depth_.append(VES_right_depth[j]) 
          VES_right_rhoa_.append(VES_right_rhoa[j])
   
VES_left_depth_order = VES_left_depth.copy(); VES_left_depth_order.sort()
VES_left_depth_ = []; VES_left_rhoa_ = []
for i in range(len(VES_left_depth)):
    for j in range(len(VES_left_depth)):
        if(VES_left_depth[j] == VES_left_depth_order[i]):
          VES_left_depth_.append(VES_left_depth[j]) 
          VES_left_rhoa_.append(VES_left_rhoa[j])
        
plt.subplot(2, 1, 1)
plt.plot(VES_right_depth_, VES_right_rhoa_, '-o', label='1D (VES)')
plt.title('VES Right')
plt.xlabel('Depth (m)')
plt.ylabel('Apparent resistivity ($\Omega$m)')
plt.grid(1)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(VES_left_depth_, VES_left_rhoa_, '-xr', label='1D (VES)')
plt.title('VES Left')
plt.xlabel('Depth (m)')
plt.ylabel('Apparent resistivity ($\Omega$m)')
plt.grid(1)
plt.legend()

plt.tight_layout(w_pad=1.0, h_pad=5.0)