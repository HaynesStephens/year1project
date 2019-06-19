from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from files_n_vars import *
from lat_lon_grid import *

def avgDataFilesLatLon(filedir, var, num_files, filetype, unit_conv):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')

        if depth == None:
            arr = nc_i[var][:]
        else:
            arr = nc_i[var][:][depth]

        arr_tot = arr_tot + arr

    arr_avg = (arr_tot * unit_conv) / num_files
    if 'aqua' in filedir:
        arr_avg = np.roll(arr_avg, (arr_avg.shape[1]) // 2, axis=1)
    return arr_avg


def getSlice(data, slice_dim, slice_coord):
    """
    :param data: the inputted 3D data array
    :param slice_dim: the dimension that you want to cut along (depth, lat, lon)
    :param slice_coord: the coordinate of dimensions that you want to cut along [degrees or m]
    :return: the 2D array sliced out along slice_dim at the coordinate slice_coord
    """
    if slice_dim == 'lat':
        slice_index = np.where(lato == slice_coord)[0][0]
        section = data[:,slice_index,:]
    elif slice_dim == 'lon':
        slice_index = np.where(lono == slice_coord)[0][0]
        section = data[:,:,slice_index]
    return section


def sliceSubplot(data, slice_dim, slice_coord, axes, row_num, col_num, ylabel, title):
    ax = axes[row_num, col_num]
    section = getSlice(data, slice_dim, slice_coord)

    im = ax.imshow(section)
    plt.colorbar(im, ax=ax)

    if row_num==0:
        ax.set_title(title, fontsize=10)

    if col_num==0:
        ax.set_ylabel(ylabel, fontsize=10, labelpad = 60, rotation=0, verticalalignment ='center')


def slicePlot(row_list, col_list, slice_dim, slice_coord):
    fig, axes = plt.subplots(len(row_list), len(col_list),
                             figsize = (10,5))

    for row_num in range(len(row_list)):
        row = row_list[row_num]
        var = row['var']
        for col_num in range(len(col_list)):
            col = col_list[col_num]
            print(row_num, col_num)
            filedir=col['filedir']
            data = avgDataFiles(filedir, var)
            sliceSubplot(data=data, slice_dim = slice_dim, slice_coord = slice_coord, axes=axes,
                        row_num=row_num, col_num=col_num, ylabel=row['ylabel'], title=col['title'])

    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/slice_dens'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()


row_list = [row_dens]
col_list = [col_0, col_1, col_22, col_39]
slice_dim = 'lon'
slice_coord = 2.5

slicePlot(row_list, col_list, slice_dim, slice_coord)

