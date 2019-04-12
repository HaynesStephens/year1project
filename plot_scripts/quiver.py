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

col_0 = {'filedir':filedir0, 'parallels':[],
        'meridians':[], 'title':'Dynamic (5L), Aquaplanet'}
col_1 = {'filedir':filedir1, 'parallels':[-12, 12],
        'meridians':[-15, 15], 'title':'Dynamic (5L), 1% SS Cont'}
col_4 = {'filedir':filedir4, 'parallels':[-16, 16],
        'meridians':[-30, 30], 'title':'Dynamic (5L), 4% SS Cont'}
col_6 = {'filedir':filedir6, 'parallels':[-20, 20],
        'meridians':[-35, 35], 'title':'Dynamic (5L), 6% SS Cont'}
col_11 = {'filedir':filedir11, 'parallels':[-24, 24],
        'meridians':[-50, 50], 'title':'Dynamic (5L), 11% SS Cont'}
col_22 = {'filedir':filedir22, 'parallels':[-36, 36],
        'meridians':[-70, 70], 'title':'Dynamic (5L), 22% SS Cont'}
col_26 = {'filedir':filedir26, 'parallels':[-40, 40],
        'meridians':[-75, 75], 'title':'Dynamic (5L), 26% SS Cont'}
col_34 = {'filedir':filedir34, 'parallels':[-44, 44],
        'meridians':[-90, 90], 'title':'Dynamic (5L), 34% SS Cont'}
col_39 = {'filedir':filedir39, 'parallels':[-48, 48],
        'meridians':[-95, 95], 'title':'Dynamic (5L), 39% SS Cont'}

col_list = [col_0, col_22, col_26]


def avgDataFiles3D(filedir, var, num_files = 10, filetype='oijl', depth=0):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:][depth]
        arr_tot = arr_tot + arr
    arr_avg = arr_tot / num_files
    return arr_avg

x = avgDataFiles3D(filedir1, 'u')


