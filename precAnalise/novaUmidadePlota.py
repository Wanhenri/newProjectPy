import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt

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
    plt.close()
    return 

for prev in range(24,192,24):

  plotaNovaUmidade(prev)