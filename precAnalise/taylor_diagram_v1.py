#
#  File:
#    taylor_diagram1.py
#
#  Synopsis:
#    Illustrates how to create a taylor diagram.
#
#  Categories:
#    taylor diagrams
#
#  Author:
#    Fred Castruccio
#    Wanderson Henrique dos Santos
#  
#  Date of initial publication:
#    March 2015
#    Dec   2019
#
#  Description:
#    This example shows how to use the taylor_diagram function added
#    in PyNGL 1.5.0 to create a taylor diagram plot.
#
#  Effects illustrated:
# 
#  Output:
#     A single visualization is produced.
#
#  Notes:
#     



import numpy as np
import Ngl

#from Ngl_modify_v1 import taylor_diagram


import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pylab
from matplotlib.ticker import StrMethodFormatter

import json

from sys import exit
from scipy.stats import pearsonr

def StandardDeviation(actual):

    StandardDeviation=np.std(actual)
    return StandardDeviation

def corr(predict, actual):

    corr, _ = pearsonr(predict, actual)
    return corr


#############################
prev = '24'
var= 'prec'
anomes = '201401'

config = {
  'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
  'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
  'latNorte':[ 75   ,130        ,130            ,195        ,195        ,130        ,195        ],
  'latSul'  :[-182  ,-119       ,-119           ,-45        ,-45        ,-139       ,-45        ],
  'lonOeste':[-157  ,-78        ,-157           ,-79        ,-157       ,-78        ,-210       ],
  'lonLest' :[-69   ,-1         ,-79            ,-1         ,-79        ,-1        ,-153        ]
}

#ind = 6
for ind in range(0,7,1):
    print('ind',ind)

    lista_umidadeGL_std = []
    lista_umidadeNova_std = []
    lista_modeloGFS_std = []

    lista_umidadeGL_corr = []
    lista_umidadeNova_corr = []
    lista_modeloGFS_corr = []

    lista_previsao = []

    for previsao in range(24,192,24):
        prev = str(previsao)
        print(prev)
        path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
        name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
        path_2 = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
        name_file_2 = 'prec_'+anomes+'.nc'
        path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
        name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
        path_4 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
        name_file_4 = 'prev.2014.jan_12z_'+ prev +'h_interp.nc'


        path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"  


        latNorte    = config['latNorte'][ind]
        latSul      = config['latSul'][ind]
        lonOeste    = config['lonOeste'][ind]
        lonLest     = config['lonLest'][ind]

        DS_NCEP = xr.open_dataset(path_1 + name_file_1)

        longName = DS_NCEP.prec.attrs['long_name']
        xTickTime = DS_NCEP.prec['time'].isel(time=slice(None, 31))

        #umidadeGL = DS_NCEP.prec.isel(time=slice(None, 31), lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon")
        umidadeGL = DS_NCEP.prec.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")

        DS_NCEP_umidade_nova = xr.open_dataset(path_3 + name_file_3)
        umidadeNova = DS_NCEP_umidade_nova.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).prec.mean(dim="lat").mean(dim="lon")

        GFS = xr.open_dataset(path_4 + name_file_4)
        modeloGFS = GFS.APCP_surface.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")

        MERGE = xr.open_dataset(path_2 + name_file_2)
        obs = MERGE.prec.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")

        previsao = prev

        corr_umidadeGL = corr(obs, umidadeGL)
        corr_umidadeNova = corr(obs, umidadeNova)
        corr_modeloGFS = corr(obs, modeloGFS)

        ##RESULTADO SUPERESTIMADO
        if ind == 1 or ind == 5 :
            StandardDeviation_umidadeGL = StandardDeviation(umidadeGL) / StandardDeviation(obs) / 2 #a divisao esta sendo feita para normalizar os dados
            StandardDeviation_umidadeNova = StandardDeviation(umidadeNova) / StandardDeviation(obs) / 2
            StandardDeviation_modeloGFS = StandardDeviation(modeloGFS) / StandardDeviation(obs) / 2
            
        else:
            StandardDeviation_umidadeGL = StandardDeviation(umidadeGL) / StandardDeviation(obs)  #a divisao esta sendo feita para normalizar os dados
            StandardDeviation_umidadeNova = StandardDeviation(umidadeNova) / StandardDeviation(obs) 
            StandardDeviation_modeloGFS = StandardDeviation(modeloGFS) / StandardDeviation(obs) 
            


#np.sqrt(np.sum(v**2))
        #RESULTADO INTERESSANTE
        #StandardDeviation_umidadeGL = StandardDeviation(umidadeGL) / np.sqrt(np.sum(StandardDeviation(umidadeGL)**2))
        #StandardDeviation_umidadeNova = StandardDeviation(umidadeNova) / np.sqrt(np.sum(StandardDeviation(umidadeNova)**2))
        #StandardDeviation_modeloGFS = StandardDeviation(modeloGFS) / np.sqrt(np.sum(StandardDeviation(modeloGFS)**2))

        lista_previsao.append(previsao)

        lista_umidadeGL_std.append(StandardDeviation_umidadeGL)
        lista_umidadeNova_std.append(StandardDeviation_umidadeNova)
        lista_modeloGFS_std.append(StandardDeviation_modeloGFS)

        lista_umidadeGL_corr.append(corr_umidadeGL)
        lista_umidadeNova_corr.append(corr_umidadeNova)
        lista_modeloGFS_corr.append(corr_modeloGFS)

    
    #FUNCIONA PARA CRIAÇÃO DE ARQUIVOS DE EXTENSÃO JSON
    #import pandas as pd
    #print(obs)
    #print(lista_umidadeGL_std)
    ##parsed_json = json.dumps(list(lista_umidadeGL_std))
    ##parsed_json = pd.DataFrame(lista_umidadeGL_std).to_json('data.json', orient='split')
    #parsed_json = pd.DataFrame(lista_umidadeGL_std).to_json(orient='values')
    #print(parsed_json)
    #exit(0)

    ###########################
    # Cases [Model]
    #case      = [ "Case A", "Case B" ]
    case      = [ "LDAS", "OPER", "GFS" ]
    nCase     = np.size( case )                 # # of Cases [Cases]

    # variables compared
    #var       = [ "SLP", "Tsfc", "Prc", "Prc 30S-30N", "LW", "SW", "U300", "Guess" ]
    var       = [ "24", "48", "72", "96", "120", "144", "168" ]
    nVar      = np.size(var)                    # # of Variables

    # "Case A"                        
    CA_ratio   = lista_umidadeNova_std #np.array([1.230, 0.988, 1.092, 1.172, 1.064, 0.966, 1.079])
    CA_cc      = lista_umidadeNova_corr #np.array([0.958, 0.973, 0.740, 0.743, 0.922, 0.982, 0.952])

    # "Case B" 
    CB_ratio   = lista_umidadeGL_std # np.array([1.129, 0.996, 1.016, 1.134, 1.023, 0.962, 1.048])
    CB_cc      = lista_umidadeGL_corr #np.array([0.963, 0.975, 0.801, 0.814, 0.946, 0.984, 0.968])

    # "Case C" 
    CC_ratio   = lista_modeloGFS_std #np.array([1.109, 0.906, 1.006, 1.104, 1.003, 0.902, 1.008])
    CC_cc      = lista_modeloGFS_corr #np.array([0.903, 0.905, 0.851, 0.804, 0.906, 0.904, 0.908])

    # arrays to be passed to taylor plot 
    ratio      = np.zeros((nCase, nVar))  
    cc         = np.zeros((nCase, nVar)) 

    ratio[0,:] = CA_ratio 
    ratio[1,:] = CB_ratio
    ratio[2,:] = CC_ratio

    cc[0,:]    = CA_cc 
    cc[1,:]    = CB_cc
    cc[2,:]    = CC_cc

    #**********************************
    # create plot
    #**********************************

    res = Ngl.Resources()                   # default taylor diagram
    
    #del rxy.tmYLValues
    res.tmYLValues        = [0.0, .25, 0.50, 0.75, 1.00, 1.25, 1.5, 1.75]

    res.Markers = [16, 16, 16]             # make all solid fill
    res.gsMarkerSizeF = 18
    res.gsMarkerThicknessF = 2

    #case      = [ "LDAS", "OPER", "GFS" ]
    res.Colors       = ["red", "blue", "Green" ]
    res.varLabels    = var
    res.caseLabels   = case

    res.caseLabelsXloc = 1.2                # Move location of variable labels [default 0.45]
    res.caseLabelsYloc = 1.7                # Move location of variable labels [default 0.45]
    res.caseLabelsFontHeightF = 0.025       # make slight larger   [default=0.12 ]
    res.varLabelsYloc = 1.5                 # Move location of variable labels [default 0.45]
    res.varLabelsFontHeightF  = 0.02        # make slight smaller  [default=0.013]

    res.stnRad        = [ 0.5, 4 ]          # additional standard radii
    res.ccRays        = [ 0.4, 0.75, 0.95 ]        # correllation rays
    res.centerDiffRMS = True                # RMS 'circles'
    #res.centerDiffRMS_color = "gray50"
    res.tiMainFontHeightF   = 0.018

    res.ccRays_color  = "black"          #; default is black
    res.centerDiffRMS_color  = "black"   #; default is black

    res.tiMainString      = "Regiao: " + config['Regiao'][ind] + "Setor: " + config['Setor'][ind]
    res.tiMainFontColor   = "Navy"
    res.tiMainOffsetYF    = 0.02
    res.tiMainFontHeightF = 0.035

    wks_type = "png"

    #wks = Ngl.open_wks(wks_type,path_out + "taylor_diagram_" + str(config['Regiao'][ind])  )
    wks = Ngl.open_wks(wks_type,path_out + "taylor_diagram_" + str(config['Regiao'][ind]) + "_" + str(config['Setor'][ind])  )
  
    plot  = Ngl.taylor_diagram(wks,ratio,cc,res)


