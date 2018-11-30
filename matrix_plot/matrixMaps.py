from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from lat_lon_grid import lat_grid, lon_grid

filebase='/project2/abbot/haynes/ROCKE3D_output/'
filename1=filebase+'pc_proxcenb_ssc5L_TL_500yr_rs2/AN82941-2950.aijpc_proxcenb_ssc5L_TL_500yr_rs2.nc'
filename2=filebase+'pc_proxcenb_aqua5L_TL_500yr_rs2/AN82941-2950.aijpc_proxcenb_aqua5L_TL_500yr_rs2.nc'

row0 = {'row_num':0, 'var':'frac_land',      'ylabel':'Land \n Fraction'}
row1 = {'row_num':1, 'var':'net_rad_planet', 'ylabel':'Net \n Planet \n Radiation'}
row2 = {'row_num':2, 'var':'tsurf',          'ylabel':'Surface \n Temperature'}
row3 = {'row_num':3, 'var':'snowicefr',      'ylabel':'Snow/Ice \n Fraction'}
row4 = {'row_num':4, 'var':'ZSI',            'ylabel':'Sea Ice \n Thickness'}
row_list = [row0, row1, row2, row3, row4]

col0 = {'col_num':0, 'filename':filename1, 'parallels':[-10, 10],
        'meridians':[-12.5, 12.5], 'title':'Dynamic Ocean, 1% SS Continent'}
col1 = {'col_num':1, 'filename':filename1, 'parallels':[-10, 10],
        'meridians':[-12.5, 12.5], 'title':'Dynamic Ocean, 1% SS Continent'}
col2 = {'col_num':2, 'filename':filename1, 'parallels':[-10, 10],
        'meridians':[-12.5, 12.5], 'title':'Dynamic Ocean, 1% SS Continent'}
col3 = {'col_num':3, 'filename':filename1, 'parallels':[-10, 10],
        'meridians':[-12.5, 12.5], 'title':'Dynamic Ocean, 1% SS Continent'}
col_list = [col0, col1, col2, col3]


def makeSubplot(ax, row_num, col_num, var, ylabel, parallels, meridians, title):
    data = nc[var][:]
    m = Basemap(ax = ax)
    m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(parallels, labels=[1,0,0,0], ax = ax, fontsize=4)
    merdians_drawn = m.drawmeridians(meridians, labels=[0,0,0,1], ax = ax, rotation=45, fontsize=4)
    ny=data.shape[0]
    nx=data.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)
    cs = m.contourf(x,y,data, ax=ax)
    if row_num==0:
        ax.set_title(title, fontsize=7)
    if col_num==0:
        ax.set_ylabel(ylabel, fontsize=7, labelpad = 40, rotation=0)


fig, axes = plt.subplots(5, 4, figsize = (8,7))

for col in col_list:
    for row in row_list:
        filename = col['filename']
        nc = ds(filename, 'r+', format='NETCDF4')
        row_num = row['row_num']
        col_num = col['col_num']
        makeSubplot(ax=axes[row_num, col_num], row_num=row_num, col_num=col_num, var=row['var'],
                    ylabel=row['ylabel'], parallels=col['parallels'], meridians=col['meridians'],
                    title=col['title'])


fig.tight_layout()
plt.savefig('matrix_basemap.svg')
plt.savefig('matrix_basemap.pdf')
plt.show()
