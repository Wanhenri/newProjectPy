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
ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-08-*RAINC.nc", engine="pynio")
wc_RAINC = ds['RAINC'].groupby('XTIME.month').mean('XTIME')
ds.close()
print("OK RAINC")
ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-08-*RAINNC.nc", engine="pynio")
wc_RAINNC = ds['RAINNC'].groupby('XTIME.month').mean('XTIME')
ds.close()
print("OK RAINNC")

wc = wc_RAINC + wc_RAINNC 

print(wc)

fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
ax = plt.axes(projection=ccrs.PlateCarree())
#clevs=[-70,1,2,4,6,8,10,12,14,16,18,19,20,25,30,40,50,60,70,80,100,120]
#color=['white','white','dodgerblue','dodgerblue','darkturquoise','darkturquoise','mediumspringgreen','mediumspringgreen','lime','lime','yellow','yellow','orange','orange','goldenrod','goldenrod','red','red','firebrick','firebrick']

clevs=[-70,2,4,6,8,10,12,14,16,18,70]
color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
         'orange','goldenrod','red','firebrick']

lats = ds['XLAT' ][:]
lons = ds['XLONG'][:]
cp = plt.contourf(lons,lats,wc[0], clevs, colors=color,zorder=1)

ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.coastlines(resolution='110m')

ax.add_feature(cartopy.feature.LAND,  linewidth=.001)
ax.add_feature(cartopy.feature.OCEAN)

ax.set_extent([-95, -15, -60, 15])
ax.stock_img()
ax.set_title(
                       'WRF' 
                     + '\n' 
                     + '201808'
                     + '\n'
                     + '',
                     fontsize=18
)

fig.colorbar(cp, orientation='horizontal',pad=0.05)
fig.set_label('mm')

title = 'WRF_201808_RAINC_RAINNC.png'

plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
print('Saved: {}'.format(title))






#Dates = pd.date_range(start="2018-08-01 00:00:00", periods=48, freq="1H")
#datesextension = Dates.format(formatter=lambda x: x.strftime('%Y-%m-%d_%H:%M:%S'))
#datesday = Dates.format(formatter=lambda x: x.strftime('%d'))

#clevs=[-70,2,4,6,8,10,12,14,16,18,70]
#clevs=[-70,1,2,4,6,8,10,12,14,16,18,19,20,25,30,40,50,60,70,80,100,120]
##clevs=[-120,1,5,10,15,20,25,30,35,40,50,60,80,100,120]
#color=['white','white','dodgerblue','dodgerblue','darkturquoise','darkturquoise','mediumspringgreen','mediumspringgreen','lime','lime','yellow','yellow','orange','orange','goldenrod','goldenrod','red','red','firebrick','firebrick']
#color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow','orange','goldenrod','red','firebrick']
#color=['white',(0.0,0.0,0.0),
#       (0.180,0.50,0.20),
#       (0.255,0.145,0.65),
#       (0.255,0.215,0.80),
#       (0.255,0.240,0.180),
#       (0.230,0.255,0.230),
#       (0.170,0.230,0.180),
#       (0.130,0.250,0.170),
#       (0.110,0.230,0.110),
#       (0.55,0.210,0.60),
#       (0.6,0.190,0.10),
#       (0.5,0.140,0.0),
#       (0.0,0.80,0.0),
#       (0.0,0.50,0.0),
#       (0.0,0.35,0.0)]
