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
    return arr_avg

def quiverPlot(col, ax, tit_ad, num_files = 10, filetype='oijl', unit_conv=0.1, depth=0):
    filedir = col['filedir']
    parallels = col['parallels']
    meridians = col['meridians']
    title = col['title']
    if filetype == 'oijl':
        u = avgDataFiles3D(filedir, 'u', num_files, filetype, unit_conv, depth)
        v = avgDataFiles3D(filedir, 'v', num_files, filetype, unit_conv, depth)
    elif filetype == 'aij':
        u = avgDataFiles3D(filedir, 'usurf', num_files, filetype, unit_conv, depth)
        v = avgDataFiles3D(filedir, 'vsurf', num_files, filetype, unit_conv, depth)
    uv_mag = np.sqrt((u*u) + (v*v))

    if title == 'Dynamic (5L), Aquaplanet':
        u      = np.roll(u,      (u.shape[1])//2, axis=1)
        v      = np.roll(v,      (v.shape[1])//2, axis=1)
        uv_mag = np.roll(uv_mag, (uv_mag.shape[1]) // 2, axis=1)
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
        if filetype == 'aij':
            key_scale = 500
            U = 10
        elif filetype == 'oijl':
            key_scale = 150
            U = 1
        key_label = '{0} m/s'.format(U)
        return key_scale, U, key_label

    key_scale, U, key_label = getScale(filetype)
    q = m.quiver(x, y, u, v, ax=ax, scale_units='width', scale=key_scale,
                 pivot='middle', width=0.001, headwidth=7, headlength=5)
    ax.quiverkey(q, X=0.93, Y=1.02, U=U, label = key_label, labelpos = 'E')

    if title != 'Dynamic (5L), Aquaplanet':
        x1, y1 = m(meridians[0], parallels[0])
        x2, y2 = m(meridians[0], parallels[1])
        x3, y3 = m(meridians[1], parallels[1])
        x4, y4 = m(meridians[1], parallels[0])
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none', edgecolor='black', linewidth=1)
        plt.gca().add_patch(cont_boundary)

    if filetype=='aij':
        ax.set_title(title, fontsize=10)
    ax.set_ylabel(tit_ad, fontsize=10, labelpad=30)


def quiverPlot():
    fig, axes = plt.subplots(2,1, figsize = (10,7))

    ax0 = axes[0]
    quiverPlot(col_39, ax0, 'Air Surface Velocity', filetype='aij', unit_conv=1, depth=None)
    ax1 = axes[1]
    quiverPlot(col_39, ax1, 'Ocean Surface Velocity', filetype='oijl', unit_conv=0.1, depth=1)

    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/quiver_39p'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()