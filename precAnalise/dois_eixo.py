import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import pylab
from matplotlib.ticker import StrMethodFormatter
from sys import exit



def rmse(predict, actual):
    #predict = np.array(predict)
    #actual = np.array(actual)

    difference = predict - actual
    square_diff = np.square(difference)
    mean_square_diff = square_diff.mean()
    score = np.sqrt(mean_square_diff)
    return score

def data(actual):
    scoredata = actual.mean()
    return scoredata

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
    #########Pegar long_name e Valores do Eixo X########################
    #path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
    #name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
    #DS_NCEP = xr.open_dataset(path_1 + name_file_1)
    #longName = DS_NCEP.prec.attrs['long_name']
    #xTickTime = DS_NCEP.prec['time'].isel(time=slice(None, 31))
    ###################################################################

    lista_umidadeGL = []
    lista_umidadeNova = []
    lista_modeloGFS = []
    lista_previsao = []

    lista_data_umidadeGL = []
    lista_data_umidadeNova = []
    lista_data_modeloGFS = []


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
        name_file_4 = 'prev.2014.jan.'+ prev +'h_interp.nc'
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
        ###Copiar aqui
	###
        #teste = valorOri(umidadeGL)
        #print(teste)
        #exit(0)
        rmse_umidadeGL = rmse(obs, umidadeGL)
        #print('prev ', prev,'rmse umidade GL: ', rmse_umidadeGL)
        rmse_umidadeNova = rmse(obs, umidadeNova)
        #print('prev ',prev,'umidade nova: ', rmse_umidadeNova)
        rmse_modeloGFS = rmse(obs, modeloGFS)
        #print('prev ',prev,'rmse GFS: ', rmse_modeloGFS)

        lista_previsao.append(previsao)
        lista_umidadeGL.append(rmse_umidadeGL)
        lista_umidadeNova.append(rmse_umidadeNova)
        lista_modeloGFS.append(rmse_modeloGFS)

        ###até aqui

        ############################################################
        #teste = valorOri(umidadeGL)
        #print(teste)
        #exit(0)
        data_umidadeGL = data(umidadeGL)
        #print('value umidade GL: ', data_umidadeGL)
        data_umidadeNova = data(umidadeNova)
        #print('value umidade nova: ', data_umidadeNova)
        data_modeloGFS = data(modeloGFS)
        #print('value GFS: ',data_modeloGFS)

        #lista_previsao.append(previsao)
        lista_data_umidadeGL.append(data_umidadeGL)
        lista_data_umidadeNova.append(data_umidadeNova)
        lista_data_modeloGFS.append(data_modeloGFS)
        ############################################################

    pylab.rcParams['figure.figsize'] = (30,10)
    fig = plt.figure(figsize=(30,10))
    fig, ax1 = plt.subplots()
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
    plt.tight_layout()

    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}'))

    plt.figtext(.5,.99,'Root Mean Squared Error (RMSE)', fontsize=30, ha='center')
    plt.figtext(.5,.95,'Janeiro/2014',fontsize=20,ha='center')
    plt.figtext(.86,.95,'Região: '+ config['Regiao'][ind] +' Setor: '+ config['Setor'][ind] ,fontsize=20,ha='right')
   
     ###copiar aqui
    #Eixo 1
    ax1.set_ylabel('RMSE')
    lns1 = plt.plot(lista_previsao,lista_umidadeGL,color='orange', label='OPER')
    lns2 = plt.plot(lista_previsao,lista_umidadeNova,color='r', label='LDAS')
    #plt.plot(lista_previsao,lista_modeloGFS, color='g', label='GFS')
    #plt.ylim(0,7)
    #plt.ylabel(longName[8:30], labelpad=30)
    
    #Eixo 2
    ax2 = ax1.twinx()
    ax2.set_ylabel('orig', color='b')
    lns3 = plt.plot(lista_previsao,lista_data_umidadeGL, marker='o', linestyle='',color='orange', label='OPER')
    lns4 = plt.plot(lista_previsao,lista_data_umidadeNova, marker='o', linestyle='',color='r', label='LDAS')
    #lns6 = ax2.plt(lista_previsao,lista_data_modeloGFS, marker='o', linestyle='', color='g', label='GFS')
        
    plt.xticks(rotation=45) 
    plt.xlabel('Previsão', labelpad=30)
    title = 'regiao_'+ config['Regiao'][ind] +'_'+ config['Setor'][ind]+'_rmse.png'
    plt.legend(fontsize=17, frameon=True)
    ax1.legend(loc='upper left', bbox_to_anchor=(0.1, -0.15), shadow=True, ncol=5)
    ax2.legend(loc='upper left', bbox_to_anchor=(0.6, -0.15), shadow=True, ncol=5)
    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    plt.cla() #means clear current axis
    plt.clf() #means clear current figure
    plt.close()
    DS_NCEP.close()
    DS_NCEP_umidade_nova.close()
    GFS.close()
    MERGE.close()


   

    
    
#set_extent([x0,x1,y0,y1])
#America do Sul
#set_extent([-82, -34, -50, 12])
#Norte B5
#ax.set_extent([-65, -49, -11, 2])
#Norte B7
#ax.set_extent([-75, -65, -11, 2])
#Nordeste B4
#ax.set_extent([-51, -34, -11, 3])
#Centro-Oeste B3
#ax.set_extent([-65, -49, -35, -11])
#Sul B1
#ax.set_extent([-65, -49, -35, -24])
#Sudeste B2
#ax.set_extent([-49, -39, -24, -10])
#Sudeste B6
#ax.set_extent([-51, -39, -24, -15])