import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import pylab
from matplotlib.ticker import StrMethodFormatter

def rmse(predict, actual):

    difference = predict - actual
    square_diff = np.square(difference)
    mean_square_diff = square_diff.mean()
    score = np.sqrt(mean_square_diff)
    return score

config = {
    'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
    'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
    'latNorte':[ 75   ,130        ,130            ,195        ,195        ,130        ,195        ],
    'latSul'  :[-182  ,-119       ,-119           ,-45        ,-45        ,-139       ,-45        ],
    'lonOeste':[-157  ,-78        ,-157           ,-79        ,-157       ,-78        ,-210       ],
    'lonLest' :[-69   ,-1         ,-79            ,-1         ,-79        ,-1        ,-153        ]
  }

latNorte    = config['latNorte'][ind]
latSul      = config['latSul'][ind]
lonOeste    = config['lonOeste'][ind]
lonLest     = config['lonLest'][ind]

pylab.rcParams['figure.figsize'] = (30,10)

#RAINC
ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-"+ mes +"-*RAINC_interp.nc", engine="pynio")
wc_RAINC = ds['RAINC'].isel(lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).groupby('XTIME.day').mean('XTIME').mean(dim="lat").mean(dim="lon")


sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Com 3 casas decimais
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
obs = MERGE.prec.isel(lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
plt.plot(xTickTime, p2,color='dodgerblue', label='MERGE', linewidth=2)
plt.xticks(rotation=45)
MERGE.close()

path_out ="/dados/dmdpesq/out_wrf/
wc = wc_RAINC + wc_RAINNC 

rmse_umidadeGL = rmse(obs, wc)

##### Falta Previsão


title = "Regiao_"+ config['Regiao'][ind] +"_"+ config['Setor'][ind]+"_WRF_2018"+ mes +"_RAINC_RAINNC_serieTemporal.png"
plt.legend(fontsize=17, frameon=True
plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
print('Saved: {}'.format(title))
plt.cla() #means clear current axis
plt.clf() #means clear current figure