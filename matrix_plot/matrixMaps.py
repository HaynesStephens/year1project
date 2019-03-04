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

row_frac_land =         {'var':'frac_land',      'ylabel':'Land \n Fraction'}
row_net_rad_planet =    {'var':'net_rad_planet', 'ylabel':'Net \n Planet \n Radiation'}
row_tsurf=              {'var':'tsurf',          'ylabel':'Surface \n Temperature'}
row_snowicefr =         {'var':'snowicefr',      'ylabel':'Snow/Ice \n Fraction'}
row_ZSI =               {'var':'ZSI',            'ylabel':'Sea Ice \n Thickness'}
row_lwp =               {'var':'lwp',            'ylabel':'Liquid Water \n Path'}
row_swcrf_toa =         {'var':'swcrf_toa',      'ylabel':'SW Cloud \n Rad Forcing'}
row_lwcrf_toa =         {'var':'lwcrf_toa',      'ylabel':'LW Cloud \n Rad Forcing'}
row_pcldt =             {'var':'pcldt',          'ylabel':'Total Cloud \n Coverage'}
row_pscld =             {'var':'pscld',          'ylabel':'Shallow Convective \n Cloud Cover'}
row_pdcld =             {'var':'pdcld',          'ylabel':'Deep Convective \n Cloud Cover'}
row_wtrcld =            {'var':'wtrcld',         'ylabel':'Water \n Cloud Cover'}
row_icecld =            {'var':'icecld',         'ylabel':'Ice \n Cloud Cover'}
row_list = [row_frac_land, row_lwp, row_swcrf_toa, row_pscld]

col_0 = {'filedir':filedir0, 'parallels':[-45, 45],
        'meridians':[-90, 90], 'title':'Dynamic (5L), Aquaplanet'}
col_1 = {'filedir':filedir1, 'parallels':[-45, -10, 10, 45],
        'meridians':[-90, -12.5, 12.5, 90], 'title':'Dynamic (5L), 1% SS Cont'}
col_4 = {'filedir':filedir4, 'parallels':[-45, -14, 14, 45],
        'meridians':[-90, -27.5, 27.5, 90], 'title':'Dynamic (5L), 4% SS Cont'}
col_6 = {'filedir':filedir6, 'parallels':[-45, -18, 18, 45],
        'meridians':[-90, -32.5, 32.5, 90], 'title':'Dynamic (5L), 6% SS Cont'}
col_11 = {'filedir':filedir11, 'parallels':[-45, -22, 22, 45],
        'meridians':[-90, -47.5, 47.5, 90], 'title':'Dynamic (5L), 11% SS Cont'}
col_22 = {'filedir':filedir22, 'parallels':[-45, -34, 34, 45],
        'meridians':[-90, -67.5, 67.5, 90], 'title':'Dynamic (5L), 22% SS Cont'}
col_26 = {'filedir':filedir26, 'parallels':[-45, -38, 38, 45],
        'meridians':[-90, -72.5, 72.5, 90], 'title':'Dynamic (5L), 26% SS Cont'}
col_34 = {'filedir':filedir34, 'parallels':[-45, -42, 42, 45],
        'meridians':[-90, -87.5, 87.5, 90], 'title':'Dynamic (5L), 34% SS Cont'}
col_39 = {'filedir':filedir39, 'parallels':[-45, -46, 46, 45],
        'meridians':[-90, -92.5, 92.5, 90], 'title':'Dynamic (5L), 39% SS Cont'}

col_list = [col_6, col_26]


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

    print(np.max(data), np.min(data))

    m.colorbar(mappable=cs, ax=ax)
    if row_num==0:
        ax.set_title(title, fontsize=7)
    if col_num==0:
        ax.set_ylabel(ylabel, fontsize=7, labelpad = 40, rotation=0)


fig, axes = plt.subplots(len(row_list), len(col_list), figsize = (10,7))

for col_num in range(len(col_list)):
    for row_num in range(len(row_list)):
        col = col_list[col_num]
        row = row_list[row_num]
        filedir = col['filedir']
        var = row['var']
        data = avgDataFiles(filedir, var, num_files = 10)
        makeSubplot(data, ax=axes[row_num, col_num], row_num=row_num, col_num=col_num, ylabel=row['ylabel'],
                    parallels=col['parallels'], meridians=col['meridians'], title=col['title'])


fig.tight_layout()
plt.savefig('matrix_basemap_big_clouds.svg')
plt.savefig('matrix_basemap_big_clouds.pdf')
plt.show()
