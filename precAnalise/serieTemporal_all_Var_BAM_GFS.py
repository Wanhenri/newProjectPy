#import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pylab
#import pandas as pd
#import numpy as np
#import datetime
#from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
 
from matplotlib.ticker import StrMethodFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator

#import cartopy


def serieTemporal(prev):
    prev = str(prev)


    config = {
      'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
      'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
      'latNorte':[ 75   ,130        ,130            ,195        ,195        ,130        ,195        ],
      'latSul'  :[-182  ,-119       ,-119           ,-45        ,-45        ,-139       ,-45        ],
      'lonOeste':[-157  ,-78        ,-157           ,-79        ,-157       ,-78        ,-210       ],
      'lonLest' :[-69   ,-1         ,-79            ,-1         ,-79        ,-1        ,-153        ]
    }


    for ind in range(0,7,1):
        print('ind',ind)

        for indVars in range(0,5,1):
            print('indVars',indVars)

        #for ind in range(0,7,1):
        #    print('ind',ind)

            pylab.rcParams['figure.figsize'] = (30,10)

            anomes = '201401'
            path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
            name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

            path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
            name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

            path_4 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
            name_file_4 = 'prev.2014.jan_12z_'+ prev +'h_interp.nc'

            path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   

            latNorte    = config['latNorte'][ind]
            latSul      = config['latSul'][ind]
            lonOeste    = config['lonOeste'][ind]
            lonLest     = config['lonLest'][ind]


            sns.set_style("darkgrid", {"axes.facecolor": ".9"})
            sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
            plt.tight_layout()
    
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Com 3 casas decimais
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))

            DS_NCEP = xr.open_dataset(path_1 + name_file_1)
            DS_NCEP_umidade_nova = xr.open_dataset(path_3 + name_file_3)
            GFS = xr.open_dataset(path_4 + name_file_4)

            vars = {
            'ds':[
                DS_NCEP.prec              
                ,DS_NCEP.cssf               
                ,DS_NCEP.clsf               
                ,DS_NCEP.t2mt               
                ,DS_NCEP.q2mt   ],
            'ds_nova_umidade':[
                DS_NCEP_umidade_nova.prec 
                ,DS_NCEP_umidade_nova.cssf  
                ,DS_NCEP_umidade_nova.clsf  
                ,DS_NCEP_umidade_nova.t2mt  
                ,DS_NCEP_umidade_nova.q2mt],
            'ds_GFS': [
                GFS.APCP_surface
                ,GFS.SHTFL_surface
                ,GFS.LHTFL_surface
                ,GFS.TMP_2maboveground
                ,GFS.SPFH_2maboveground
            ],
            'variavel':[
                'PREC'                       
                ,'CSSF'                     
                ,'CLSF'                     
                ,'T2MT'                     
                ,'Q2MT'       ]
            }

            longName = vars['ds_GFS'][indVars].attrs['long_name']
            units = vars['ds_GFS'][indVars].attrs['units']


            plt.figtext(.5,.94,'20140101 12Z  ' + prev +'h' , fontsize=20, ha='center')
            plt.figtext(.5,.90,'Serie Temporal  ' + longName ,fontsize=20,ha='center')
            plt.figtext(.86,.90,'Região: '+ config['Regiao'][ind] +' Setor: '+ config['Setor'][ind] ,fontsize=20,ha='right')



            xTickTime = DS_NCEP.prec['time'].isel(time=slice(None, 31))  


            p1 = vars['ds'][indVars].isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
            plt.plot(xTickTime,p1,color='orange', label='umidade GL')
            plt.xticks(rotation=45) 
            
            p3 = vars['ds_nova_umidade'][indVars].isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
            plt.plot(xTickTime,p3,color='r', label='Nova umidade')
            plt.xticks(rotation=45) 

            p4 = vars['ds_GFS'][indVars].isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
            plt.plot(xTickTime,p4,color='k', label='GFS')
            plt.xticks(rotation=45) 


            plt.ylabel(longName + ' [ '+ units + ']', labelpad=30)


            #plt.ylabel(longName[8:30], labelpad=30)
            plt.xlabel('', labelpad=30)

            title = 'previsao_'+ prev +'_regiao_'+ config['Regiao'][ind] +'_'+ config['Setor'][ind]+'_SerieTemporal_'+ vars['variavel'][indVars] +'_withGFS.png'
            plt.legend(fontsize=17, frameon=True)
            plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300, figsize=(15,15))
            print('Saved: {}'.format(title))
            plt.cla() #means clear current axis
            plt.clf() #means clear current figure
            plt.close()
            DS_NCEP.close()
            DS_NCEP_umidade_nova.close()
            GFS.close()

    return


prev = '24'
for prev in range(24,192,24):
  print('prev',prev)
  serieTemporal(prev)