from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.patches import Polygon
from cbar import MidPointNorm
# from matplotlib.colors import from_levels_and_colors,  LinearSegmentedColormap, rgb2hex


filebase='/project2/abbot/haynes/ROCKE3D_output/'
filedir0=filebase+'pc_proxcenb_aqua5L_TL_500yr_rs2'
filedir1=filebase+'pc_proxcenb_ssc5L_TL_500yr_rs2'
filedir4=filebase+'pc_proxcenb_ssc5L_TL_4p'
filedir6=filebase+'pc_proxcenb_ssc5L_TL_6p'
filedir11=filebase+'pc_proxcenb_ssc5L_TL_11p'
filedir22=filebase+'pc_proxcenb_ssc5L_TL_22p'
filedir26=filebase+'pc_proxcenb_ssc5L_TL_26p'
filedir34=filebase+'pc_proxcenb_ssc5L_TL_34p'
filedir39=filebase+'pc_proxcenb_ssc5L_TL_39p'

row_frac_land =         {'var':'frac_land',      'ylabel':'Land \n Fraction \n [%]'}
row_net_rad_planet =    {'var':'net_rad_planet', 'ylabel':'Net \n Planet \n Radiation \n [Wm$^{-2}$]'}
row_tsurf =             {'var':'tsurf',          'ylabel':'Surface \n Temperature \n [C]'}
row_snowicefr =         {'var':'snowicefr',      'ylabel':'Snow/Ice \n Fraction \n [%]'}
row_ZSI =               {'var':'ZSI',            'ylabel':'Sea Ice \n Thickness \n [m]'}
row_lwp =               {'var':'lwp',            'ylabel':'Liquid \n Water \n Path \n [0.1kgm$^{-2}$]'}
row_swcrf_toa =         {'var':'swcrf_toa',      'ylabel':'SW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]'}
row_lwcrf_toa =         {'var':'lwcrf_toa',      'ylabel':'LW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]'}
row_pcldt =             {'var':'pcldt',          'ylabel':'Total Cloud \n Cover \n [%]'}
row_pscld =             {'var':'pscld',          'ylabel':'Shallow \n Convective \n Cloud \n Cover \n [%]'}
row_pdcld =             {'var':'pdcld',          'ylabel':'Deep \n Convective \n Cloud \n Cover \n [%]'}
row_wtrcld =            {'var':'wtrcld',         'ylabel':'Water \n Cloud Cover \n [%]'}
row_icecld =            {'var':'icecld',         'ylabel':'Ice \n Cloud Cover \n [%]'}
row_list = [row_net_rad_planet, row_tsurf, row_snowicefr, row_ZSI]

col_0 = {'filedir':filedir0, 'parallels':[],
        'meridians':[], 'title':'Dynamic (5L), Aquaplanet'}
col_1 = {'filedir':filedir1, 'parallels':[-12, 12],
        'meridians':[-15, 15], 'title':'Dynamic (5L), 1% SS Cont'}
col_4 = {'filedir':filedir4, 'parallels':[-16, 16],
        'meridians':[-30, 30], 'title':'Dynamic (5L), 4% SS Cont'}
col_6 = {'filedir':filedir6, 'parallels':[-20, 20],
        'meridians':[-35, 35], 'title':'Dynamic (5L), 6% SS Cont'}
col_11 = {'filedir':filedir11, 'parallels':[-24, 24],
        'meridians':[-50, 50], 'title':'Dynamic (5L), 11% SS Cont'}
col_22 = {'filedir':filedir22, 'parallels':[-36, 36],
        'meridians':[-70, 70], 'title':'Dynamic (5L), 22% SS Cont'}
col_26 = {'filedir':filedir26, 'parallels':[-40, 40],
        'meridians':[-75, 75], 'title':'Dynamic (5L), 26% SS Cont'}
col_34 = {'filedir':filedir34, 'parallels':[-44, 44],
        'meridians':[-90, 90], 'title':'Dynamic (5L), 34% SS Cont'}
col_39 = {'filedir':filedir39, 'parallels':[-48, 48],
        'meridians':[-95, 95], 'title':'Dynamic (5L), 39% SS Cont'}

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
    m.drawmeridians([-135, -90, -45, 0, 45, 90, 135], labels=[0,0,0,1], ax = ax, rotation=40, fontsize=8, linewidth=0)

    ny=u.shape[0]
    nx=u.shape[1]
    lons, lats = m.makegrid(nx, ny)
    x, y = m(lons, lats)

    cs = m.contourf(x, y, uv_mag, ax=ax)
    m.ax.tick_params(labelsize=2)
    m.colorbar(mappable=cs, ax=ax, label='m/s')
    q = m.quiver(x, y, u, v, ax=ax, scale_units='width', scale=150,
                 pivot='middle', width=0.001, headwidth=7, headlength=5)
    ax.quiverkey(q, X=0.93, Y=1.02, U=1, label = '1 m/s', labelpos = 'E')

    if title != 'Dynamic (5L), Aquaplanet':
        x1, y1 = m(meridians[0], parallels[0])
        x2, y2 = m(meridians[0], parallels[1])
        x3, y3 = m(meridians[1], parallels[1])
        x4, y4 = m(meridians[1], parallels[0])
        cont_boundary = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none', edgecolor='black', linewidth=1)
        plt.gca().add_patch(cont_boundary)

    ax.set_ylabel(title+': '+tit_ad, fontsize=10, pad = 0.5)



fig, axes = plt.subplots(2,1, figsize = (10,7))
ax0 = axes[0]
quiverPlot(col_39, ax0, 'Ocean Surface Velocity', filetype='oijl', unit_conv=0.1, depth=1)
ax1 = axes[1]
quiverPlot(col_39, ax1, 'Air Surface Velocity', filetype='aij', unit_conv=1, depth=None)

fig.tight_layout(w_pad = 2.25)
file_name = 'plots/quiver_39p'
# plt.savefig(file_name+'.svg')
plt.savefig(file_name+'.pdf')
plt.show()
