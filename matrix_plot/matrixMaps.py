from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
import os
from lat_lon_grid import lat_grid, lon_grid

filebase='/project2/abbot/haynes/ROCKE3D_output/'
filename0=filebase+'pc_proxcenb_ssc5L_TL_500yr_rs2/AN82941-2950.aijpc_proxcenb_ssc5L_TL_500yr_rs2.nc'
filename1=filebase+'pc_proxcenb_aqua5L_TL_500yr_rs2/AN82941-2950.aijpc_proxcenb_aqua5L_TL_500yr_rs2.nc'
filename2=filebase+'pc_proxcenb_ssc5L_TL_11p/ANM3040-3049.accpc_proxcenb_ssc5L_TL_11p.nc'

row0 = {'row_num':0, 'var':'frac_land',      'ylabel':'Land \n Fraction'}
row1 = {'row_num':1, 'var':'net_rad_planet', 'ylabel':'Net \n Planet \n Radiation'}
row2 = {'row_num':2, 'var':'tsurf',          'ylabel':'Surface \n Temperature'}
row3 = {'row_num':3, 'var':'snowicefr',      'ylabel':'Snow/Ice \n Fraction'}
row4 = {'row_num':4, 'var':'ZSI',            'ylabel':'Sea Ice \n Thickness'}
row5 = {'row_num':5, 'var':'pcldt',            'ylabel':'Total Cloud \n Coverage'}
row_list = [row0, row1, row2, row3, row4, row5]

col0 = {'col_num':0, 'filename':filename0, 'parallels':[-45, -10, 10, 45],
        'meridians':[-45, -12.5, 12.5, 45], 'title':'Dynamic (5L), 1% SS Cont'}
col1 = {'col_num':1, 'filename':filename1, 'parallels':[-45, -10, 10, 45],
        'meridians':[-45, -12.5, 12.5, 45], 'title':'Dynamic (5L), Aquaplanet'}
col2 = {'col_num':2, 'filename':filename2, 'parallels':[-10, 10],
        'meridians':[-12.5, 12.5], 'title':'Dynamic (5L), 1% SS Cont'}
# col3 = {'col_num':3, 'filename':filename3, 'parallels':[-10, 10],
#         'meridians':[-12.5, 12.5], 'title':'Dynamic (5L), 1% SS Cont'}
col_list = [col0, col1]


def avgDataFiles(filedir, var):
    results = [each for each in os.listdir(filedir) if 'acc' in each][-10:]
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:]
        arr_tot = arr_tot + arr
    arr_avg = arr_tot / 10
    return arr_avg



def makeSubplot(ax, row_num, col_num, var, ylabel, parallels, meridians, title):
    data = nc[var][:]
    if title == 'Dynamic (5L), Aquaplanet':
        data = np.roll(data, (data.shape[1])//2, axis=1)
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
    m.colorbar(mappable=cs, ax=ax)
    if row_num==0:
        ax.set_title(title, fontsize=7)
    if col_num==0:
        ax.set_ylabel(ylabel, fontsize=7, labelpad = 40, rotation=0)


fig, axes = plt.subplots(len(row_list), len(col_list), figsize = (10,7))

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
