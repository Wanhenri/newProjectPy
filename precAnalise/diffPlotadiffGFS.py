import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import cm

from sys import exit
#import seaborn as sns
#from matplotlib import pylab
#import pandas as pd
#import numpy as np
#import datetime
#from datetime import datetime
#import matplotlib.dates as mdates
#from matplotlib.dates import DateFormatter 
#from matplotlib.ticker import StrMethodFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator



import cartopy

def plotaDiff(previsao,anomes):
    prev = str(previsao)

    
    path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
    name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

    path_2 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/" 
    name_file_2 = 'prev.2014.jan.'+ prev +'h_interp.nc'

    path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
    name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
    
    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   
  

    DS_NCEP_umidade_GL = xr.open_dataset(path_1 + name_file_1)
    #da_DS_NCEP_umidade_GL = DS_NCEP_umidade_GL.prec.mean('time')


    DS_NCEP_umidade_Nova = xr.open_dataset(path_3 + name_file_3)
    #da_DS_NCEP_umidade_Nova = DS_NCEP_umidade_Nova.prec.mean('time')

    GFS = xr.open_dataset(path_2 + name_file_2)
    #da_merge = GFS.prec.mean('time')

    
    diff1 = (DS_NCEP_umidade_GL.prec.mean('time') - GFS.APCP_surface.mean('time'))
    diff2 = (DS_NCEP_umidade_Nova.prec.mean('time') - GFS.APCP_surface.mean('time'))


    #da = abs((DS_NCEP_umidade_GL.prec.mean('time') - MERGE.prec.mean('time'))) - abs((DS_NCEP_umidade_Nova.prec.mean('time') - MERGE.prec.mean('time')))
    #da = (DS_NCEP_umidade_GL.prec.mean('time') - MERGE.prec.mean('time')) - (DS_NCEP_umidade_Nova.prec.mean('time') - MERGE.prec.mean('time'))
    #da = (DS_NCEP_umidade_Nova.prec.mean('time') - MERGE.prec.mean('time')) - (DS_NCEP_umidade_GL.prec.mean('time') - MERGE.prec.mean('time')) 
    da = diff2 - diff1
    #print(da)
    #exit(0)

    lons = DS_NCEP_umidade_GL.variables['lon'][:]
    lats = DS_NCEP_umidade_GL.variables['lat'][:]


    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
    clevs=[-50,-45,-40,-35,-30,-25,-20,-15,-10,0,10,15,20,25,30,35,40]
    ax = plt.axes(projection=ccrs.PlateCarree())
    #cp = plt.contourf(lons,lats,da,clevs, cmap=cm.BrBG , zorder=1)
    cp = plt.contourf(lons,lats,da,clevs, cmap=cm.BrBG , zorder=1)
#1 teste cmap=cm.PuOr
#2 teste cmap=cm.RdGy
#3 teste cmap=cm.BrBG
    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #for BR
    ax.set_extent([-83, -34, -47.5, 10])
    ax.stock_img()
    ax.set_title(          '20140101 12Z '
                         + prev
                         + 'h'
                         + '\n'   
                         + 'DIFF PRECIPITATION = (LDAS1-GFS) - (OPER-GFS) ' ,
                         fontsize=18
    )

    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')
    
    title = 'diff_'+ prev +'_Diff_GFS.png'

    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    DS_NCEP_umidade_GL.close()
    DS_NCEP_umidade_Nova.close()
    GFS.close()
    return

#prev = '24'
for prev in range(24,192,24):
  anomes = '201401'
  plotaDiff(prev,anomes)
