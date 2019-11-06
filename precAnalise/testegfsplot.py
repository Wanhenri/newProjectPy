import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from sys import exit
from matplotlib import cm
import cartopy

def plotaGFS(previsao):
    prev = str(previsao)
    path = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"
    #name_file = 'JAN2014_'+ prev +'Z_12Z.nc'
    name_file = 'prev.2014.jan_SHTFL_12z_'+ prev +'h_interp.nc'

    print(name_file[24:26])
    #exit(0)

    umidade = 'GFS'
    text = 'Condição inicial:' + umidade

    GFS = xr.open_dataset(path + name_file)
    
    da = GFS.SHTFL_surface.mean('time')
    
    lons = GFS.variables['lon'][:]
    lats = GFS.variables['lat'][:]


    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)

    ax = plt.axes(projection=ccrs.PlateCarree())
    clevs=[-100,-85,-70,-55,-40,-25,-10,0,10,25,40,55,70,85,100,115,130,145,160,175,190,205,220,235,250]
    #clevs=[0,150,300,450,600,750]
    cp = plt.contourf(lons,lats,da, clevs, cmap=cm.rainbow,zorder=1)
    #cp = plt.contourf(lons,lats,da,  cmap=cm.rainbow,zorder=1)


    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #ax.add_feature(cartopy.feature.OCEAN, zorder=100, facecolor='white',linestyle=':')
    
    #for BR
    #ax.set_extent([-85, -30, -60, 15])
    ax.set_extent([-83, -34, -47.5, 10])
    ax.stock_img()
    ax.set_title(
                           'GFS'
                         + '\n'
                         + (name_file[24:27] if prev =='120' or prev =='144' or prev == '168' else name_file[24:26])
                         + 'h 12Z'
                         + '\n'
                         + ' ',
                         fontsize=18
    )

    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')

    title = umidade + '_'+ (name_file[24:27] if prev =='120' or prev =='144' or prev == '168' else name_file[24:26]) + 'h_12Z__SHTFL_interp_teste2.png'

    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))
    plt.close()
    GFS.close()
    
    return

for prev in range(24,48,24):

  plotaGFS(prev)