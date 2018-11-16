from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from lat_lon_grid import lat_grid, lon_grid
f, ax1 = plt.subplots(1, 1)

filedir='/Users/haynesstephens1/uchi/research/year1/pulled_data/pc_proxcenb_ssc5L_TL_500yr/'
filename=filedir+'D+J2440.aijpc_proxcenb_ssc5L_TL_500yr.nc'
nc = ds(filename, 'r+', format='NETCDF4')

def makeSubplot(ax=ax1, var='frac_land', parallels=[-10, 10],
                meridians=[-12.5, 12.5], title="Land Fraction (Night Side)"):
    data = nc[var][:]
    m = Basemap(ax = ax)
    m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(parallels, ax = ax)
    m.drawmeridians(meridians, ax = ax)
    ny=data.shape[0]
    nx=data.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)
    cs = m.contourf(x,y,data, ax=ax)
    ax1.set_title(title)

makeSubplot(ax=ax1, var='frac_land', parallels=[-10, 10],
                meridians=[-12.5, 12.5], title="Land Fraction w/ Dynamic Ocean, 1% SS Continent")

plt.show()
plt.savefig(filedir + 'basemap.svg')
