import numpy as np
import pandas as pd
from netCDF4 import Dataset as ds
import matplotlib.pyplot as plt

def showAvgNetRad(filename):
    df = pd.read_csv(filename)
    print(df['radiation'][-10:])
    print(np.mean(df['radiation'][-10:]))
    return


def oceanPotTemp(filename):
    nc = ds(filename, 'r+', format='NETCDF4')
    pot_temp = nc['pot_temp'][:]
    avg_pot_temp = np.array([])
    for o_layer in pot_temp:
        avg_pot_temp = np.append(avg_pot_temp, np.mean(o_layer))
    print('Avg Pot Temp (Celsius)')
    print(avg_pot_temp)
    return

def iceGrowth(filedir, filename1, filename2):
    nc1 = ds(filedir+filename1, 'r+', format='NETCDF4')
    zsi1 = nc1['ZSI'][:]
    net_rad1 = nc1['net_rad_planet'][:]

    nc2 = ds(filedir + filename2, 'r+', format='NETCDF4')
    zsi2 = nc2['ZSI'][:]
    net_rad2 = nc2['net_rad_planet'][:]

    def getScale(arr1, arr2, div=True):
        arr1_max = np.max(np.abs(arr1))
        arr2_max = np.max(np.abs(arr2))
        tot_max = max(arr1_max, arr2_max)
        if div:
            tot_min = tot_max * -1
        else:
            arr1_min = np.min(np.abs(arr1))
            arr2_min = np.min(np.abs(arr2))
            tot_min = min(arr1_min, arr2_min)
        return tot_min, tot_max

    fig, axes = plt.subplots(2, 2)
    ax1 = axes[0,0]
    ax1.set_title('Ice Thickness Growth [m]')
    zsi_min, zsi_max = getScale(zsi1, zsi2)

    im1 = ax1.imshow(zsi1, cmap='Blues', vmin = 0, vmax = zsi_max)
    fig.colorbar(im1, ax=ax1)

    ax2 = axes[0, 1]
    im2 = ax2.imshow(zsi2, cmap='Blues', vmin = 0, vmax = zsi_max)
    fig.colorbar(im2, ax=ax2)

    ax3 = axes[1, 0]
    ax3.set_title('Net Radiation [Wm$^{-2}$]')
    rad_min, rad_max = getScale(net_rad1, net_rad2)
    im3 = ax3.imshow(net_rad1, cmap='seismic', vmin=rad_min, vmax=rad_max)
    fig.colorbar(im3, ax=ax3)

    ax4 = axes[1, 1]
    im4 = ax4.imshow(net_rad2, cmap='seismic', vmin=rad_min, vmax=rad_max)
    fig.colorbar(im4, ax=ax4)

    plt.tight_layout()
    plt.show()


    # def avgDataFiles(filedir, var, num_files=10):
    #     results = glob('{0}/*aij*'.format(filedir))
    #     arr_tot = np.zeros((46, 72))
    #     for filename in results:
    #         nc_i = ds(filename, 'r+', format='NETCDF4')
    #         arr = nc_i[var][:]
    #         arr_tot = arr_tot + arr
    #     arr_avg = arr_tot / num_files
    #     return arr_avg






