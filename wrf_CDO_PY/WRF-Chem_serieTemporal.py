import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import cartopy

import locale


from sys import exit

from datetime import date, datetime, time

import seaborn as sns
from matplotlib import pylab

import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
 
from matplotlib.ticker import StrMethodFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator

###config = {
###     'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
###     'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
###     'latNorte':[156   ,170        ,169            ,3          ,2          ,165        ,2          ],
###     'latSul'  :[-35   ,-24        ,-35            ,-11        ,-11        ,-24        ,-11        ],
###     'lonOeste':[-65   ,-49        ,-65            ,-51        ,-65        ,-51        ,-75        ],
###     'lonLest' :[-49   ,-39        ,-49            ,-34        ,-49        ,-39        ,-65        ]
###  }

config = {
    'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
    'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
    'latNorte':[ 75   ,130        ,130            ,195        ,195        ,130        ,195        ],
    'latSul'  :[-182  ,-119       ,-119           ,-45        ,-45        ,-139       ,-45        ],
    'lonOeste':[-157  ,-78        ,-157           ,-79        ,-157       ,-78        ,-210       ],
    'lonLest' :[-69   ,-1         ,-79            ,-1         ,-79        ,-1        ,-153        ]
  }


for mes in range(8,10,1):
    mes = '%0.2d' % mes
    print("MES: ",mes)
    
    #https://stackoverflow.com/questions/17994358/error-unsupported-locale-setting-on-python-osx
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    mesString = datetime.strptime(mes, '%m').strftime('%B').upper()
    print(mesString)

    
    for ind in range(0,7,1):
        print('ind',ind)


        latNorte    = config['latNorte'][ind]
        latSul      = config['latSul'][ind]
        lonOeste    = config['lonOeste'][ind]
        lonLest     = config['lonLest'][ind]

        pylab.rcParams['figure.figsize'] = (30,10)

        #RAINC
        ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-"+ mes +"-*RAINC_interp.nc", engine="pynio")
        wc_RAINC = ds['RAINC'].isel(lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).groupby('XTIME.day').mean('XTIME').mean(dim="lat").mean(dim="lon")
        #ano_date = ds.JULYR
      

        sns.set_style("darkgrid", {"axes.facecolor": ".9"})
        sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
        plt.tight_layout()

        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Com 3 casas decimais
        #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        #plt.gca().xaxis.set_major_formatter(DateFormatter("%d"))  

        plt.figtext(.5,.96,'Série Temporal', fontsize=30, ha='center')
        plt.figtext(.5,.90,mesString +'/2018',fontsize=20,ha='center')
        #plt.figtext(.15,.90,'Previsão '+ prev +'h 12Z',fontsize=20,ha='left')
        plt.figtext(.86,.90,'Região: '+ config['Regiao'][ind] +' Setor: '+ config['Setor'][ind] ,fontsize=20,ha='right')

        plt.ylim(0,14)

        xTickTime = wc_RAINC['day']

        #print(xTickTime)
        ds.close()
        print("OK RAINC")

        #RAINNC
        ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-"+ mes +"-*RAINNC_interp.nc", engine="pynio")
        wc_RAINNC = ds['RAINNC'].isel(lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).groupby('XTIME.day').mean('XTIME').mean(dim="lat").mean(dim="lon")
        ds.close()
        print("OK RAINNC")

        ##MERGE
        anomes = "2018"+ mes
        path_2 = "/dados/dmdpesq/MERGE/"
        name_file_2 = 'prec_concate_'+anomes+'.nc'
        MERGE = xr.open_dataset(path_2 + name_file_2)
        p2 = MERGE.prec.isel(lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
        plt.plot(xTickTime, p2,color='dodgerblue', label='MERGE', linewidth=2)
        plt.xticks(rotation=45)
        MERGE.close()


        path_out ="/dados/dmdpesq/out_wrf/"

        wc = wc_RAINC + wc_RAINNC 

        plt.plot(xTickTime, wc, color='g', label='RAINC+RAINCC')
        plt.xticks(rotation=45)

        title = "Regiao_"+ config['Regiao'][ind] +"_"+ config['Setor'][ind]+"_WRF_2018"+ mes +"_RAINC_RAINNC_serieTemporal.png"
        plt.legend(fontsize=17, frameon=True)

        plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
        print('Saved: {}'.format(title))
        plt.cla() #means clear current axis
        plt.clf() #means clear current figure
  
   