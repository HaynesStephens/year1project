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

def avgDataFiles(filedir, filetype, var, depth, unit_conv = 1, num_files=10):
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


def makeSubplot(data, var, cbar_data, grid, row_num, col_num, ylabel, parallels, meridians, title, plot_cbar=False):
    ax = grid[col_num]
    ax.set_facecolor('.25')
    m = Basemap(ax = ax)

    ny=data.shape[0]
    nx=data.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)

    min_val = np.min(cbar_data)
    max_val = np.max(cbar_data)

    def make_cmap(var):
        sequential_list = ['frac_land', 'pscld', 'pdcld', 'snowicefr', 'lwp',
                           'pcldt', 'pscld', 'pdcld', 'wtrcld', 'icecld', 'ZSI', 'prec', 'qatm',
                           'pot_dens', 'salt']
                            #list of sequential variables to use for cmap
        divergent_list = ['pot_temp', 'tsurf']
        if var in sequential_list:
            cmap = cm.Blues_r
            norm = Normalize(vmin = min_val, vmax = max_val)
        elif var in divergent_list:
            cmap = cm.seismic
            norm = MidPointNorm(midpoint=0, vmin=min_val, vmax=max_val)
            """KEEP EYE ON THIS. TRY OUT TO MAKE SURE IT WORKS W/ DIV CBARS"""
        levels = 20
        return cmap, norm, levels

    cmap, norm, levels = make_cmap(var)

    if plot_cbar:
        #Create colorbar to be used and then wipe axis so cbar_data isn't actually plotted
        cs_cbar = m.contourf(x, y, cbar_data, levels, ax=ax, cmap=cmap, norm=norm)
        ax.clear()

    cs = m.contourf(x, y, data, levels, ax=ax, cmap=cmap, norm=norm)
    m.ax.tick_params(labelsize=2)
    # m.colorbar(mappable=cs, ax=ax)

    if row_num==0:
        ax.set_title(title, fontsize=10)

    if col_num==0:
        ax.set_ylabel(ylabel, fontsize=10, labelpad = 60, rotation=0, verticalalignment ='center')

    # draw parallels and meridians.
        m.drawparallels([-60, -30, 0, 30, 60], labels=[1,0,0,0], ax = ax,
                    rotation=30, fontsize=8, linewidth=0)
    m.drawmeridians([-135, -90, -45, 0, 45, 90, 135], labels=[0,0,0,1], ax = ax,
                    rotation=40, fontsize=8, linewidth=0)

    def ContLines(m, ax, var, x, y, data):
        if var == 'tsurf':
            m.contour(x, y, data, ax=ax, levels = [0], colors=('k',),linestyles=('-.',),linewidths=(1,))

    ContLines(m, ax, var, x, y, data)

    if title != 'Aqua':
        x1, y1 = m(meridians[0], parallels[0])
        x2, y2 = m(meridians[0], parallels[1])
        x3, y3 = m(meridians[1], parallels[1])
        x4, y4 = m(meridians[1], parallels[0])
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none',
                                edgecolor='black', linewidth=1)
        ax.add_patch(cont_boundary)

    if plot_cbar:
        #Plot the colorbar on the final plot of the row
        # plt.colorbar(mappable=cs_cbar, cax=axes[row_num, col_num+1])
        grid.cbar_axes[0].colorbar(cs_cbar)

def getDataAndMaxVal(col_list, filetype, var, depth):
    """
    Used to get data for a given row and the max value in order to have uniform colorbars across a row.
    :param col_list:
    :param var:
    :return:
    """
    data_list = []
    for i in range(len(col_list)):
        col = col_list[i]
        filedir = col['filedir']
        data = avgDataFiles(filedir, filetype, var, depth)
        data_list.append(data)
        if i == 0:
            min_val = np.min(data)
            max_val = np.max(data)
        else:
            min_val = min(min_val, np.min(data))
            max_val = max(max_val, np.max(data))
    cbar_data = np.ones(shape = data.shape) * max_val # creates fake data w/ same shape to use for colorbar
    cbar_data[0, 0] = min_val # sets one point in fake data to min_val so fake data has the entire spread
    return data_list, cbar_data


def rowMatrixMap(row_list, col_list, filetype, depth = None):
    fig = plt.figure(figsize = (14,8))
    grid1 = ImageGrid(fig, 111,
                      nrows_ncols=(len(row_list), len(col_list)),
                      axes_pad=0.07,
                      share_all=True,
                      cbar_location="right",
                      cbar_mode="single",
                      cbar_size="7%",
                      cbar_pad="7%",
                      aspect=True)

    for row_num in range(len(row_list)):
        row = row_list[row_num]
        var = row['var']
        data_list, cbar_data = getDataAndMaxVal(col_list, filetype, var, depth)
        print("MIN VAL: {0}, MAX VAL: {1}".format(np.min(cbar_data), np.max(cbar_data)))
        for col_num in range(len(col_list)):
            col = col_list[col_num]
            print(col_num, row_num)
            data = data_list[col_num]
            if col_num == len(col_list) - 1:
                plot_cbar = True
            else:
                plot_cbar = False
            makeSubplot(data=data, var=var, cbar_data=cbar_data, grid=grid1,
                        row_num=row_num, col_num=col_num, ylabel=row['ylabel'], parallels=col['parallels'],
                        meridians=col['meridians'], title=col['title'], plot_cbar=plot_cbar)

    # fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/row_matrix_o_pot_temp_3'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()

row_list = [row_o_pot_temp]

col_list = [col_0, col_1, col_22, col_39]

filetype = 'oijlpc'

rowMatrixMap(row_list, col_list, filetype, depth = 3)
