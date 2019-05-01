from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from files_n_vars import *


def avgDataFilesGlobal(filedir, var, num_files, filetype, unit_conv, depth, side):
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
    if side == 'Global':
        avg_val = np.sum(arr_avg * area_arr) / np.sum(area_arr)
        return avg_val
    else:
        avg_val = getSideMean(data, area_arr, side)
        return avg_val


def getSideMean(data, area_arr, side):
    cropped_data = data.copy()
    cropped_area = area_arr.copy()
    if side == 'Day Side':
        lon_indices = np.where(np.abs(lon_grid) < 88)[0]
    elif side == 'Night Side':
        lon_indices = np.where(np.abs(lon_grid) > 88)[0]
    elif side == 'Sub-stellar':
        lon_indices = np.where(np.abs(lon_grid) < 13)[0]
        lat_indices = np.where(np.abs(lat_grid) < 11)[0]
        cropped_data = cropped_data[lat_indices, :]
        cropped_area = cropped_area[lat_indices, :]

    cropped_data = cropped_data[:, lon_indices]
    cropped_area = cropped_area[:, lon_indices]
    avg_val = np.sum(cropped_data * cropped_area) / np.sum(cropped_area)
    return avg_val


def makeSubplot(col_list, ax, row, filetype, num_files=10, unit_conv=1, depth=None, side='Global'):
    var = row['var']
    title = row['title']
    units = row['units']
    SA_arr = []
    val_arr = []
    for col in col_list:
        filedir = col['filedir']
        SA_arr.append(col['SA'])
        val_arr.append(avgDataFilesGlobal(filedir, var, num_files, filetype, unit_conv, depth, side))
    SA_arr = np.array(SA_arr)
    val_arr = np.array(val_arr)
    ax.plot(SA_arr, val_arr, color='k', marker='o', markersize=10, label = 'ROCKE-3D')
    ax.set_title(side + ' Mean ' + title)
    ax.set_xlabel('Continent size (% of total surface)')
    ax.set_ylabel(units)


def globalValPlot():
    col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]
    row = row_tsurf
    fig, ax = plt.subplots()

    makeSubplot(col_list, ax, row, filetype='aijpc', side='Day')

    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/day_side_tsurf'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()

globalValPlot()


