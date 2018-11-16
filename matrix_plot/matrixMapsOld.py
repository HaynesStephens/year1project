from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from lat_lon_grid import lat_grid, lon_grid
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,7))

m = Basemap(projection='geos',
            rsphere=(6378137.00,6356752.3142),
            resolution='l',
            area_thresh=10000.,
            lon_0=0,
            satellite_height=7255000000,
            ax = ax1)
m.drawcoastlines()
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
# m.drawparallels(lat_grid[::2]+2, ax = ax1)
# m.drawmeridians(lon_grid[::2] +2.5, ax = ax1)
m.drawparallels([-10, 10], ax = ax1)
m.drawmeridians([-12.5, 12.5], ax = ax1)
# m.drawmapboundary(fill_color='aqua')
m.scatter(0,0,20,marker='o',color='k', latlon=True, ax = ax1)
ax1.set_title("Land Fraction (Day Side)")

filedir='/Users/haynesstephens1/uchi/research/year1/pulled_data/pc_proxcenb_ssc5L_TL_500yr/'
filename=filedir+'D+J2440.aijpc_proxcenb_ssc5L_TL_500yr.nc'

nc = ds(filename, 'r+', format='NETCDF4')
data = nc['frac_land'][:]

data1 = data[:,18:-18]
ny=data1.shape[0]
nx=data1.shape[1]
lons, lats = m.makegrid(nx, ny)
print(lons)
print(lons.shape)
x, y = m(lons, lats)
print(x)
print(x.shape)
cs = m.contourf(x,y,data1, ax=ax1)

m = Basemap(projection='geos',
            rsphere=(6378137.00,6356752.3142),
            resolution='l',
            area_thresh=10000.,
            lon_0=180,
            satellite_height=7255000000,
            ax = ax2)
m.drawcoastlines()
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(lat_grid[::1]+2, ax = ax2)
m.drawmeridians(lon_grid[::1]+2.5, ax = ax2)
data2 = np.append(data[:,-18:], data[:,:18], axis=1)
ny=data2.shape[0]
nx=data2.shape[1]
lons, lats = m.makegrid(nx, ny)
x, y = m(lons, lats)
cs = m.contourf(x,y,data2, ax=ax2)
ax2.set_title("Land Fraction (Night Side)")


plt.show()
plt.savefig(filedir + 'basemap_old.svg')
