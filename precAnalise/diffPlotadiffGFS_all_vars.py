import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import cm
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

def plotaDiff(previsao,):
    prev = str(previsao)
    
    for indVars in range(0,5,1):
        print('indVars',indVars)

        path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
        name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

        path_2 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/" 
        name_file_2 = 'prev.2014.jan_12z_'+ prev +'h_interp.nc'

        path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
        name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

        path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   
    

        DS_NCEP = xr.open_dataset(path_1 + name_file_1)


        DS_NCEP_umidade_Nova = xr.open_dataset(path_3 + name_file_3)


        GFS = xr.open_dataset(path_2 + name_file_2)

        prec = [-50,-45,-40,-35,-30,-25,-20,-15,-10,0,10,15,20,25,30,35,40,45,50]
        #ussl = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
        #uzrs = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
        #uzds = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
        cssf = [-100,-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90, 100]
        clsf = [-160, -140.5,-121,-101.5,-82,-62.5,-43,-23.5,-4,0,4,23.5,43, 62.5,82,101.5,120, 139.5, 160]
        t2mt = [-18,-16.5,-15,-13.5,-12,-10.5,-9,-7.5,-6,-4.5,-3,-1.5,0,1.5, 3, 4.5, 6, 7.5, 9, 10.5,12,13.5,15]
        q2mt = [-0.006, -0.005, -0.004, -0.003, -0.002, -0.001, 0.00, 0.001, 0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01] #0.006,0.008,0.010,0.012,0.014,0.016,0.018,0.020,0.022,0.024,0.026,0.028,0.030,0.032]


        vars = {
                'ds':[
                    DS_NCEP.prec              
                    ,DS_NCEP.cssf               
                    ,DS_NCEP.clsf               
                    ,DS_NCEP.t2mt               
                    ,DS_NCEP.q2mt
                ],
                'ds_nova_umidade':[
                    DS_NCEP_umidade_Nova.prec 
                    ,DS_NCEP_umidade_Nova.cssf  
                    ,DS_NCEP_umidade_Nova.clsf  
                    ,DS_NCEP_umidade_Nova.t2mt  
                    ,DS_NCEP_umidade_Nova.q2mt],
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
                    ,'Q2MT'       
                ],
                'niveis':[
                    prec
                    ,clsf
                    ,cssf
                    ,t2mt
                    ,q2mt
                ]
                }

        longName = vars['ds_GFS'][indVars].attrs['long_name']
        units = vars['ds_GFS'][indVars].attrs['units']


        diff1 = (vars['ds'][indVars].mean('time') - vars['ds_GFS'][indVars].mean('time'))
        diff2 = (vars['ds_nova_umidade'][indVars].mean('time') - vars['ds_GFS'][indVars].mean('time'))
        da = diff2 - diff1

        lons = GFS.variables['lon'][:]
        lats = GFS.variables['lat'][:]

        level = vars['niveis'][indVars]


        fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
        clevs=level
        ax = plt.axes(projection=ccrs.PlateCarree())

        cp = plt.contourf(lons,lats,da, clevs, cmap=cm.BrBG,zorder=1)
        #cp = plt.contourf(lons,lats,da,  cmap=cm.BrBG,zorder=1)

        ax.coastlines(resolution='110m')
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
        #for BR
        ax.set_extent([-83, -34, -47.5, 10])
        ax.stock_img()
        ax.set_title(        '20140101 12Z '
                             + prev
                             + 'h  '
                             + '\n' 
                             + ' DIFF ' 
                             + longName
                             + ' = (LDAS1-GFS) - (OPER-GFS)'
                             + ' [ '+ units + ']',
                             fontsize=18
        )



        fig.colorbar(cp, orientation='horizontal',pad=0.05)
        fig.set_label('mm')

        title = 'diff_'+ prev +'h_'+ vars['variavel'][indVars]+'_Diff_GFS.png'

        plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
        print('Saved: {}'.format(title))
        plt.cla() #means clear current axis
        plt.clf() #means clear current figure
        plt.close('all')
        fig.clf()
        DS_NCEP.close()
        GFS.close()
    return


for prev in range(24,192,24):
    plotaDiff(prev)
