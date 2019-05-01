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
    cropped_data = data.copy()
    cropped_area = area_arr.copy()
    if side == 'day':
        lon_indices = np.where(np.abs(lon_grid) < 88)[0]
    elif side == 'night':
        lon_indices = np.where(np.abs(lon_grid) > 88)[0]
    elif side == 'substellar':
        lon_indices = np.where(np.abs(lon_grid) < 13)[0]
        lat_indices = np.where(np.abs(lat_grid) < 11)[0]
        cropped_data = cropped_data[lat_indices, :]
        cropped_area = cropped_area[lat_indices, :]
    cropped_data = cropped_data[:, lon_indices]
    cropped_area = cropped_area[:, lon_indices]
    avg_val = np.sum(cropped_data * cropped_area) / np.sum(cropped_area)
    print(cropped_data)
    print(np.where(cropped_data > 0))
    print(cropped_data.shape)
    return avg_val

avgDataFilesLatLon(filedir1, 'frac_land', 10, 'aijpc', 1, None, 'night')

