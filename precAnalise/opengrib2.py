import warnings
warnings.filterwarnings("ignore")
#import cartopy.crs as ccrs
import xarray as xr
#import matplotlib.pyplot as plt
#import seaborn as sns
#from matplotlib import pylab
#import pandas as pd
#import numpy as np
#import datetime
#from datetime import datetime
#import matplotlib.dates as mdates
#from matplotlib.dates import DateFormatter
 
#from matplotlib.ticker import StrMethodFormatter, MultipleLocator, FormatStrFormatter, AutoMinorLocator

ds = xr.open_mfdataset("/dados/dmdpesq/Proj_GFS/etapa1/12/gfs.t12z.pgrb2f24.201401??12_SPFH.grib2", engine="pynio")
#print(ds)

#path_5 = "/dados/dmdpesq/Proj_GFS/GFS/201401/0212/"    
#name_file_5 = 'gfs.t12z.pgrb2f06.2014010212.grib2'
#
#GFS= xr.open_dataset(path_5 + name_file_5,engine='pynio')
##print(GFS)
#da = GFS.APCP_P8_L1_GLL0_acc
##da = GFS.APCP_P8_L1_GLL0_acc6h
#print(da)
#
##lons = GFS.variables['longitude'][:]
#lats = GFS.variables['latitude'][:]



#p1 = DS_NCEP.prec.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
#plt.plot(xTickTime,p1,color='orange', label='OPER')
#plt.xticks(rotation=45) 