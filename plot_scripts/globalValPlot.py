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

row_frac_land =         {'var':'frac_land',      'ylabel':'Land \n Fraction \n [%]'}
row_net_rad_planet =    {'var':'net_rad_planet', 'ylabel':'Net \n Planet \n Radiation \n [Wm$^{-2}$]'}
row_tsurf =             {'var':'tsurf',          'ylabel':'Surface \n Temperature \n [C]'}
row_snowicefr =         {'var':'snowicefr',      'ylabel':'Snow/Ice \n Fraction \n [%]'}
row_ZSI =               {'var':'ZSI',            'ylabel':'Sea Ice \n Thickness \n [m]'}
row_lwp =               {'var':'lwp',            'ylabel':'Liquid \n Water \n Path \n [0.1kgm$^{-2}$]'}
row_swcrf_toa =         {'var':'swcrf_toa',      'ylabel':'SW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]'}
row_lwcrf_toa =         {'var':'lwcrf_toa',      'ylabel':'LW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]'}
row_pcldt =             {'var':'pcldt',          'ylabel':'Total Cloud \n Cover \n [%]'}
row_pscld =             {'var':'pscld',          'ylabel':'Shallow \n Convective \n Cloud \n Cover \n [%]'}
row_pdcld =             {'var':'pdcld',          'ylabel':'Deep \n Convective \n Cloud \n Cover \n [%]'}
row_wtrcld =            {'var':'wtrcld',         'ylabel':'Water \n Cloud Cover \n [%]'}
row_icecld =            {'var':'icecld',         'ylabel':'Ice \n Cloud Cover \n [%]'}
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


def makeSubplot(ax, row):
    var = row['var']
    ylabel = row['ylabel']
    SA_arr = []
    val_arr = []
    for col in col_list:
        filedir = col['filedir']
        SA_arr.append(col['SA'])
        val_arr.append(avgDataFilesGlobal(filedir, var, num_files, filetype, unit_conv, depth))
    SA_arr = np.array(SA_arr)
    val_arr = np.array(val_arr)
    ax.plot(SA_arr, val_arr)
    ax.set_title(ylabel)


var = row_tsurf['var']
fig, ax = plt.subplots(figsize = (10,7))

makeSubplot(ax, row)

fig.tight_layout(w_pad = 2.25)
file_name = 'plots/global_Tsurf'
# plt.savefig(file_name+'.svg')
# plt.savefig(file_name+'.pdf')
plt.show()




