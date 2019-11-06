import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from sys import exit
from matplotlib import cm

import cartopy

def plotaGFS(previsao):
    prev = str(previsao)

    for ind in range(0,5,1):
        print('ind',ind)
        path = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
        path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
        #name_file = 'JAN2014_'+ prev +'Z_12Z.nc'
        #name_file = 'prev.2014.jan.'+ prev +'h.nc'
        name_file = 'prev.2014.jan_12z_'+ prev +'h_interp.nc'
        umidade = 'GFS'
        text = 'Condição inicial:' + umidade

        GFS = xr.open_dataset(path + name_file)


        prec = [-70,2,4,6,8,10,12,14,16,18,70]
        #ussl = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
        #uzrs = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
        #uzds = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
        cssf = [-100,-85,-70,-55,-40,-25,-10,0,10,25,40,55,70,85,100,115,130,145,160,175,190,205,220,235,250]
        clsf = [-100,-85,-70,-55,-40,-25,-10,0,10,25,40,55,70,85,100,115,130,145,160,175,190,205,220,235,250]
        t2mt = [260,265,270,273,275,278,280,285,287,290,292,293,294,295,296,297,298,299,300,305]
        q2mt = [0.000,0.002,0.004,0.006,0.008,0.010,0.012,0.014,0.016,0.018,0.020,0.022,0.024,0.026,0.028,0.030,0.032]

        config = {
        'ds'      :[GFS.APCP_surface  ,GFS.LHTFL_surface ,GFS.SHTFL_surface ,GFS.SPFH_2maboveground ,GFS.TMP_2maboveground  ],
        'variavel':['PREC'        ,'CLSF'       ,'CSSF'           ,'Q2MT'       ,'T2MT'            ],
        'niveis':  [prec, clsf, cssf, q2mt, t2mt]
        }


        longName = config['ds'][ind].attrs['long_name']
        units = config['ds'][ind].attrs['units']



        #print(longName)
        #exit(0)

        da = config['ds'][ind].mean('time')
        lons = GFS.variables['lon'][:]
        lats = GFS.variables['lat'][:]
        level = config['niveis'][ind]
        fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
        ax = plt.axes(projection=ccrs.PlateCarree())
        clevs=level
        color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
               'orange','goldenrod','red','firebrick']
        if ind == 0:
          #Para Precipitação           
          cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)
        else:
          #Para a demais variaveis
          cp = plt.contourf(lons,lats,da, clevs, cmap=cm.rainbow,zorder=1)

        #if ind == 0:
        #    cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)
        #elif ind == 1:
        #    cp = plt.contourf(lons,lats,da, cmap=cm.rainbow,zorder=1)
        #elif ind == 2:
        #    cp = plt.contourf(lons,lats,da, cmap=cm.rainbow,zorder=1)
        #else:
        #    cp = plt.contourf(lons,lats,da, clevs, cmap=cm.rainbow,zorder=1)





    #    da = GFS.APCP_surface.mean('time')
    #    
    #    lons = GFS.variables['longitude'][:]
    #    lats = GFS.variables['latitude'][:]
    #
    #
    #    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
    #
    #    ax = plt.axes(projection=ccrs.PlateCarree())
    #    clevs=[-70,2,4,6,8,10,12,14,16,18,70]
    #    color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
    #           'orange','goldenrod','red','firebrick']
    #    cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)
    #
    #
        ax.coastlines(resolution='110m')
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
        #for BR
        #ax.set_extent([-85, -30, -60, 15])
        ax.set_extent([-83, -34, -47.5, 10])
        #ax.stock_img()
        ax.set_title(
                              'Global Forecast System (GFS)'
                            + '\n'
                            + '20140101 12Z ' 
                            + (name_file[18:21] if prev =='120' or prev =='144' or prev == '168' else name_file[18:20])
                            + 'h  '
                            +'IC= '
                            + text
                            + '\n'
                            +longName
                            +'  ['
                            + units
                            +']',
                            fontsize=18
        )

        fig.colorbar(cp, orientation='horizontal',pad=0.05)
        fig.set_label('mm')

        title = umidade + '_'+ (name_file[18:21] if prev =='120' or prev =='144' or prev == '168' else name_file[18:20]) + 'h_12Z_'+ config['variavel'][ind]+'_interp.png'

        plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
        print('Saved: {}'.format(title))
        plt.close()
        GFS.close()
    
    return

for prev in range(24,192,24):

  plotaGFS(prev)