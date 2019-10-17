import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
#import xesmf as xe
import cartopy.crs as ccrs
import pandas as pd
import cartopy
#import wrf
from sys import exit

#ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-08-02*.nc", engine="pynio")
ds = xr.open_mfdataset("/dados/dmdpesq/CATT-BRAMS/profile_2018*.nc", engine="pynio")
wc_precip = ds['precip'].groupby('time.month').mean('time')
ds.close()
print(wc_precip)
print("OK precip")

#exit(0)
#wc = np.divide(wc_precip[0],wc_precip[1])
#wc = np.power(wc_precip[0],wc_precip[1])
#wc = np.true_divide(wc_precip[0],wc_precip[1])
wc = (wc_precip[0] + wc_precip[1])/2
print(wc)

#exit(0)
fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
ax = plt.axes(projection=ccrs.PlateCarree())

clevs=[-70,2,4,6,8,10,12,14,16,18,70]
color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
         'orange','goldenrod','red','firebrick']

lats = ds['lat' ][:]
lons = ds['lon'][:]
cp = plt.contourf(lons,lats,wc, clevs, colors=color,zorder=1)

ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.coastlines(resolution='110m')

ax.add_feature(cartopy.feature.LAND,  linewidth=.001)
ax.add_feature(cartopy.feature.OCEAN)

ax.set_extent([-95, -15, -60, 15])
ax.stock_img()
ax.set_title(
                       'BRAMS' 
                     + '\n' 
                     + 'Mean Agosto + Setembro/2018'
                     + '\n'
                     + '',
                     fontsize=18
)

fig.colorbar(cp, orientation='horizontal',pad=0.05)
fig.set_label('mm')

title = "BRAMS_20180809_precip.png"

plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
print('Saved: {}'.format(title))





