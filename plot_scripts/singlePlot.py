from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
from matplotlib import pyplot as plt, cm as cm
from glob import glob
from matplotlib.patches import Polygon
from matplotlib.colors import Normalize
from cbar import MidPointNorm
from files_n_vars import *
from mpl_toolkits.axes_grid1 import make_axes_locatable, ImageGrid
import calculatedQuantities as calcQuant

def avgDataFiles(filedir, filetype, var, unit_conv = 1, num_files=10):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = 0
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:]
        arr_tot = arr_tot + arr
    arr_avg = (arr_tot * unit_conv) / num_files

    if 'aqua' in filedir: #if it's aquaplanet simulation you need to roll so that substell point is in middle
        roll_size = arr_avg.shape[-1]
        roll_axis = len(arr_avg.shape) - 1
        arr_avg = np.roll(arr_avg, (roll_size) // 2, axis=roll_axis)
    if 'o' in filetype: #if it's ocean file, only take the top 5 levels
        arr_avg = arr_avg[:5, :, :]
    return arr_avg


def makeSubplot(grid, data, row, col, title, seq_or_div):
    ax = grid[0]
    ax.set_facecolor('.25')
    m = Basemap(ax = ax)

    ny=data.shape[0]
    nx=data.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)

    # min_val = np.min(np.abs(data))
    # max_val = np.max(np.abs(data))

    def make_cmap(seq_or_div):
        min_val = 0.1
        max_val = 700
        levels = np.linspace(min_val, max_val, 15)
        if seq_or_div == 'seq':
            cmap = cm.Reds
            norm = Normalize(vmin = min_val, vmax = max_val)
        elif seq_or_div == 'div':
            cmap = cm.seismic
            norm = MidPointNorm(midpoint=0, vmin=min_val, vmax=max_val)
        return cmap, norm, levels
    cmap, norm, levels = make_cmap(seq_or_div)

    cs = m.contourf(x, y, data, levels, ax=ax, cmap=cmap, norm=norm)
    m.ax.tick_params(labelsize=2)

    ax.set_title(title, fontsize=10)

    ax.set_ylabel(row['ylabel'], fontsize=10, labelpad = 60, rotation=0, verticalalignment ='center')

    # draw parallels and meridians.
    m.drawparallels([-60, -30, 0, 30, 60], labels=[1,0,0,0], ax = ax,
                    rotation=30, fontsize=8, linewidth=0)
    m.drawmeridians([-135, -90, -45, 0, 45, 90, 135], labels=[0,0,0,1], ax = ax,
                    rotation=40, fontsize=8, linewidth=0)

    if row['var'] == 'tsurf':
        m.contour(x, y, data, ax=ax, levels = [0], colors=('k',),linestyles=('-.',),linewidths=(1,))

    parallels = col['parallels']
    meridians = col['meridians']
    if 'Aqua' not in title:
        x1, y1 = m(meridians[0], parallels[0])
        x2, y2 = m(meridians[0], parallels[1])
        x3, y3 = m(meridians[1], parallels[1])
        x4, y4 = m(meridians[1], parallels[0])
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none',
                                edgecolor='black', linewidth=1)
        ax.add_patch(cont_boundary)

    grid.cbar_axes[0].colorbar(cs)


def getPlotName(row, col, filetype, depth):
    """
    If the plot is a single figure (one simulation),
    then generate the filename automatically.
    :param row:
    :param col:
    :param filetype:
    :param depth:
    :return:
    """
    if depth == None:
        depth_name = ''
    elif depth == 'vertAvg':
        depth_name = '_vertAvg'
    else:
        depth_name = '_' + str(depth)

    var_name = row['var']
    if 'o' in filetype:
        var_name = 'o_' + var_name

    p_name = str(col['SA'])+'p'

    file_name = 'plots/{0}/{1}{2}'.format(p_name, var_name, depth_name)
    return file_name


def depthOrVertAvg(data, col, depth):
    if depth == None:
        data = data
        title = col['title']

    elif depth == 'vertAvg':
        data = np.mean(data, axis=0)
        print("AVG MIN: {0}, AVG MAX: {1}".format(np.min(data), np.max(data)))
        title = col['title'] + ', Vert. Avg.'

    else:
        data = data[depth,:,:]
        print("DEPTH MIN: {0}, DEPTH MAX: {1}".format(np.min(data), np.max(data)))
        if 'o' in filetype:
            ext = ' m'
        elif 'a' in filetype:
            ext = ' mb'
        title = col['title'] + ', ' + str(row['z'][depth]) + ext

    return data, title


def singlePlot(row, col, filetype, depth, seq_or_div):
    fig = plt.figure(figsize = (14,6))
    grid1 = ImageGrid(fig, 111,
                      nrows_ncols=(1,1),
                      axes_pad=0.07,
                      share_all=True,
                      cbar_location="right",
                      cbar_mode="single",
                      cbar_size="7%",
                      cbar_pad="7%",
                      aspect=True)

    var = row['var']
    filedir = col['filedir']
    data = avgDataFiles(filedir, filetype, var)
    print("TOT MIN: {0}, TOT MAX: {1}".format(np.min(data), np.max(data)))
    data, title = depthOrVertAvg(data, col, depth)

    # # Calculated Planetary Albedo Scenario
    # arr_avg, area_arr, plot_row, title = calcQuant.getPlanAlbFromSol(col)
    # data = arr_avg
    # print("TOT MIN: {0}, TOT MAX: {1}".format(np.min(data), np.max(data)))
    # row = plot_row
    # #

    makeSubplot(grid=grid1, data=data, row=row, col=col, title=title, seq_or_div=seq_or_div)

    # fig.tight_layout(w_pad = 2.25)
    file_name = getPlotName(row, col, filetype, depth)
    print('PLOT NAME:', file_name)

    # plt.savefig(file_name+'.svg')
    # plt.savefig(file_name+'.pdf')
    # plt.show()
    print('Plot saved.')


row = row_o_pot_dens
# col = col_39
filetype = 'oijlpc'
seq_or_div = 'seq'
col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]


# ############# SINGLE DEPTH PLOT #################
# depth = None
# singlePlot(row, col, filetype, depth, seq_or_div)

# ############# ALL DEPTHS PLOT ###################
# for depth_i in range(row['z'].size):
#     singlePlot(row, col, filetype, depth_i, seq_or_div)

# ############# ALL VERT AVGS PLOT #################
# depth = 'vertAvg'
# for col_i in col_list:
#     singlePlot(row, col_i, filetype, depth, seq_or_div)

############# WHOLE SHABANG ################
for col_i in col_list:
    for depth_i in range(row['z'].size):
        singlePlot(row, col_i, filetype, depth_i, seq_or_div)
    singlePlot(row, col_i, filetype, 'vertAvg', seq_or_div)

# ############# ALL CALLS OF SAME DEPTH ################
# depth = None
# for col_i in col_list:
#     singlePlot(row, col_i, filetype, depth, seq_or_div)


