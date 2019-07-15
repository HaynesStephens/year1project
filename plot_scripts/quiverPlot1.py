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


def makeSubplot(grid, row_u, u, v, row_contour, contour_data, col, title, seq_or_div):
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

    def quiverUV(x_u, y_u, u, v, quiv_norm=False):
        if quiv_norm:
            uv_mag = np.sqrt((u * u) + (v * v))
            q = ax.quiver(x_u, y_u, u/uv_mag, v/uv_mag)
        else:
            q = ax.quiver(x_u, y_u, u, v, scale_units='width', scale=1000,
                 pivot='middle', width=0.001, headwidth=5, headlength=5)
            U = 10
            key_label = '{0} m/s'.format(U)
            ax.quiverkey(q, X=0.93, Y=1.02, U=U, label=key_label, labelpos='E')

    def contourPlot(x, y, data, units, levels, cmap, norm):
        im = ax.contourf(x, y, data, levels, cmap=cmap, norm=norm)
        cbar = grid.cbar_axes[0].colorbar(im)
        cbar.set_label_text(units)

    if row_contour != None:
        x_contour = row_contour['lon']
        y_contour = row_contour['lat']
        units_contour = row_contour['units']
    else:
        x_contour = x_u
        y_contour = y_u
        units_contour = row_u['units']

    contourPlot(x_contour, y_contour, contour_data, units_contour, levels, cmap, norm)
    quiverUV(x_u, y_u, u, v)

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

    ax.set_title(title)


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


def getTitle(row_u, row_contour, col, depth, filetype_uv, filetype_contour):
    title_row = 'Velocity'
    if depth == None:
        title_depth = ''
    elif depth == 'vertAvg':
        title_depth = ', Vert. Avg.'
    else:
        if row_contour != None:
            row_ext = row_contour
            filetype_ext = filetype_contour
            title_row = row_contour['title']
        else:
            row_ext = row_u
            filetype_ext = filetype_uv
        if 'o' in filetype_ext:
            ext = ' m'
        elif 'a' in filetype_ext:
            ext = ' mb'
        title_depth = ', ' + str(row_ext['z'][depth]) + ext
    title = col['title'] + title_depth + ', ' + title_row
    return title



def quiverPlot(row_u, row_v, row_contour, col, filetype_uv, filetype_contour, depth, seq_or_div):
    fig = plt.figure(figsize = (14,6))
    grid1 = ImageGrid(fig, 111,
                      nrows_ncols=(1,1),
                      axes_pad=0.07,
                      share_all=True,
                      cbar_location="bottom",
                      cbar_mode="single",
                      cbar_size="4%",
                      cbar_pad="7%",
                      aspect=True)
    filedir = col['filedir']

    var_u = row_u['var']
    u = avgDataFiles(filedir, filetype_uv, var_u)
    print("U MIN: {0}, U MAX: {1}".format(np.min(u), np.max(u)))
    u = depthOrVertAvg(u, depth)

    var_v = row_v['var']
    v = avgDataFiles(filedir, filetype_uv, var_v)
    print("V MIN: {0}, V MAX: {1}".format(np.min(v), np.max(v)))
    v = depthOrVertAvg(v, depth)

    if row_contour != None:
        var_contour = row_contour['var']
        contour_data = avgDataFiles(filedir, filetype_contour, var_contour)
        print("{0} MIN: {1}, {0} MAX: {2}".format(var_contour, np.min(contour_data), np.max(contour_data)))
    else:
        contour_data = np.sqrt((u * u) + (v * v)) # Set contours as the horizontal velocity magnitudes
        print("{0} MIN: {1}, {0} MAX: {2}".format('Velocity', np.min(contour_data), np.max(contour_data)))


    title = getTitle(row_u, row_contour, col, depth, filetype_uv, filetype_contour)
    makeSubplot(grid=grid1, row_u=row_u, u=u, v=v,
                row_contour=row_contour, contour_data=contour_data,
                col=col, title=title, seq_or_div=seq_or_div)

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
filetype_uv = 'aijkpc'
row_contour = None
filetype_contour = None
col = col_4
depth = 10

seq_or_div = 'seq'

quiverPlot(row_u, row_v, row_contour, col, filetype_uv, filetype_contour, depth, seq_or_div)
