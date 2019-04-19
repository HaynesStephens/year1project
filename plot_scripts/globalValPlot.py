from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.patches import Polygon
from cbar import MidPointNorm
# from matplotlib.colors import from_levels_and_colors,  LinearSegmentedColormap, rgb2hex


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

row_frac_land =         {'var':'frac_land',      'title':'Land Fraction',                  'units': '[%]'}
row_evap =              {'var':'evap',           'title':'Evaporation',                    'units': '[mm/day]'}
row_net_rad_planet =    {'var':'net_rad_planet', 'title':'Net Planet Radiation',           'units': '[Wm$^{-2}$]'}
row_tsurf =             {'var':'tsurf',          'title':'Surface Temperature',            'units': '[$^{\circ}$C]'}
row_snowicefr =         {'var':'snowicefr',      'title':'Snow/Ice Fraction',              'units': '[%]'}
row_ZSI =               {'var':'ZSI',            'title':'Sea Ice Thickness',              'units': '[m]'}
row_lwp =               {'var':'lwp',            'title':'Liquid Water Path',              'units': '[0.1kgm$^{-2}$]'}
row_swcrf_toa =         {'var':'swcrf_toa',      'title':'SW Cloud Rad Forcing',           'units': '[Wm$^{-2}$]'}
row_lwcrf_toa =         {'var':'lwcrf_toa',      'title':'LW Cloud Rad Forcing',           'units': '[Wm$^{-2}$]'}
row_pcldt =             {'var':'pcldt',          'title':'Total Cloud Cover',              'units': '[%]'}
row_pscld =             {'var':'pscld',          'title':'Shallow Convective Cloud Cover', 'units': '[%]'}
row_pdcld =             {'var':'pdcld',          'title':'Deep Convective Cloud Cover',    'units': '[%]'}
row_wtrcld =            {'var':'wtrcld',         'title':'Water Cloud Cover',              'units': '[%]'}
row_icecld =            {'var':'icecld',         'title':'Ice Cloud Cover',                'units': '[%]'}
row_list = [row_net_rad_planet, row_tsurf, row_snowicefr, row_ZSI]

col_0  = {'filedir':filedir0,  'SA':0}
col_1  = {'filedir':filedir1,  'SA':1}
col_4  = {'filedir':filedir4,  'SA':4}
col_6  = {'filedir':filedir6,  'SA':6}
col_11 = {'filedir':filedir11, 'SA':11}
col_22 = {'filedir':filedir22, 'SA':22}
col_26 = {'filedir':filedir26, 'SA':26}
col_34 = {'filedir':filedir34, 'SA':34}
col_39 = {'filedir':filedir39, 'SA':39}

col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]


def avgDataFilesGlobal(filedir, var, num_files, filetype, unit_conv, depth):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')

        if filetype == 'aij':
            area_arr = nc_i['axyp'][:]
        elif filetype == 'oijl':
            area_arr = nc_i['oxyp3'][:][depth]

        if depth == None:
            arr = nc_i[var][:]
        else:
            arr = nc_i[var][:][depth]
        arr_tot = arr_tot + arr
    arr_avg = (arr_tot * unit_conv) / num_files
    avg_val = np.sum(arr_avg * area_arr) / np.sum(area_arr)
    return avg_val


def makeSubplot(ax, row, filetype, num_files=10, unit_conv=1, depth=None):
    var = row['var']
    title = row['title']
    units = row['units']
    SA_arr = []
    val_arr = []
    for col in col_list:
        filedir = col['filedir']
        SA_arr.append(col['SA'])
        val_arr.append(avgDataFilesGlobal(filedir, var, num_files, filetype, unit_conv, depth))
    SA_arr = np.array(SA_arr)
    val_arr = np.array(val_arr)
    ax.plot(SA_arr, val_arr, color='k', marker='x', markersize=10)
    ax.set_title('Global Mean ' + title)
    ax.set_xlabel('Surface Area Coverage [%]')
    ax.set_ylabel(units)


row = row_tsurf
fig, ax = plt.subplots()

makeSubplot(ax, row, filetype='aij')

fig.tight_layout(w_pad = 2.25)
file_name = 'plots/global_tsurf'
# plt.savefig(file_name+'.svg')
plt.savefig(file_name+'.pdf')
plt.show()




