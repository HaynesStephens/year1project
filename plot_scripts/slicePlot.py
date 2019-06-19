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

