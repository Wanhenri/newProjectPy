import numpy as np
from numpy import ma
import mpl_toolkits.axisartist.grid_finder as GF
import mpl_toolkits.axisartist.floating_axes as FA
import matplotlib.pyplot as plt

from matplotlib.projections import PolarAxes
from matplotlib import cm

def Taylor_diag(series_corr,series_std,series_previsao):
    """ Taylor Diagram : obs is reference data sample
        in a full diagram (0 --> npi)
        --------------------------------------------------------------------------
        Input: series     - dict with all time series (lists) to analyze  
               series[0]  - is the observation, the reference by default.
    """

    corr1 = series_corr[1]
    std1= series_std[1]
    prev1= series_previsao[1]

    corr = series_corr[0]
    std= series_std[0]
    prev=series_previsao[0]
    
       
    ref = 1# ma.std(series[0])
    #print corr
    
    rlocs = np.concatenate((np.arange(0,-10,-0.25),[-0.95,-0.99],np.arange(0,10,0.25),[0.95,0.99]))
    str_rlocs = np.concatenate((np.arange(0,10,0.25),[0.95,0.99],np.arange(0,10,0.25),[0.95,0.99]))
    tlocs = np.arccos(rlocs)        # Conversion to polar angles
    gl1 = GF.FixedLocator(tlocs)    # Positions
    tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))
    

    str_locs2 = np.arange(-10,11,0.5)
    tlocs2 =  np.arange(-10,11,0.5)      # Conversion to polar angles
       
    g22 = GF.FixedLocator(tlocs2)  
    tf2 = GF.DictFormatter(dict(zip(tlocs2, map(str,str_locs2))))

    
    
    
    tr = PolarAxes.PolarTransform()
    
    smin = 0
    smax = 2.5

    ghelper = FA.GridHelperCurveLinear(tr,
                                           extremes=(0,np.pi, # 1st quadrant
                                                     smin,smax),
                                           grid_locator1=gl1,
                                           #grid_locator2=g11,
                                           tick_formatter1=tf1,
                                           tick_formatter2=tf2,
                                           )
    fig = plt.figure(figsize=(10,5), dpi=100)
    ax = FA.FloatingSubplot(fig, 111, grid_helper=ghelper)

    fig.add_subplot(ax)
    ax.axis["top"].set_axis_direction("bottom") 
    ax.axis["top"].toggle(ticklabels=True, label=True)
    ax.axis["top"].major_ticklabels.set_axis_direction("top")
    ax.axis["top"].label.set_axis_direction("top")
    ax.axis["top"].label.set_text("Correlation Coefficient")

    ax.axis["left"].set_axis_direction("bottom") 
    ax.axis["left"].label.set_text("Standard Deviation")

    ax.axis["right"].set_axis_direction("top") 
    ax.axis["right"].toggle(ticklabels=True, label=True)
    ax.axis["right"].set_visible(True)
    ax.axis["right"].major_ticklabels.set_axis_direction("bottom")
    #ax.axis["right"].label.set_text("Standard Deviation")

    ax.axis["bottom"].set_visible(False) 

    ax.grid(True)

    ax = ax.get_aux_axes(tr)

    t = np.linspace(0, np.pi)
    r = np.zeros_like(t) + ref
    ax.plot(t,r, 'k--', label='_')


    rs,ts = np.meshgrid(np.linspace(smin,smax),
                            np.linspace(0,np.pi))

    
    rms = np.sqrt(ref**2 + rs**2 - 2*ref*rs*np.cos(ts))
    CS =ax.contour(ts, rs,rms,cmap=cm.bone)
    plt.clabel(CS, inline=1, fontsize=10)
    

    ax.plot(np.arccos(0.9999),ref,'k',marker='*',ls='', ms=10)
    #aux = range(1,len(corr))
    #del aux[ref]


    
    #colors = plt.matplotlib.cm.jet(np.linspace(0,1,len(corr)))
    
    #for i in aux:
    plt.plot(np.arccos(corr), std, alpha=0.7,ms=15,marker='o',label="%s" )
    plt.text(np.arccos(corr), std, "OPER" + prev)

    plt.plot(np.arccos(corr1), std1, alpha=0.7,ms=15,marker='o',label="%s" )
    plt.text(np.arccos(corr1), std1, "OPER" + prev1)
    #legend(bbox_to_anchor=(1.5, 1),prop=dict(size='large'),loc='best')
    plt.savefig('example.png', dpi=300)
    return


    #




#import numpy as np
import Ngl

#from Ngl_modify_v1 import taylor_diagram


import xarray as xr
#import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pylab
from matplotlib.ticker import StrMethodFormatter

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
        #print('prev ', prev,'corr umidade GL: ', corr_umidadeGL)
        corr_umidadeNova = corr(obs, umidadeNova)
        #print('prev ',prev,'umidade nova: ', corr_umidadeNova)
        corr_modeloGFS = corr(obs, modeloGFS)
        #print('prev ',prev,'corr GFS: ', corr_modeloGFS)

        StandardDeviation_umidadeGL = StandardDeviation(umidadeGL) / StandardDeviation(obs) #a divisao esta sendo feita para normalizar os dados
        ##print('prev ', prev,'StandardDeviation umidade GL: ', StandardDeviation_umidadeGL)
        StandardDeviation_umidadeNova = StandardDeviation(umidadeNova) / StandardDeviation(obs)
        ##print('prev ',prev,'umidade nova: ', StandardDeviation_umidadeNova)
        StandardDeviation_modeloGFS = StandardDeviation(modeloGFS) / StandardDeviation(obs)
        ##print('prev ',prev,'StandardDeviation GFS: ', StandardDeviation_modeloGFS)



        lista_previsao.append(previsao)

        lista_umidadeGL_std.append(StandardDeviation_umidadeGL)
        lista_umidadeNova_std.append(StandardDeviation_umidadeNova)
        lista_modeloGFS_std.append(StandardDeviation_modeloGFS)

        lista_umidadeGL_corr.append(corr_umidadeGL)
        lista_umidadeNova_corr.append(corr_umidadeNova)
        lista_modeloGFS_corr.append(corr_modeloGFS)

Taylor_diag(lista_umidadeGL_corr,lista_umidadeGL_std,lista_previsao)