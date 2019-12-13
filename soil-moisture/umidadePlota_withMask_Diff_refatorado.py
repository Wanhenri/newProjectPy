import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import cm

import cartopy

for index in range(1,9,1):
  print('index',index)

  for ind in range(2,3,1):
    print('ind',ind) 
    path1 = "/dados/dmdpesq/Experimento_umidade_do_solo/analiseUmidade/soilmvfm_20140112_interp.nc"
    path2 = "/dados/dmdpesq/Experimento_umidade_do_solo/analiseUmidade/SoilMoistureWeekly.201401_ldas2_4bam_12Z.nc"
    path3 = "/dados/dmdpesq/Experimento_umidade_do_solo/analiseUmidade/SoilMoistureWeekly.201401_ldas4bam_12Z.nc"

    path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/analiseUmidade/out/campoEspacial/" 

    DS_NCEP_OPER = xr.open_dataset(path1)
    Oper = DS_NCEP_OPER.soilm.mean('time').sel(lev=index) 
    DS_NCEP_OPER.close()

    DS_NCEP_LDAS1 = xr.open_dataset(path2)  
    LDAS1 = DS_NCEP_LDAS1.soilm.mean('time').sel(lev=index)
    lons = DS_NCEP_LDAS1.variables['lon'][:]
    lats = DS_NCEP_LDAS1.variables['lat'][:] 
    DS_NCEP_LDAS1.close()

    DS_NCEP_LDAS2 = xr.open_dataset(path3)    
    LDAS2 = DS_NCEP_LDAS2.soilm.mean('time').sel(lev=index) 
    DS_NCEP_LDAS2.close()

    #print("OPER: ",Oper)
    #print("LDAS1: ",LDAS1)
    #exit(0)

    if ind == 1:
        titleText = "Diff LDAS2 - OPER"
        titleText_file = "Diff_LDAS2-OPER"

        print("titleText: ", titleText, "ind: ", ind)

        da = LDAS2 - Oper
        

        print(titleText)
    
    elif ind == 2:
        titleText = "Diff LDAS1 - OPER"
        titleText_file = "Diff_LDAS1-OPER"
        
        print("titleText: ", titleText, "ind: ", ind)

        da = LDAS1 - Oper
       
        
        print(titleText)
    
    elif ind == 3:
        titleText = "Diff LDAS2 - LDAS1"
        titleText_file = "Diff_LDAS2-LDAS1"
        
        print("titleText: ", titleText, "ind: ", ind)

        da = LDAS2 - LDAS1
       
        
        print(titleText)
        
    else:
        print("!!!")
#    titleText_file = "Diff_LDAS2-LDAS1"
#    titleText = "Diff LDAS2 - LDAS1"
#    
#    da = LDAS2 - LDAS1
#    print(da)
    #exit(0)
    #lons = DS_NCEP_LDAS1.variables['lon'][:]
    #lats = DS_NCEP_LDAS1.variables['lat'][:]
    level = [0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05]
    fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
    ax = plt.axes(projection=ccrs.PlateCarree())
    clevs=level
    color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
           'orange','goldenrod','red','firebrick']
    #cp = plt.contourf(lons,lats,da[0], clevs, colors=color,zorder=1)
    #cp = plt.contourf(lons,lats,da, clevs, cmap=cm.rainbow,zorder=1)
    cp = plt.contourf(lons,lats,da,  cmap=cm.BrBG,zorder=1)
    #print(cp)
    #exit(0)
    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.OCEAN, zorder=100, facecolor='white',linestyle=':')
    #for BR
    #ax.set_extent([-85, -30, -60, 15])
    ax.set_extent([-83, -34, -47.5, 10])
    ax.stock_img()
    ax.set_title(
                          ' Experimentos: '
                         + titleText 
                         + '\n'
                         + 'nivel: '
                         + str(index)
                         + '\n' 
                         + '20140101 12Z ',
                         fontsize=18
    )
    fig.colorbar(cp, orientation='horizontal',pad=0.05)
    fig.set_label('mm')

    title = titleText_file + '_nivel_'+ str(index) +'_2014010112_withMask.png'
    plt.savefig(path_out + title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))      
    #DS_NCEP_OPER.close()
    #DS_NCEP_LDAS1.close()
    #DS_NCEP_LDAS2.close()
    plt.cla() #means clear current axis
    plt.clf() #means clear current figure
    plt.close('all')


