import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import cartopy

import locale


from sys import exit

from datetime import date, datetime, time

import seaborn as sns
from matplotlib import pylab

import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
 
from matplotlib.ticker import StrMethodFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator

##config = {
##     'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
##     'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
##     'latNorte':[156   ,170        ,169            ,3          ,2          ,165        ,2          ],
##     'latSul'  :[-35   ,-24        ,-35            ,-11        ,-11        ,-24        ,-11        ],
##     'lonOeste':[-65   ,-49        ,-65            ,-51        ,-65        ,-51        ,-75        ],
##     'lonLest' :[-49   ,-39        ,-49            ,-34        ,-49        ,-39        ,-65        ]
##  }

config = {
     'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
     'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
     'latNorte':[ 75   ,130        ,130            ,195        ,195        ,130        ,195          ],
     'latSul'  :[-182  ,-119       ,-119           ,-45        ,-45        ,-139       ,-45        ],
     'lonOeste':[-157  ,-78        ,-157           ,-79        ,-157       ,-78        ,-210        ],
     'lonLest' :[-69   ,-1         ,-79            ,-1         ,-79        ,-1        ,-153        ]
  }


latNorte    = config['latNorte'][6]
latSul      = config['latSul'][6]
lonOeste    = config['lonOeste'][6]
lonLest     = config['lonLest'][6]

ds = xr.open_mfdataset("/dados/dmdpesq/WRF-Chem/wrfout_d01_2018-08-*RAINC_interp.nc", engine="pynio")
wc_RAINC = ds['RAINC'].isel(lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).groupby('XTIME.day').mean('XTIME')

print(wc_RAINC)
#exit(0)

fig, ax = plt.subplots(111,figsize=(15,15), dpi=200)
ax = plt.axes(projection=ccrs.PlateCarree())
#clevs=[-70,1,2,4,6,8,10,12,14,16,18,19,20,25,30,40,50,60,70,80,100,120]
#color=['white','white','dodgerblue','dodgerblue','darkturquoise','darkturquoise','mediumspringgreen','mediumspringgreen','lime','lime','yellow','yellow','orange','orange','goldenrod','goldenrod','red','red','firebrick','firebrick']



clevs=[-70,2,4,6,8,10,12,14,16,18,70]
color=['white','dodgerblue','darkturquoise','mediumspringgreen','lime','yellow',
         'orange','goldenrod','red','firebrick']

lats = wc_RAINC['lat' ][:]
lons = wc_RAINC['lon'][:]
cp = plt.contourf(lons,lats,wc_RAINC[0], clevs, colors=color,zorder=1)

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

title = 'teste-slice.png'

plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
print('Saved: {}'.format(title))