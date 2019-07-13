from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
from matplotlib import pyplot as plt, cm as cm
from glob import glob
from matplotlib.patches import Polygon
from matplotlib.colors import Normalize
from cbar import MidPointNorm
from files_n_vars import *
from mpl_toolkits.axes_grid1 import ImageGrid

def avgDataFiles(filedir, filetype, var, unit_conv = 1, num_files=10):
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


def makeSubplot(grid, row_u, row_contour, u, v, col, title, seq_or_div):
    ax = grid[0]
    ax.set_facecolor('.25')

    x_u = row_u['lon']
    y_u = row_u['lat']

    # min_val = np.min(np.abs(data))
    # max_val = np.max(np.abs(data))

    def make_cmap(seq_or_div):
        min_val = 0
        max_val = 50
        levels = np.linspace(min_val, max_val, 50)
        if seq_or_div == 'seq':
            cmap = cm.Reds
            norm = Normalize(vmin = min_val, vmax = max_val)
        elif seq_or_div == 'div':
            cmap = cm.seismic
            norm = MidPointNorm(midpoint=0, vmin=-max_val, vmax=max_val)
        return cmap, norm, levels
    cmap, norm, levels = make_cmap(seq_or_div)


    def quiverUVNone(x_u, y_u, u, v):
        q = ax.quiver(x_u, y_u, u/u, v/v)

    def quiverUVX(x_u, y_u, u, v):
        q = ax.quiver(x_u, y_u, u, v)
        U = 1
        key_label = '{0} m/s'.format(U)
        ax.quiverkey(q, X=0.93, Y=1.02, U=U, label=key_label, labelpos='E')

    def contourOverlay(x, y, data, units, levels, cmap, norm):
        im = ax.contourf(x, y, data, levels, cmap=cmap, norm=norm)
        cbar = grid.cbar_axes[0].colorbar(im)
        cbar.set_label_text(units)

    if row_contour != None:
        var_contour = row_contour['var']
        contour_data = avgDataFiles(filedir, filetype, var_contour)
        print("{0} MIN: {1}, {0} MAX: {2}".format(var_contour, np.min(contour_data), np.max(contour_data)))
        contour_data = depthOrVertAvg(contour_data, depth)
        x_contour = row_contour['lon']
        y_contour = row_contour['lat']
        contourOverlay(x_contour, y_contour, contour_data, row_contour['units'], levels, cmap, norm)
        if row_contour['var'] == 'tsurf':
            ax.contour(row_contour['lon'], row_contour['lat'], contour_data,
                       ax=ax, levels=[0], colors=('k',), linestyles=('-.',), linewidths=(1,))
        quiverUVX(x_u, y_u, u, v)
    else:
        contour_data = np.sqrt((u * u) + (v * v))
        print("{0} MIN: {1}, {0} MAX: {2}".format('Velocity', np.min(contour_data), np.max(contour_data)))
        contourOverlay(x_u, y_u, contour_data, row_u['units'], levels, cmap, norm)
        quiverUVNone(x_u, y_u, u, v)


    parallels = col['parallels']
    meridians = col['meridians']
    if 'Aqua' not in title:
        x1, y1 = meridians[0], parallels[0]
        x2, y2 = meridians[0], parallels[1]
        x3, y3 = meridians[1], parallels[1]
        x4, y4 = meridians[1], parallels[0]
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none',
                                edgecolor='black', linewidth=1)
        ax.add_patch(cont_boundary)


# def getPlotName(row, col, filetype, depth):
#     """
#     If the plot is a single figure (one simulation),
#     then generate the filename automatically.
#     :param row:
#     :param col:
#     :param filetype:
#     :param depth:
#     :return:
#     """
#     if depth == None:
#         depth_name = ''
#     elif depth == 'vertAvg':
#         depth_name = '_vertAvg'
#     else:
#         depth_name = '_' + str(depth)
#
#     var_name = row['var']
#     if 'o' in filetype:
#         var_name = 'o_' + var_name
#
#     p_name = str(col['SA'])+'p'
#
#     file_name = 'plots/{0}/{1}{2}'.format(p_name, var_name, depth_name)
#     return file_name


def depthOrVertAvg(data, depth):
    if depth == None:
        data = data

    elif depth == 'vertAvg':
        data = np.mean(data, axis=0)
        print("AVG MIN: {0}, AVG MAX: {1}".format(np.min(data), np.max(data)))

    else:
        data = data[depth,:,:]
        print("DEPTH MIN: {0}, DEPTH MAX: {1}".format(np.min(data), np.max(data)))

    return data



def quiverPlot(row_u, row_v, row_contour, col, filetype, depth, seq_or_div):
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
    filedir = col['filedir']

    var_u = row_u['var']
    u = avgDataFiles(filedir, filetype, var_u)
    print("U MIN: {0}, U MAX: {1}".format(np.min(u), np.max(u)))
    u = depthOrVertAvg(u, depth)

    var_v = row_v['var']
    v = avgDataFiles(filedir, filetype, var_v)
    print("V MIN: {0}, V MAX: {1}".format(np.min(v), np.max(v)))
    v = depthOrVertAvg(v, depth)

    makeSubplot(grid=grid1, row_u=row_u, row_contour=row_contour, u=u, v=v,
                col=col, title='None yet', seq_or_div=seq_or_div)

    # fig.tight_layout(w_pad = 2.25)
    """
    file_name = getPlotName(row, col, filetype, depth)
    print('PLOT NAME:', file_name)
    """


    # plt.savefig(file_name+'.svg')
    # plt.savefig(file_name+'.pdf')
    plt.show()
    print('Plot saved.')


row_u = row_ub
row_v = row_vb
row_contour = None
col = col_4
filetype = 'aijkpc'
depth = 10

seq_or_div = 'seq'

quiverPlot(row_u, row_v, row_contour, col, filetype, depth, seq_or_div)
