from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
from matplotlib import pyplot as plt, cm as cm
from glob import glob
from matplotlib.colors import Normalize
from cbar import MidPointNorm
from files_n_vars import *
from mpl_toolkits.axes_grid1 import ImageGrid


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


def getDimAvg(data, avg_coord):
    """
    get an average array over one dimension
    :param data: inputted 3D data (depth, lat, lon)
    :param avg_coord: coordinate you want to average across, leaving the others to show
    Example: averaging across 'lon' leaves you with an array that is depth by latitude.
    :return:
    """
    if avg_coord == 'lat':
        avg_axis = 1
    elif avg_coord == 'lon':
        avg_axis = 2
    return np.mean(data, axis=avg_axis)


def makeSubplot(data, grid, row, col, seq_or_div):
    ax = grid[0]

    min_val = np.min(data)
    max_val = np.max(data)

    def make_cmap(seq_or_div, levels = 20):
        if seq_or_div == 'seq':
            cmap = cm.Blues_r
            norm = Normalize(vmin = min_val, vmax = max_val)
        elif seq_or_div == 'div':
            cmap = cm.seismic
            norm = MidPointNorm(midpoint=0, vmin=min_val, vmax=max_val)
        return cmap, norm, levels
    cmap, norm, levels = make_cmap(seq_or_div)

    im = ax.imshow(data, cmap=cmap, norm=norm)
    grid.cbar_axes[0].colorbar(im)
    ax.set_title(col['title'] + ', ' + row['title'])


def getPlotName(row, col, filetype, avg_coord):
    var_name = row['var']
    if 'o' in filetype:
        var_name = 'o_' + var_name
    p_name = str(col['SA'])+'p'
    file_name = 'plots/{0}/{1}_{2}Avg2D'.format(p_name, var_name, avg_coord)
    return file_name


def dimAvg2DPlot(row, col, filetype, avg_coord, seq_or_div = 'div'):
    fig = plt.figure(figsize = (14,6))
    grid = ImageGrid(fig, 111,
                      nrows_ncols=(1, 1),
                      axes_pad=0.07,
                      share_all=True,
                      cbar_location="right",
                      cbar_mode="single",
                      cbar_size="7%",
                      cbar_pad="7%",
                      aspect=True)
    var = row['var']
    filedir = col['filedir']
    data = getDimAvg(avgDataFiles(filedir, var, filetype), avg_coord)
    print("MIN VAL: {0}, MAX VAL: {1}".format(np.min(data), np.max(data)))

    makeSubplot(data=data, grid=grid, row=row, col=col, seq_or_div=seq_or_div)

    # fig.tight_layout(w_pad = 2.25)
    file_name = getPlotName(row, col, filetype, avg_coord)
    print('Filename:', file_name)
    # plt.savefig(file_name+'.svg')
    # plt.savefig(file_name+'.pdf')
    plt.show()
    print('Plot Saved.')

row = row_o_salt
col = col_0
filetype = 'oijlpc'
avg_coord = 'lon'
seq_or_div = 'div'

dimAvg2DPlot(row, col, filetype, avg_coord, seq_or_div)
