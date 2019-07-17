from files_n_vars import *
from lat_lon_grid import *
import numpy as np
from netCDF4 import Dataset as ds

def getPlanAlbFromSol(col, filetype = 'aijpc', num_files = 10):
    filedir = col['filedir']
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = 0
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        net_i = nc_i['srnf_toa'][:]
        inc_i = nc_i['incsw_toa'][:]
        out_i = inc_i - net_i
        albedo_i = (out_i / inc_i) * 100
        arr_tot = arr_tot + albedo_i

        area_arr = nc_i['axyp'][:]
        area_arr[albedo_i.mask] = 0
        print(np.where(area_arr == 0)[0].size)
    arr_avg = arr_tot / num_files
    if 'aqua' in filedir:
        arr_avg = np.roll(arr_avg, (arr_avg.shape[1]) // 2, axis=1)
        area_arr = np.roll(area_arr, (area_arr.shape[1]) // 2, axis=1)
        # Rolling the area so that masked values (i.e. for albedo) are rolled according to their coordinate
        # Rollling is necessary for determining side and substell averages

    plot_row = {'var':'plan_alb_calc',
                'ylabel':'Calculated \n Planetary \n Albedo \n [%]',
                'title':'Calculated Planetary Albedo',
                'units':'[%]',
                'lat':lat,
                'lon':lon}
    title = col['title']
    return arr_avg, area_arr, plot_row, title


