import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt

import cartopy

def plotaMERGE(anomes):

  #path = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
  path = "/dados/dmdpesq/MERGE/"
  path_out ="/dados/dmdpesq/out_wrf"
  name_file = 'prec_'+anomes+'.nc'
  umidade = 'MERGE'
  text = 'Condição inicial:' + umidade
  MERGE = xr.open_dataset(path + name_file)
  da = MERGE.prec.mean('time')
  lons = MERGE.variables['lon'][:]
  lats = MERGE.variables['lat'][:]
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
                         'MERGE'
                       + '\n' 
                       + anomes 
                       +' 12Z'
                       + '\n'
                       + ' ',
                       fontsize=18
  )
  fig.colorbar(cp, orientation='horizontal',pad=0.05)
  fig.set_label('mm')
  title = umidade + '_'+ anomes  + '_12Z_.png'
  plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
  print('Saved: {}'.format(title))
  plt.close()
  return

anomes = '201808'
plotaMERGE(anomes)