import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pylab
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



 
from matplotlib.ticker import StrMethodFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator



import cartopy


def plotaNovaUmidade(previsao):
    prev = str(previsao)
    path = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
    name_file = 'JAN2014_'+ prev +'Z_12Z.nc'
    umidade = 'Nova_Umidade_do_Solo'
    text = 'Condição inicial:' + umidade
        
    DS_NCEP = xr.open_dataset(path + name_file)

    da = DS_NCEP.prec.mean('time')

    lons = DS_NCEP.variables['lon'][:]
    lats = DS_NCEP.variables['lat'][:]


    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)

    ax = plt.axes(projection=ccrs.PlateCarree())
    clevs=[-70,2,4,6,8,10,12,14,16,18,70]
    color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
           'orange','goldenrod','red','firebrick']
    cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)


    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #for BR
    ax.set_extent([-85, -30, -60, 15])
    ax.stock_img()
    ax.set_title(
                           'Brazilian Global Atmospheric Model (BAM)' 
                         + '\n' 
                         + (name_file[0:11] if prev =='120' or prev =='144' or prev == '168' else name_file[0:10])
                         + 'h 12Z'
                         + '\n'
                         + text,
                         fontsize=18
    )

    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')

    title = (name_file[0:11] if prev =='120' or prev =='144' or prev == '168' else name_file[0:10]) + 'h_12Z_'+ umidade +'.png'

    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    return 

########
def plotaUmidadeGL(previsao):
    prev = str(previsao)
    path = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
    name_file = 'JAN2014_'+ prev +'Z_12Z.nc'
    umidade = 'umidade_GL'
    text = 'Condição inicial:' + umidade

    DS_NCEP = xr.open_dataset(path + name_file)

    da = DS_NCEP.prec.mean('time')
    
    lons = DS_NCEP.variables['lon'][:]
    lats = DS_NCEP.variables['lat'][:]


    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)

    ax = plt.axes(projection=ccrs.PlateCarree())
    clevs=[-70,2,4,6,8,10,12,14,16,18,70]
    color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
           'orange','goldenrod','red','firebrick']
    cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)


    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #for BR
    ax.set_extent([-85, -30, -60, 15])
    ax.stock_img()
    ax.set_title(
                           'Brazilian Global Atmospheric Model (BAM)'
                         + '\n'
                         + (name_file[0:11] if prev =='120' or prev =='144' or prev == '168' else name_file[0:10])
                         + 'h 12Z'
                         + '\n'
                         + text,
                         fontsize=18
    )

    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')

    title = (name_file[0:11] if prev =='120' or prev =='144' or prev == '168' else name_file[0:10]) + 'h_12Z_'+ umidade +'.png'

    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    return
#####
def plotaGFS(previsao):
    prev = str(previsao)
    path = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
    #name_file = 'JAN2014_'+ prev +'Z_12Z.nc'
    name_file = 'prev.2014.jan.'+ prev +'h.nc'
    umidade = 'GFS'
    text = 'Condição inicial:' + umidade

    GFS = xr.open_dataset(path + name_file)
    
    da = GFS.APCP_surface.mean('time')
    
    lons = GFS.variables['longitude'][:]
    lats = GFS.variables['latitude'][:]


    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)

    ax = plt.axes(projection=ccrs.PlateCarree())
    clevs=[-70,2,4,6,8,10,12,14,16,18,70]
    color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
           'orange','goldenrod','red','firebrick']
    cp = plt.contourf(lons,lats,da, clevs, colors=color,zorder=1)


    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #for BR
    ax.set_extent([-85, -30, -60, 15])
    ax.stock_img()
    ax.set_title(
                           'GFS'
                         + '\n'
                         + (name_file[14:17] if prev =='120' or prev =='144' or prev == '168' else name_file[14:16])
                         + 'h 12Z'
                         + '\n'
                         + ' ',
                         fontsize=18
    )

    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')

    title = umidade + '_'+ (name_file[14:17] if prev =='120' or prev =='144' or prev == '168' else name_file[14:16]) + 'h_12Z_.png'

    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    return





def plotaMERGE(anomes):

  path = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
  path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
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
  ax.coastlines(resolution='110m')
  ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
  #for BR
  ax.set_extent([-83, -34, -47.5, 10])
  ax.stock_img()
  ax.set_title(
                         'MERGE'
                       + '\n'
                       + (name_file[14:17]) 
                       + ' 12Z'
                       + '\n'
                       + ' ',
                       fontsize=18
  )
  fig.colorbar(cp, orientation='horizontal',pad=0.05)
  fig.set_label('mm')
  title = umidade + '_'+ (name_file[14:17])  + '12Z_.png'
  plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
  print('Saved: {}'.format(title))
  return



def plotaDiff(previsao,anomes,tipoUmidade):
    prev = str(previsao)
    
    path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/"+ tipoUmidade +"/"
    name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

    path_2 = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
    name_file_2 = 'prec_'+anomes+'.nc'
    
    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   

  

    DS_NCEP = xr.open_dataset(path_1 + name_file_1)
    da_DS_NCEP = DS_NCEP.prec.mean('time')

    MERGE = xr.open_dataset(path_2 + name_file_2)
    da_merge = MERGE.prec.mean('time')

    
    da = (DS_NCEP.prec.mean('time') - MERGE.prec.mean('time'))
    #da = (MERGE.prec.mean('time') - DS_NCEP.prec.mean('time'))
    #print(da)

    
    lons = DS_NCEP.variables['lon'][:]
    lats = DS_NCEP.variables['lat'][:]


    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
    clevs=[-50,-45,-40,-35,-30,-25,-20,-15,-10,0,10,15,20,25,30,35,40]
    ax = plt.axes(projection=ccrs.PlateCarree())
    cp = plt.contourf(lons,lats,da,clevs, zorder=1)
#
#
    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #for BR
    ax.set_extent([-83, -34, -47.5, 10])
    ax.stock_img()
    ax.set_title(
                           'Brazilian Global Atmospheric Model (BAM)'
                         + '\n'
                         + 'Diff' 
                         + '\n'
                         + 'MERGE'
                         + ' - ' 
                         + 'BAM GL' 
                         + '\n'
                         + prev 
                         + 'h 12Z'
                         + '\n',
                         fontsize=18
    )

    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')
    
    title = 'diff_'+ prev +'h_newLevel_'+ tipoUmidade +'.png'

    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    return

################anomes = '201401'
################
################for prev in range(24,192,24):
################	plotaNovaUmidade(prev)
##########################
################	plotaUmidadeGL(prev)
##########################
################	plotaGFS(prev)
################
################plotaMERGE(anomes)

#prev = 168
#plotaNovaUmidade(prev)
#plotaUmidadeGL(prev)
#plotaGFS(prev)



#umidade_GL
#umidade_Nova
#tipoUmidade = 'umidade_Nova'
#tipoUmidade = ['umidade_GL','umidade_Nova']

##anomes = '201401'
prev = '24'
tipoUmidade = ['umidade_GL','umidade_Nova']
for ind in tipoUmidade:
  for prev in range(24,192,24):
    anomes = '201401'
    print("ind: ",ind)

    plotaDiff(prev,anomes,ind)
##
##for prev in range(24,192,24):
##
##  plotaNovaUmidade(prev)
##  plotaUmidadeGL(prev)
##  plotaGFS(prev)

###plotaMERGE(anomes)


def serieTemporal(prev):
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
  #plot(linestyle='dashed',color='g', linewidth=2, marker='o',markersize=10) 
  #slice(180,-1), lon=slice(-75,-65)
  #sns.set()
  #sns.set_style('white', {"xtick.major.size": 2, "ytick.major.size": 2})
  #plt.tight_layout()
  sns.set_style("darkgrid", {"axes.facecolor": ".9"})
  sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

  fig=plt.figure()
  plt.tight_layout()

  plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Com 3 casas decimais
  plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
  plt.gca().xaxis.set_major_formatter(DateFormatter("%y-%m-%d"))

  

  plt.figtext(.5,.96,'Série Temporal', fontsize=30, ha='center')
  plt.figtext(.5,.90,'Janeiro/2014',fontsize=20,ha='center')
  plt.figtext(.15,.90,'Previsão 24h 12Z',fontsize=20,ha='left')
  plt.figtext(.86,.90,'Região: NORTE   B7',fontsize=20,ha='right')

  #plt.title('Série Temporal \n Janeiro/2014 \n Região: NORTE \n B7',fontsize=20, pad=30)


  DS_NCEP = xr.open_dataset(path_1 + name_file_1)

  longName = DS_NCEP.prec.attrs['long_name']
  print('atributos',longName)

  DS_NCEP.prec.isel(lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon").plot(color='orange', label='umidade GL')

  #p1 = DS_NCEP.prec.isel(lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon")
  #plt.plot(p1,color='orange', label='umidade GL')

  DS_NCEP_umidade_nova = xr.open_dataset(path_3 + name_file_3)
  DS_NCEP_umidade_nova.isel(lat=slice(2,-11), lon=slice(-75,-65)).prec.mean(dim="lat").mean(dim="lon").plot(color='r', label='Nova umidade')
  #
  GFS = xr.open_dataset(path_4 + name_file_4)
  GFS.APCP_surface.isel(lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon").plot(color='g', label='GFS')
  #
  MERGE = xr.open_dataset(path_2 + name_file_2)
  MERGE.prec.isel(lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon").plot(color='dodgerblue', label='MERGE', linewidth=2)
  
  plt.ylabel(longName[8:30], labelpad=30)
  plt.xlabel('Dia', labelpad=30)
  
  title = 'teste_'+ prev +'.png'
  plt.legend(fontsize=17, frameon=True)
  plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300, figsize=(15,15))
  print('Saved: {}'.format(title))
  return

#var= 'prec'
#prev = '24'
#serieTemporal(prev)


#def plotLatLon(var,prev):
#  path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
#  name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
#  path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   
#
#  DS_NCEP = xr.open_dataset(path_1 + name_file_1)  
#
#  lati = 41.4; loni = -100.8
#  dsloc = DS_NCEP.sel(lon=loni, lat=lati, method='nearest')
#
#  # select a variable to plot
#  dsloc[var].plot()
#  title = 'testevv_.png'
#  plt.legend(fontsize=17, frameon=True)
#  plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300, figsize=(15,15))
#  print('Saved: {}'.format(title))
#  return
#
#var= 'prec'
#prev = '24'
#plotLatLon(var,prev)
#serieTemporal(prev)