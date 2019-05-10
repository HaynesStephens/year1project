from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
from matplotlib import pyplot as plt, cm as cm
from glob import glob
from matplotlib.patches import Polygon
from cbar import MidPointNorm
from files_n_vars import *

row_list = [row_pcldt, row_lwp]

col_list = [col_0, col_11, col_22, col_39]


def avgDataFiles(filedir, var, num_files = 10):
    results = glob('{0}/*aijpc*'.format(filedir))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:]
        arr_tot = arr_tot + arr
    arr_avg = arr_tot / num_files
    if 'aqua' in filedir:
        arr_avg = np.roll(arr_avg, (arr_avg.shape[1]) // 2, axis=1)
    return arr_avg


def makeSubplot(data, var, ax, row_num, col_num, ylabel, parallels, meridians, title):
    m = Basemap(ax = ax)
    # m.drawcoastlines()
    # m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels([-60, -30, 0, 30, 60], labels=[1,0,0,0], ax = ax, rotation=30, fontsize=8, linewidth=0)
    m.drawmeridians([-135, -90, -45, 0, 45, 90, 135], labels=[0,0,0,1], ax = ax, rotation=40, fontsize=8, linewidth=0)

    ny=data.shape[0]
    nx=data.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)

    def make_cmap(var):
        sequential_list = ['frac_land', 'pscld', 'pdcld', 'snowicefr', 'lwp',
                           'pcldt', 'pscld', 'pdcld', 'wtrcld', 'icecld', 'ZSI']
                            #list of sequential variables to use for cmap
        if var in sequential_list:
            cmap = cm.Blues_r
            norm = None
        else:
            cmap = cm.seismic
            norm = MidPointNorm(midpoint=0, vmin=-np.max(np.abs(data)), vmax=np.max(np.abs(data)))
        levels = 20
        return cmap, norm, levels

    cmap, norm, levels = make_cmap(var)
    plt.gca().patch.set_color('.25')
    cs = m.contourf(x, y, data, levels, ax=ax, cmap=cmap, norm=norm)
    m.ax.tick_params(labelsize=2)
    m.colorbar(mappable=cs, ax=ax)


    def ContLines(m, ax, var, x, y, data):
        if var == 'tsurf':
            m.contour(x, y, data, ax=ax, levels = [0], colors=('k',),linestyles=('-.',),linewidths=(1,))


    ContLines(m, ax, var, x, y, data)

    if title != 'Dynamic (5L), Aquaplanet':
        x1, y1 = m(meridians[0], parallels[0])
        x2, y2 = m(meridians[0], parallels[1])
        x3, y3 = m(meridians[1], parallels[1])
        x4, y4 = m(meridians[1], parallels[0])
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none', edgecolor='black', linewidth=1)
        plt.gca().add_patch(cont_boundary)

    if row_num==0:
        ax.set_title(title, fontsize=10)

    if col_num==0:
        ax.set_ylabel(ylabel, fontsize=10, labelpad = 60, rotation=0, verticalalignment ='center')


def getUniformColorbar(col_list, var):
    data_list = []
    max_val = 0
    for col in col_list:
        filedir = col['filedir']
        data = avgDataFiles(filedir, var, num_files=10)
        data_list.append(data)
        data_max = np.max(np.abs(data))
        max_val = max(max_val, data_max)
    return data_list, max_val


def matrixMaps():
    fig, axes = plt.subplots(len(row_list), len(col_list), figsize = (10,5))

    for row_num in range(len(row_list)):
        row = row_list[row_num]
        var = row['var']
        for col_num in range(len(col_list)):
            col = col_list[col_num]
            print(col_num, row_num)
            data = avgDataFiles(col['filedir'], var, num_files = 10)
            makeSubplot(data, var=var, ax=axes[row_num, col_num], row_num=row_num, col_num=col_num, ylabel=row['ylabel'],
                        parallels=col['parallels'], meridians=col['meridians'], title=col['title'])

    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/matrix_clouds4stephLWP'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()
