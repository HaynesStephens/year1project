from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from files_n_vars import *
from lat_lon_grid import *


def avgDataFilesLatLon(filedir, var, num_files, filetype, unit_conv, depth, side):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')

        if filetype == 'aijpc':
            area_arr = nc_i['axyp'][:]
        elif filetype == 'oijlpc':
            area_arr = nc_i['oxyp3'][:][depth]

        if depth == None:
            arr = nc_i[var][:]
        else:
            arr = nc_i[var][:][depth]

        arr_tot = arr_tot + arr

    arr_avg = (arr_tot * unit_conv) / num_files
    if 'aqua' in filedir:
        arr_avg = np.roll(arr_avg, (arr_avg.shape[1]) // 2, axis=1)
    return getSideMean(arr_avg, area_arr, side)


def getSideMean(data, area_arr, side):
    if side == 'day':
        cropped_data = data[:, -87.5 <= lon_grid <= 87.5]
        cropped_area = area_arr[:, -87.5 <= lon_grid <= 87.5]
    elif side == 'night':
        cropped_data = data[:, np.abs(lon_grid) > 87.5]
        cropped_area = area_arr[:, np.abs(lon_grid) > 87.5]
    elif side == 'substellar':
        cropped_data = data[-10 <= lat_grid <= 10, -12.5 <= lon_grid <= 12.5]
        cropped_area = area_arr[-10 <= lat_grid <= 10, -12.5 <= lon_grid <= 12.5]
    avg_val = np.sum(cropped_data * cropped_area) / np.sum(cropped_area)
    return cropped_data

avgDataFilesLatLon(filedir1, 'frac_land', 10, 'aijpc', 1, None, 'day')

