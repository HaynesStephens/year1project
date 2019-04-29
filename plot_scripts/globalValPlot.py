from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from files_n_vars import *


def avgDataFilesGlobal(filedir, var, num_files, filetype, unit_conv, depth):
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
    avg_val = np.sum(arr_avg * area_arr) / np.sum(area_arr)
    return avg_val


def makeSubplot(col_list, ax, row, filetype, num_files=10, unit_conv=1, depth=None):
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
    ax.plot(SA_arr, val_arr, color='k', marker='o', markersize=10, label = 'ROCKE-3D')
    ax.set_title('Global Mean ' + title)
    ax.set_xlabel('Continent size (% of total surface)')
    ax.set_ylabel(units)


def globalValPlot():
    col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]
    row = row_qatm
    fig, ax = plt.subplots()

    makeSubplot(col_list, ax, row, filetype='aijpc')

    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/global_qatm'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()




