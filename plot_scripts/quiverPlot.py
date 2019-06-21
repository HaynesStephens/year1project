from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.patches import Polygon
from cbar import MidPointNorm
from files_n_vars import *

col_list = [col_0, col_22, col_26]

def avgDataFiles3D(filedir, var, num_files, filetype, unit_conv, depth):
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

def quiverSubPlot(col, ax, tit_ad, filetype, unit_conv, depth, num_files = 10):
    filedir = col['filedir']
    parallels = col['parallels']
    meridians = col['meridians']
    title = col['title']
    if filetype == 'oijlpc':
        u = avgDataFiles3D(filedir, 'u', num_files, filetype, unit_conv, depth)
        v = avgDataFiles3D(filedir, 'v', num_files, filetype, unit_conv, depth)
    elif filetype == 'aijpc':
        u = avgDataFiles3D(filedir, 'usurf', num_files, filetype, unit_conv, depth)
        v = avgDataFiles3D(filedir, 'vsurf', num_files, filetype, unit_conv, depth)
    uv_mag = np.sqrt((u*u) + (v*v))

    m = Basemap(ax = ax)
    # m.drawcoastlines()
    # m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels([-60, -30, 0, 30, 60], labels=[1,0,0,0], ax = ax, rotation=30, fontsize=8, linewidth=0)
    m.drawmeridians([-135, -90, -45, 0, 45, 90, 135], labels=[0,0,0,1], ax = ax, rotation=0, fontsize=8, linewidth=0)

    ny=u.shape[0]
    nx=u.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)
    plt.gca().patch.set_color('.25')
    cs = m.contourf(x, y, uv_mag, ax=ax, cmap='Reds')
    m.ax.tick_params(labelsize=2)
    m.colorbar(mappable=cs, ax=ax, label='m/s')

    def getScale(filetype):
        if filetype == 'aijpc':
            key_scale = 500
            U = 10
        elif filetype == 'oijlpc':
            key_scale = 150
            U = 1
        key_label = '{0} m/s'.format(U)
        return key_scale, U, key_label

    key_scale, U, key_label = getScale(filetype)
    q = m.quiver(x, y, u, v, ax=ax, scale_units='width', scale=key_scale,
                 pivot='middle', width=0.001, headwidth=7, headlength=5)
    ax.quiverkey(q, X=0.93, Y=1.02, U=U, label = key_label, labelpos = 'E')

    if title != 'Aqua':
        x1, y1 = m(meridians[0], parallels[0])
        x2, y2 = m(meridians[0], parallels[1])
        x3, y3 = m(meridians[1], parallels[1])
        x4, y4 = m(meridians[1], parallels[0])
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none', edgecolor='black', linewidth=1)
        plt.gca().add_patch(cont_boundary)

    if filetype=='aijpc':
        ax.set_title(title, fontsize=10)
    ax.set_ylabel(tit_ad, fontsize=10, labelpad=30)


def quiverPlot():
    fig, axes = plt.subplots(2,2, figsize = (10,7))
    col = col_0
    ax0 = axes[0,0]
    quiverSubPlot(col=col, ax=ax0, tit_ad='Air Surface Velocity', filetype='aijpc', unit_conv=1, depth=None)
    ax1 = axes[0,1]
    quiverSubPlot(col=col, ax=ax1, tit_ad='Ocean Surface Velocity', filetype='oijlpc', unit_conv=0.1, depth=0)

    ax2 = axes[1, 0]
    quiverSubPlot(col=col, ax=ax2, tit_ad='Ocean 1 Layer', filetype='oijlpc', unit_conv=0.1, depth=1)
    ax3 = axes[1, 1]
    quiverSubPlot(col=col, ax=ax3, tit_ad='Ocean 2 Layer', filetype='oijlpc', unit_conv=0.1, depth=5)


    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/quiver_0_1p'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()

quiverPlot()
