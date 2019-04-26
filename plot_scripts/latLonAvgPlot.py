from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from files_n_vars import *
from lat_lon_grid import *

def avgDataFilesLatLon(filedir, var, num_files, filetype, unit_conv, depth, avg_coord):
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
    if avg_coord == 'lat':
        avg_axis = 1
    elif avg_coord == 'lon':
        avg_axis = 0
    avg_arr = np.sum(arr_avg * area_arr, axis=avg_axis) / np.sum(area_arr, axis=avg_axis)
    return avg_arr

def makeSubplot(ax, row, filetype, avg_coord, num_files=10, unit_conv=1, depth=None):
    if avg_coord == 'lat':
        x = lat_grid
        x_label = 'Latitude'
    elif avg_coord == 'lon':
        x = lon_grid
        x_label = 'Longitude'
    var = row['var']
    title = row['title']
    units = row['units']
    for col in col_list:
        filedir = col['filedir']
        val_arr = avgDataFilesLatLon(filedir, var, num_files, filetype, unit_conv, depth, avg_coord)
        SA = str(col['SA']) + '%'
        if SA == '0%':
            SA = 'Aqua'
        ax.plot(x, val_arr, label=SA)
    ax.legend()
    ax.set_title('Average ' + title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(units)


col_list = [col_0, col_11, col_39]
row = row_tsurf
fig, ax = plt.subplots()

makeSubplot(ax, row, filetype='aijpc', avg_coord='lon')

fig.tight_layout(w_pad = 2.25)
file_name = 'plots/lon_tsurf'
# plt.savefig(file_name+'.svg')
plt.savefig(file_name+'.pdf')
plt.show()
