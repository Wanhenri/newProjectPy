import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt

import cartopy

def plotaMERGE(ano):

  #path = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
  path = "/dados/dmdpesq/MERGE/"
  path_out ="/dados/dmdpesq/out_wrf/"

   
  name_file_1 = 'prec_concate_'+ano+'08.nc'
  name_file_2 = 'prec_concate_'+ano+'09.nc'
  print(name_file_1)
  print(name_file_2)

  

  umidade = 'Mean_Agosto_Setembro_MERGE'
  text = 'Condição inicial:' + umidade
  MERGE_1 = xr.open_dataset(path + name_file_1)
  MERGE_2 = xr.open_dataset(path + name_file_2)
  da_1 = MERGE_1.prec.mean('time')
  da_2 = MERGE_2.prec.mean('time')

  da = (da_1 + da_2)/2


  lons = MERGE_1.variables['lon'][:]
  lats = MERGE_1.variables['lat'][:]
  fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
  ax = plt.axes(projection=ccrs.PlateCarree())
  clevs=[-70,2,4,6,8,10,12,14,16,18,70]
  color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
         'orange','goldenrod','red','firebrick']
  cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)
  ax.coastlines(resolution='110m') #“110m”, “50m”, and “10m”.
  ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
  #for BR
  ax.set_extent([-83, -34, -47.5, 10])
  ax.stock_img()
  ax.set_title(
                         'MERGE  ' 
                       + ano 
                       + '\n'
                       +'Mean Agosto + Setembro  12Z'
                       + '\n'
                       + ' ',
                       fontsize=18
  )
  fig.colorbar(cp, orientation='horizontal',pad=0.05)
  fig.set_label('mm')
  title = umidade + '_'+ ano  + '_12Z_.png'
  plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
  print('Saved: {}'.format(title))
  plt.close()
  return

ano = '2018'
plotaMERGE(ano)