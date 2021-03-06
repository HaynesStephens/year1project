from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from glob import glob
from files_n_vars import *
from lat_lon_grid import *

def avgDataFiles(filedir, var, filetype, unit_conv=1, num_files=10):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = 0
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:]
        arr_tot = arr_tot + arr
    arr_avg = (arr_tot * unit_conv) / num_files

    if 'aqua' in filedir: #if it's aquaplanet simulation you need to roll so that substell point is in middle
        arr_avg = np.roll(arr_avg, (arr_avg.shape[2]) // 2, axis=2)

    if 'o' in filetype: #if it's ocean file, only take the top 5 levels
        arr_avg = arr_avg[:5, :, :]

    return arr_avg


def getSlice(data, slice_dim, slice_coord, lat_grid, lon_grid):
    """
    :param data: the inputted 3D data array
    :param slice_dim: the dimension that you want to cut along (depth, lat, lon)
    :param slice_coord: the coordinate of dimensions that you want to cut along [degrees or m]
    :return: the 2D array sliced out along slice_dim at the coordinate slice_coord
    """
    if slice_dim == 'lat': # slice along a latitude
        slice_index = np.where(lat_grid == slice_coord)[0][0]
        section = data[:,slice_index,:]
    elif slice_dim == 'lon': # slice along a longitude
        slice_index = np.where(lon_grid == slice_coord)[0][0]
        section = data[:,:,slice_index]
    return section


def sliceSubplot(data, slice_dim, slice_coord, axes, row_num, col_num,
                 ylabel, title, lat_grid, lon_grid, z_grid):
    """
    :param data: inputted data
    :param slice_dim: dimension along which you want to cut
    :param slice_coord: coordinate of slice_dim you want to cut
    :param axes: axes of figure
    :param row_num:
    :param col_num:
    :param ylabel:
    :param title:
    :return: a subplot for the given variable and continent size
    """
    ax = axes#[col_num]
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    section = getSlice(data, slice_dim, slice_coord, lat_grid, lon_grid)

    im = ax.imshow(section, aspect = 'auto')
    plt.colorbar(im, cax=cax)

    if slice_dim == 'lat':
        ax.set_xlabel('Lon')
        # ax.set_xticklabels(['']*lon_grid.size)
    elif slice_dim == 'lon':
        ax.set_xlabel('Lat')
        # ax.set_xticklabels(['']*lat_grid.size)

    if row_num == 0:
        ax.set_title(title, fontsize=10)


    if col_num == 0:
        ax.set_ylabel(ylabel, fontsize=10, labelpad = 60, rotation=0, verticalalignment ='center')
        ax.set_yticklabels(['']+z_grid.tolist())
    # else:
    #     ax.set_yticklabels(['']*len(z_grid))


def slicePlot(filetype, row_list, col_list, slice_dim, slice_coord):
    fig, axes = plt.subplots(len(row_list), len(col_list),
                             figsize = (12,3))

    for row_num in range(len(row_list)):
        row = row_list[row_num]
        lat_grid = row['lat']
        lon_grid = row['lon']
        z_grid = row['z']
        if z_grid.size == 13:
            z_grid = z_grid[:5]
        var = row['var']
        for col_num in range(len(col_list)):
            col = col_list[col_num]
            print(row_num, col_num)
            filedir=col['filedir']
            data = avgDataFiles(filedir, var, filetype)
            sliceSubplot(data=data, slice_dim = slice_dim, slice_coord = slice_coord, axes=axes,
                         row_num=row_num, col_num=col_num, ylabel=row['ylabel'], title=col['title'],
                         lat_grid=lat_grid, lon_grid=lon_grid, z_grid=z_grid)

    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/slice_o_pot_dens_aqua'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()


row_list = [row_o_pot_dens]
col_list = [col_0]#, col_1, col_22, col_39]
slice_dim = 'lon'
slice_coord = 2.5
filetype = 'oijl'

slicePlot(filetype, row_list, col_list, slice_dim, slice_coord)

