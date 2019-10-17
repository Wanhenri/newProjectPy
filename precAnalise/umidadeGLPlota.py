import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import cm

import cartopy

def plotaUmidadeGL(previsao):
    prev = str(previsao)


    for ind in range(0,8,1):
      print('ind',ind) 

      path = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
      path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
      name_file = 'JAN2014_'+ prev +'Z_12Z.nc'
      umidade = 'umidade_GL'
      text = 'Condição inicial:' + umidade

      DS_NCEP = xr.open_dataset(path + name_file)


      prec = [-70,2,4,6,8,10,12,14,16,18,70]
      ussl = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
      uzrs = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
      uzds = [0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0,1.05]
      cssf = [-100,-85,-70,-55,-40,-25,-10,0,10,25,40,55,70,85,100,115,130,145,160,175,190,205,220,235,250,265,280,295,310,325,340,355,370,385,400]
      clsf = [-100,-85,-70,-55,-40,-25,-10,0,10,25,40,55,70,85,100,115,130,145,160,175,190,205,220,235,250,265,280,295,310,325,340,355,370,385,400]
      t2mt = [260,265,270,273,275,278,280,285,287,290,292,293,294,295,296,297,298,299,300,305]
      q2mt = [0.000,0.002,0.004,0.006,0.008,0.010,0.012,0.014,0.016,0.018,0.020,0.022,0.024,0.026,0.028,0.030,0.032]

      config = {
      'ds'      :[DS_NCEP.prec  ,DS_NCEP.ussl ,DS_NCEP.uzrs ,DS_NCEP.uzds ,DS_NCEP.cssf ,DS_NCEP.clsf ,DS_NCEP.t2mt,DS_NCEP.q2mt   ],
      'variavel':['PREC'        ,'USSL'       ,'UZRS'           ,'UZDS'       ,'CSSF'       ,'CLSF'       ,'T2MT','Q2MT'       ],
      'niveis':  [prec, ussl, uzrs, uzds, cssf, clsf, t2mt, q2mt]
      }


      da = config['ds'][ind].mean('time')
      lons = DS_NCEP.variables['lon'][:]
      lats = DS_NCEP.variables['lat'][:]
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
      ax.coastlines(resolution='110m')
      ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
      #for BR
      ax.set_extent([-85, -30, -60, 15])
      ax.stock_img()
      ax.set_title(
                             'Brazilian Global Atmospheric Model (BAM)'
                           + '\n'
                           + 'VAR:  ' 
                           + config['variavel'][ind]
                           + (name_file[0:11] if prev =='120' or prev =='144' or prev == '168' else name_file[0:10])
                           + 'h 12Z'
                           + '\n'
                           + text,
                           fontsize=18
      )
      fig.colorbar(cp, orientation='horizontal',pad=0.05)
      fig.set_label('mm')
      title = (name_file[0:11] if prev =='120' or prev =='144' or prev == '168' else name_file[0:10]) + 'h_12Z_'+ umidade +'_'+ config['variavel'][ind]+'.png'
      plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
      print('Saved: {}'.format(title))
      plt.close()        
      DS_NCEP.close()
    return

for prev in range(24,192,24):

  plotaUmidadeGL(prev)