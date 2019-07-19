from netCDF4 import Dataset as ds
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from files_n_vars import *
from lat_lon_grid import *
import calculatedQuantities as calcQuant


def avgDataFilesGlobal(filedir, row, var, num_files, filetype, unit_conv, depth, side):
    results = glob('{0}/*{1}*'.format(filedir, filetype))
    arr_tot = 0
    for filename in results:
        nc_i = ds(filename, 'r+', format='NETCDF4')

        if depth == None:
            arr = nc_i[var][:]
        else:
            arr = nc_i[var][:][depth]

        if filetype == 'aijpc':
            area_arr = nc_i['axyp'][:]
        elif filetype == 'oijlpc':
            area_arr = nc_i['oxyp3'][:][depth]
        # Set area to zero in cells that have no value, excluding them from the average
        area_arr[arr.mask] = 0
        if np.where(area_arr == 0)[0].size != 0:
            print('MASK CHECK', np.where(area_arr == 0)[0].size) # If an array has a mask, check to make sure area array is masked as well.

        arr_tot = arr_tot + arr

    arr_avg = (arr_tot * unit_conv) / num_files
    # # Used primarily for planetary albedo, masking area wherever there's no value (i.e. no sunlight)
    # area_arr[np.where(arr_avg==0)] = 0
    # print(np.where(area_arr == 0)[0].size)
    # #
    if 'aqua' in filedir:
        arr_avg = np.roll(arr_avg, (arr_avg.shape[1]) // 2, axis=1)
        area_arr = np.roll(area_arr, (area_arr.shape[1]) // 2, axis=1)
        # Rolling the area so that masked values (i.e. for albedo) are rolled according to their coordinate
        # Rollling is necessary for determining side and substell averages

    return arr_avg, area_arr


def getSideMean(data, area_arr, row, side):
    lat_grid = row['lat']
    lon_grid = row['lon']
    cropped_data = data.copy()
    cropped_area = area_arr.copy()
    if side == 'Global':
        avg_val = np.sum(data * area_arr) / np.sum(area_arr)
        return avg_val

    elif side == 'Day Side':
        lon_indices = np.where(np.abs(lon_grid) < 90)[0]
    elif side == 'Night Side':
        lon_indices = np.where(np.abs(lon_grid) > 90)[0]
    elif side == 'Sub-stellar':
        lon_indices = np.where(np.abs(lon_grid) < 13)[0]
        lat_indices = np.where(np.abs(lat_grid) < 11)[0]
        cropped_data = cropped_data[lat_indices, :]
        cropped_area = cropped_area[lat_indices, :]

    cropped_data = cropped_data[:, lon_indices]
    cropped_area = cropped_area[:, lon_indices]
    avg_val = np.sum(cropped_data * cropped_area) / np.sum(cropped_area)
    return avg_val


def makeSubplot(col_list, ax, row, filetype, num_files=10, unit_conv=1, depth=None, side='Global'):
    var = row['var']
    SA_arr = []
    val_arr = []

    for col in col_list:
        filedir = col['filedir']
        SA_arr.append(col['SA'])

        arr_avg_i, area_arr_i = avgDataFilesGlobal(filedir, row, var, num_files,
                                                   filetype, unit_conv, depth, side)

        # # Calculated Planetary Albedo Scenario
        # arr_avg_i, area_arr_i, plot_row, title = calcQuant.getPlanAlbFromSol(col)
        # print("TOT MIN: {0}, TOT MAX: {1}".format(np.min(arr_avg_i), np.max(arr_avg_i)))
        # row = plot_row
        # #

        val_i = getSideMean(arr_avg_i, area_arr_i, row, side)
        val_arr.append(val_i)
    SA_arr = np.array(SA_arr)
    val_arr = np.array(val_arr)

    # print('before', np.mean(val_arr))
    # # Values used in determining planetary albedo from solar fluxes
    # sol_net = np.array([177.64417, 176.96222, 174.6022, 172.0164, 169.36081,
    #                     170.56851, 172.2582, 171.33827, 173.11499])
    # sol_inc = np.ones(9) * 220.53342
    # sol_ref = sol_inc - sol_net
    # val_arr = (sol_ref / sol_inc) * 100
    # print('after', np.mean(val_arr))
    # #

    # print('before', np.mean(val_arr))
    # # Values used in determining LW Absorption according to Lewis's method
    # therm_up_surf = np.array([234.78496, 227.99066, 220.1106, 214.61176, 208.5697,
    #                      212.37679, 215.53433, 217.7208, 221.0594 ])
    # therm_up_toa = -1 * np.array([-177.47583, -177.11324, -174.68597, -172.05318, -168.60745,
    #                          -170.4261, -172.40097, -173.3177, -175.85881])
    # lw_abs = therm_up_surf - therm_up_toa
    # val_arr = lw_abs
    # print('after', np.mean(val_arr))
    # #

    print('Values: ', val_arr)
    ax.plot(SA_arr, val_arr, color='k', marker='o', markersize=10, label = 'ROCKE-3D')

    # title = row['title']
    # title = 'Planetary Albedo from Solar'
    title = 'Longwave Absorption'
    units = row['units']

    ax.set_title(side + ' Mean ' + title)
    ax.set_xlabel('Continent size (% of total surface)')
    ax.set_ylabel(units)


def getPlotName(row, side):
    if side == 'Global':
        side_ext = 'global'
    elif side == 'Day Side':
        side_ext = 'side_day'
    elif side == 'Night Side':
        side_ext = 'side_night'
    elif side == 'Sub-stellar':
        side_ext = 'substel'
    file_name = 'plots/global/new_{0}_{1}'.format(row['var'], side_ext)
    return file_name


def globalValPlot(row, side):
    col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]
    fig, ax = plt.subplots()

    makeSubplot(col_list, ax, row, filetype='aijpc', side=side)

    fig.tight_layout(w_pad = 2.25)
    # file_name = getPlotName(row, side)
    file_name = 'plots/global/global_lw_abs'
    print('PLOT NAME:', file_name)

    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()

# row = {'var':'plan_alb_calc'}
side_list = ['Global', 'Day Side', 'Night Side', 'Sub-stellar']
row = row_trnf_toa

for side_i in side_list:
    print(side_i)
    globalValPlot(row, side_i)


