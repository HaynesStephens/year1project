from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset as ds
import numpy as np
from matplotlib import pyplot as plt, cm as cm
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
row_list = [row_net_rad_planet, row_tsurf]

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

col_list = [col_0, col_1, col_39]


def avgDataFiles(filedir, var, num_files = 10):
    results = glob('{0}/*aij*'.format(filedir))
    arr_tot = np.zeros((46,72))
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        arr = nc_i[var][:]
        arr_tot = arr_tot + arr
    arr_avg = arr_tot / num_files
    return arr_avg


def makeSubplot(data, var, ax, row_num, col_num, ylabel, parallels, meridians, title):
    if title == 'Dynamic (5L), Aquaplanet':
        data = np.roll(data, (data.shape[1])//2, axis=1)
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
            m.contour(x, y, data, ax=ax, levels = [273.15], colors=('k',),linestyles=('-.',))


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

fig, axes = plt.subplots(len(row_list), len(col_list), figsize = (10,7))

for col_num in range(len(col_list)):
    col = col_list[col_num]
    filedir = col['filedir']
    for row_num in range(len(row_list)):
        print(col_num, row_num)
        row = row_list[row_num]
        var = row['var']
        data = avgDataFiles(filedir, var, num_files = 10)
        makeSubplot(data, var=var, ax=axes[row_num, col_num], row_num=row_num, col_num=col_num, ylabel=row['ylabel'],
                    parallels=col['parallels'], meridians=col['meridians'], title=col['title'])

fig.tight_layout(w_pad = 2.25)
file_name = 'plots/contour_test'
# plt.savefig(file_name+'.svg')
plt.savefig(file_name+'.pdf')
plt.show()
