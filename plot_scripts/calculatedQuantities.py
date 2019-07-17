from files_n_vars import *
from lat_lon_grid import *

def getPlanAlbFromSol(col, filetype = 'aijpc', num_files = 10):
    filedir = col['filedir']
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = 0
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')
        net_i = nc_i['srnf_toa'][:]
        inc_i = nc_i['incsw_toa'][:]
        out_i = inc_i - net_i
        albedo_i = (out_i / inc_i) * 100
        arr_tot = arr_tot + albedo_i
    arr_avg = arr_tot / num_files
    if 'aqua' in filedir: #if it's aquaplanet simulation you need to roll so that substell point is in middle
        roll_size = arr_avg.shape[-1]
        roll_axis = len(arr_avg.shape) - 1
        arr_avg = np.roll(arr_avg, (roll_size) // 2, axis=roll_axis)
    data = arr_avg
    plot_row = {'var':'None',
                'ylabel':'Calculated \n Planetary \n Albedo \n [%]',
                'title':'Calculated Planetary Albedo',
                'units':'[%]',
                'lat':lat,
                'lon':lon}
    title = col['title']
    return data, plot_row, title


