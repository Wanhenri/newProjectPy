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
  pylab.rcParams['figure.figsize'] = (30,10)
  
  anomes = '201401'
  path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
  name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
  path_2 = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
  name_file_2 = 'prec_'+anomes+'.nc'
  path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
  name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
  path_4 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
  name_file_4 = 'prev.2014.jan.'+ prev +'h_interp.nc'
  path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   

  sns.set_style("darkgrid", {"axes.facecolor": ".9"})
  sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
  plt.tight_layout()
 


  plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Com 3 casas decimais
  plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
  plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
  

  plt.figtext(.5,.96,'Série Temporal', fontsize=30, ha='center')
  plt.figtext(.5,.90,'Janeiro/2014',fontsize=20,ha='center')
  plt.figtext(.15,.90,'Previsão '+ prev +'h 12Z',fontsize=20,ha='left')
  plt.figtext(.86,.90,'Região: NORTE   B7',fontsize=20,ha='right')

  DS_NCEP = xr.open_dataset(path_1 + name_file_1)

  longName = DS_NCEP.prec.attrs['long_name']

  xTickTime = DS_NCEP.prec['time'].isel(time=slice(None, 31))  

  
  p1 = DS_NCEP.prec.isel(time=slice(None, 31), lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon")
  plt.plot(xTickTime,p1,color='orange', label='umidade GL')
  plt.xticks(rotation=45) 

  DS_NCEP_umidade_nova = xr.open_dataset(path_3 + name_file_3)
  p3 = DS_NCEP_umidade_nova.isel(time=slice(None, 31), lat=slice(2,-11), lon=slice(-75,-65)).prec.mean(dim="lat").mean(dim="lon")
  plt.plot(xTickTime,p3,color='r', label='Nova umidade')
  plt.xticks(rotation=45) 

  GFS = xr.open_dataset(path_4 + name_file_4)
  p4 = GFS.APCP_surface.isel(time=slice(None, 31), lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon")
  plt.plot(xTickTime, p4, color='g', label='GFS')
  plt.xticks(rotation=45)

  MERGE = xr.open_dataset(path_2 + name_file_2)
  p2 = MERGE.prec.isel(time=slice(None, 31), lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon")
  plt.plot(xTickTime, p2,color='dodgerblue', label='MERGE', linewidth=2)
  plt.xticks(rotation=45)

  plt.ylabel(longName[8:30], labelpad=30)
  plt.xlabel('Dia', labelpad=30)
  
  title = 'teste_reorganizando'+ prev +'.png'
  plt.legend(fontsize=17, frameon=True)
  plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300, figsize=(15,15))
  print('Saved: {}'.format(title))
  plt.cla() #means clear current axis
  plt.clf() #means clear current figure
  plt.close()
  return

var= 'prec'
prev = '24'
for prev in range(24,192,24):
  print('prev',prev)
  serieTemporal(prev)