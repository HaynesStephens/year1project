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
        min_val = -110
        max_val = 110
        levels = np.linspace(min_val, max_val, 23)
        if seq_or_div == 'seq':
            cmap = cm.Blues
            norm = Normalize(vmin = min_val, vmax = max_val)
        elif seq_or_div == 'div':
            cmap = cm.seismic
            norm = MidPointNorm(midpoint=0, vmin=min_val, vmax=max_val)
        return cmap, norm, levels
    cmap, norm, levels = make_cmap(seq_or_div)

    def quiverUV(x_u, y_u, u, v, quiv_norm=False):
        if quiv_norm:
            uv_mag = np.sqrt((u * u) + (v * v))
            q = ax.quiver(x_u, y_u, u/uv_mag, v/uv_mag)
        else:
            q = ax.quiver(x_u, y_u, u, v, scale_units='width', scale=2000,
                 pivot='middle', width=0.001, headwidth=5, headlength=5)
            U = 50
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

    ax.set_xlim(-180,180)
    ax.set_ylim(-90,90)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(title)


def getPlotName(row_contour, col, filetype_uv, depth):
    if depth == None:
        depth_name = ''
    elif depth == 'vertAvg':
        depth_name = '_vertAvg'
    else:
        depth_name = '_' + str(depth)
    if row_contour != None:
        var_name = row_contour['var']
    else:
        var_name = 'uv'
    if 'o' in filetype_uv:
        var_name = 'o_' + var_name

    p_name = str(col['SA'])+'p'

    file_name = 'plots/{0}/quiver_{1}{2}'.format(p_name, var_name, depth_name)
    return file_name


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


def getHeightFile(filedir, filetype, num_files=10):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    z_tot = 0
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        z_i = nc_i['z'][:]
        z_tot = z_tot + z_i
    z_avg = z_tot / num_files

    if 'aqua' in filedir: #if it's aquaplanet simulation you need to roll so that substell point is in middle
        z_avg = np.roll(z_avg, (z_avg.shape[2]) // 2, axis=2)

    z_final = z_avg.reshape((z_avg.shape[0], -1)).mean(axis=1)
    return z_final


def getTitle(row_u, row_contour, col, depth, filetype_uv):
    if row_contour != None:
        title_row = row_contour['title']
    else:
        title_row = 'Velocity'

    if depth == None:
        title_depth = ''
    elif depth == 'vertAvg':
        title_depth = ', Vert. Avg.'
    else:
        if 'o' in filetype_uv:
            z_arr = row_u['z']
        elif 'a' in filetype_uv:
            z_arr = getHeightFile(col['filedir'], filetype_uv)
        title_depth = ', {0:.0f} m'.format(z_arr[depth])
    title = '{0}{1}, {2}'.format(col['title'], title_depth, title_row)
    return title



def quiverPlot(row_u, row_v, row_contour, col, filetype_uv, filetype_contour,
               depth, depth_contour, seq_or_div):
    fig = plt.figure(figsize = (14,6))
    grid1 = ImageGrid(fig, 111,
                      nrows_ncols=(1,1),
                      axes_pad=0.07,
                      share_all=True,
                      cbar_location="bottom",
                      cbar_mode="single",
                      cbar_size="4%",
                      cbar_pad="11%",
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
        contour_data = depthOrVertAvg(contour_data, depth_contour)
    else:
        contour_data = np.sqrt((u * u) + (v * v)) # Set contours as the horizontal velocity magnitudes
        print("{0} MIN: {1}, {0} MAX: {2}".format('Velocity', np.min(contour_data), np.max(contour_data)))


    title = getTitle(row_u, row_contour, col, depth, filetype_uv)
    makeSubplot(grid=grid1, row_u=row_u, u=u, v=v,
                row_contour=row_contour, contour_data=contour_data,
                col=col, title=title, seq_or_div=seq_or_div)

    # fig.tight_layout(w_pad = 2.25)
    file_name = getPlotName(row_contour, col, filetype_uv, depth)
    print('PLOT NAME:', file_name)

    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    # plt.show()
    print('Plot saved.')

col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]

row_u = row_ub
row_v = row_vb
filetype_uv = 'aijkpc'

row_contour = row_temp
filetype_contour = 'aijlpc'

# col = col_39

seq_or_div = 'div'


# ############# SINGLE DEPTH PLOT #################
# depth = 0
# depth_contour = 0
# quiverPlot(row_u, row_v, row_contour, col, filetype_uv, filetype_contour,
#            depth, depth_contour, seq_or_div)

# ############ ALL DEPTHS PLOT ###################
# for depth_i in range(row_u['z'].size):
#     quiverPlot(row_u, row_v, row_contour, col, filetype_uv, filetype_contour,
#                depth_i, depth_i, seq_or_div)

# ############# ALL VERT AVGS PLOT #################
# depth = 'vertAvg'
# depth_contour = 'vertAvg'
# for col_i in col_list:
#     quiverPlot(row_u, row_v, row_contour, col_i, filetype_uv, filetype_contour,
#                depth, depth_contour, seq_or_div)

############ WHOLE SHABANG ################
for col_i in col_list:
    for depth_i in range(row_u['z'].size):
        quiverPlot(row_u, row_v, row_contour, col_i, filetype_uv, filetype_contour,
                   depth_i, depth_i, seq_or_div)
    quiverPlot(row_u, row_v, row_contour, col_i, filetype_uv, filetype_contour,
               'vertAvg', 'vertAvg', seq_or_div)
