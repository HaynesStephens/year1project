from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
# from lat_lon_grid import lat_grid, lon_grid

filebase='/project2/abbot/haynes/ROCKE3D_output/'
filedir0=filebase+'pc_proxcenb_aqua5L_TL_500yr_rs2'
filedir1=filebase+'pc_proxcenb_ssc5L_TL_500yr_rs2'
filedir4=filebase+'pc_proxcenb_ssc5L_TL_4p'
filedir6=filebase+'pc_proxcenb_ssc5L_TL_6p'
filedir11=filebase+'pc_proxcenb_ssc5L_TL_11p'
filedir22=filebase+'pc_proxcenb_ssc5L_TL_22p'
filedir26=filebase+'pc_proxcenb_ssc5L_TL_26p'
filedir34=filebase+'pc_proxcenb_ssc5L_TL_34p'
filedir39=filebase+'pc_proxcenb_ssc5L_TL_39p'

row0 = {'row_num':0, 'var':'frac_land',      'ylabel':'Land \n Fraction'}
row1 = {'row_num':1, 'var':'net_rad_planet', 'ylabel':'Net \n Planet \n Radiation'}
row2 = {'row_num':2, 'var':'tsurf',          'ylabel':'Surface \n Temperature'}
row3 = {'row_num':3, 'var':'snowicefr',      'ylabel':'Snow/Ice \n Fraction'}
row4 = {'row_num':4, 'var':'ZSI',            'ylabel':'Sea Ice \n Thickness'}
row5 = {'row_num':5, 'var':'pcldt',            'ylabel':'Total Cloud \n Coverage'}
row_list = [row0, row1, row2, row3, row4, row5]

col0 = {'col_num':0, 'filedir':filedir0, 'parallels':[-45, 45],
        'meridians':[-90, 90], 'title':'Dynamic (5L), Aquaplanet'}
col1 = {'col_num':1, 'filedir':filedir1, 'parallels':[-45, -10, 10, 45],
        'meridians':[-90, -12.5, 12.5, 90], 'title':'Dynamic (5L), 1% SS Cont'}
col4 = {'col_num':2, 'filedir':filedir4, 'parallels':[-45, -14, 14, 45],
        'meridians':[-90, -27.5, 27.5, 90], 'title':'Dynamic (5L), 4% SS Cont'}
col6 = {'col_num':0, 'filedir':filedir6, 'parallels':[-45, -18, 18, 45],
        'meridians':[-90, -32.5, 32.5, 90], 'title':'Dynamic (5L), 6% SS Cont'}
col11 = {'col_num':1, 'filedir':filedir11, 'parallels':[-45, -22, 22, 45],
        'meridians':[-90, -47.5, 47.5, 90], 'title':'Dynamic (5L), 11% SS Cont'}
col22 = {'col_num':2, 'filedir':filedir22, 'parallels':[-45, -34, 34, 45],
        'meridians':[-90, -67.5, 67.5, 90], 'title':'Dynamic (5L), 22% SS Cont'}
col26 = {'col_num':3, 'filedir':filedir26, 'parallels':[-45, -38, 38, 45],
        'meridians':[-90, -72.5, 72.5, 90], 'title':'Dynamic (5L), 26% SS Cont'}
col34 = {'col_num':2, 'filedir':filedir34, 'parallels':[-45, -42, 42, 45],
        'meridians':[-90, -87.5, 87.5, 90], 'title':'Dynamic (5L), 34% SS Cont'}
col39 = {'col_num':2, 'filedir':filedir39, 'parallels':[-45, -46, 46, 45],
        'meridians':[-90, -92.5, 92.5, 90], 'title':'Dynamic (5L), 39% SS Cont'}

col_list = [col6, col11, col22, col26]


def avgDataFiles(filedir, var, num_files = 10):
    results = glob('{0}/*aij*'.format(filedir))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:]
        arr_tot = arr_tot + arr
    arr_avg = arr_tot / num_files
    return arr_avg


def makeSubplot(data, ax, row_num, col_num, ylabel, parallels, meridians, title):
    # data = nc[var][:]
    if title == 'Dynamic (5L), Aquaplanet':
        data = np.roll(data, (data.shape[1])//2, axis=1)
    m = Basemap(ax = ax)
    # m.drawcoastlines()
    # m.fillcontinents(color='coral',lake_color='aqua')
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
        filedir = col['filedir']
        row_num = row['row_num']
        col_num = col['col_num']
        var = row['var']
        data = avgDataFiles(filedir, var, num_files = 10)
        makeSubplot(data, ax=axes[row_num, col_num], row_num=row_num, col_num=col_num, ylabel=row['ylabel'],
                    parallels=col['parallels'], meridians=col['meridians'], title=col['title'])


fig.tight_layout()
plt.savefig('matrix_basemap_big.svg')
plt.savefig('matrix_basemap_big.pdf')
plt.show()
