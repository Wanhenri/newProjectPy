import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt

import cartopy

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
    plt.close()
    GFS.close()
    
    return

for prev in range(24,192,24):

  plotaGFS(prev)