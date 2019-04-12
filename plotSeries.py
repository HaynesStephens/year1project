import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

def makeSubPlots(runid = 'pc_proxcenb_ssc5L_TL_11p',
                 runbase = '/project2/abbot/haynes/ROCKE3D_output/',
                 data_file = 'ts_data'):
    rundir = runbase + runid

    os.chdir(rundir) # Switch on over to the run directory.

    df = pd.read_csv(data_file + '.csv')

    fig, axes = plt.subplots(2, 2, figsize=(9,9))

    def makeSubPlot(x, y, x_lab, y_lab, i, j):
        axes[i, j].plot(x, y)
        axes[i, j].set_xlabel(x_lab)
        axes[i, j].set_ylabel(y_lab)

    x = df['decade'] * 10
    x_lab = 'Year'
    y_list = ['radiation', 'temperature', 'snow_ice_cover', 'ice_thickness']
    y_lab_list = ['Net Radiation (W/m^2)', 'Temperature (C)', 'Snow Ice Cover (%)', 'Ice Thickness (m)']

    for num in range(4):
        i = num // 2
        j = num % 2
        y = df[y_list[num]]
        y_lab = y_lab_list[num]
        makeSubPlot(x, y, x_lab, y_lab, i, j)

    fig.suptitle(runid, y=1, fontsize=10)
    fig.tight_layout()
    # plt.savefig(data_file + '.svg')
    plt.savefig(data_file + '.pdf')
    plt.show()
    print('data saved.')
    return


def makeIcePlots(runid = 'pc_proxcenb_ssc5L_TL_11p',
                 runbase = '/project2/abbot/haynes/ROCKE3D_output/',
                 data_file = 'ts_data'):
    rundir = runbase + runid

    os.chdir(rundir) # Switch on over to the run directory.

    df = pd.read_csv(data_file + '.csv')

    fig, axes = plt.subplots(1, 3, figsize=(9,9), sharey='col')

    x = df['decade'] * 10
    x = x
    x_lab = 'Year'

    net_rad = df['radiation']
    net_rad = net_rad

    dh_ice = df['ice_thickness']
    rho_ice = 916.9 # kg/m^3
    EF_ice = 333.55 * 10**3 #J/kg
    dt = 10*11.186*24*3600 #seconds in a ProxCenb decade
    ice_flux = []
    for i in range(len(dh_ice)-1):
        h_i = dh_ice[i]
        h_f = dh_ice[i+1]
        dh = h_f - h_i
        ice_flux_i = (dh/dt) * EF_ice * rho_ice
        ice_flux.append(ice_flux_i)
    ice_flux = np.array(ice_flux)
    ax0 = axes[0]
    ax0.plot(x, net_rad)
    ax0.set_xlabel(x_lab)
    ax0.set_ylabel('Net Radiation (W/m^2)')
    ax0.set_ylim(-10, 10)

    ax1 = axes[1]
    ax1.plot(x[1:], ice_flux)
    ax1.set_xlabel(x_lab)
    ax1.set_ylabel('Ice Radiation (W/m^2)')
    ax1.set_ylim(-10, 10)

    ax2 = axes[2]
    ax2.plot(x[1:], ice_flux + net_rad[1:])
    ax2.set_xlabel(x_lab)
    ax2.set_ylabel('Ice + Net (W/m^2)')
    ax2.set_ylim(-10, 10)

    fig.suptitle(runid+'Ice-Rad Check', y=1, fontsize=10)
    fig.tight_layout()
    # plt.savefig(data_file + '_ice_rad.svg')
    plt.savefig(data_file + '_ice_rad.pdf')
    plt.show()
    print('data saved.')
    return


makeIcePlots()
# makeSubPlots()


