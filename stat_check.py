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

    nc2 = ds(filedir + filename2, 'r+', format='NETCDF4')
    zsi2 = nc2['ZSI'][:]
    growth = zsi2 - zsi1
    growth[growth < 0] = 0
    plt.imshow(growth, cmap='Blues')
    plt.colorbar()
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






