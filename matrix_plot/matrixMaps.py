from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.patches import Polygon
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
row_lwp =               {'var':'lwp',            'ylabel':'Liquid \n Water \n Path'}
row_swcrf_toa =         {'var':'swcrf_toa',      'ylabel':'SW \n Cloud \n Rad \n Forcing'}
row_lwcrf_toa =         {'var':'lwcrf_toa',      'ylabel':'LW \n Cloud \n Rad \n Forcing'}
row_pcldt =             {'var':'pcldt',          'ylabel':'Total Cloud \n Coverage'}
row_pscld =             {'var':'pscld',          'ylabel':'Shallow \n Convective \n Cloud \n Cover'}
row_pdcld =             {'var':'pdcld',          'ylabel':'Deep \n Convective \n Cloud \n Cover'}
row_wtrcld =            {'var':'wtrcld',         'ylabel':'Water \n Cloud Cover'}
row_icecld =            {'var':'icecld',         'ylabel':'Ice \n Cloud Cover'}
row_list = [row_frac_land, row_lwp, row_swcrf_toa, row_pscld]

col_0 = {'filedir':filedir0, 'parallels':[0],
        'meridians':[0], 'title':'Dynamic (5L), Aquaplanet'}
col_1 = {'filedir':filedir1, 'parallels':[-10, 10],
        'meridians':[-12.5, 12.5], 'title':'Dynamic (5L), 1% SS Cont'}
col_4 = {'filedir':filedir4, 'parallels':[-14, 14],
        'meridians':[-27.5, 27.5], 'title':'Dynamic (5L), 4% SS Cont'}
col_6 = {'filedir':filedir6, 'parallels':[-20, 20],
        'meridians':[-35, 35], 'title':'Dynamic (5L), 6% SS Cont'}
col_11 = {'filedir':filedir11, 'parallels':[-22, 22],
        'meridians':[-47.5, 47.5], 'title':'Dynamic (5L), 11% SS Cont'}
col_22 = {'filedir':filedir22, 'parallels':[-34, 34],
        'meridians':[-67.5, 67.5], 'title':'Dynamic (5L), 22% SS Cont'}
col_26 = {'filedir':filedir26, 'parallels':[-40, 40],
        'meridians':[-75, 75], 'title':'Dynamic (5L), 26% SS Cont'}
col_34 = {'filedir':filedir34, 'parallels':[-42, 42],
        'meridians':[-87.5, 87.5], 'title':'Dynamic (5L), 34% SS Cont'}
col_39 = {'filedir':filedir39, 'parallels':[-46, 46],
        'meridians':[-92.5, 92.5], 'title':'Dynamic (5L), 39% SS Cont'}

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
    if title == 'Dynamic (5L), Aquaplanet':
        data = np.roll(data, (data.shape[1])//2, axis=1)
    m = Basemap(ax = ax)
    # m.drawcoastlines()
    # m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(parallels, labels=[1,0,0,0], ax = ax, fontsize=8)
    m.drawmeridians(meridians, labels=[0,0,0,1], ax = ax, rotation=45, fontsize=8)

    print(row_num)
    print(col_num)
    print(parallels)
    print(meridians)

    x1, y1 = m(meridians[0], parallels[0])
    x2, y2 = m(meridians[0], parallels[1])
    x3, y3 = m(meridians[1], parallels[1])
    x4, y4 = m(meridians[1], parallels[0])
    poly = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none', edgecolor='black', linewidth=1)
    plt.gca().add_patch(poly)

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

for col_num in range(len(col_list)):
    col = col_list[col_num]
    filedir = col['filedir']
    for row_num in range(len(row_list)):
        row = row_list[row_num]
        var = row['var']
        data = avgDataFiles(filedir, var, num_files = 10)
        makeSubplot(data, ax=axes[row_num, col_num], row_num=row_num, col_num=col_num, ylabel=row['ylabel'],
                    parallels=col['parallels'], meridians=col['meridians'], title=col['title'])


fig.tight_layout()
plt.savefig('matrix_basemap_big_clouds.svg')
plt.savefig('matrix_basemap_big_clouds.pdf')
plt.show()
