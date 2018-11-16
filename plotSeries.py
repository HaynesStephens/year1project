import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def makeSubPlots(runid = 'pc_proxcenb_aqua5L_TL_500yr_rs2',
                 runbase = '/project2/abbot/haynes/ROCKE3D_output/',
                 data_file = 'ts_data.csv'):
    rundir = runbase + runid

    os.chdir(rundir) # Switch on over to the run directory.

    df = pd.read_csv(data_file)

    fig, axes = plt.subplots(2, 2, figsize=(9,9))

    def makeSubPlot(x, y, x_lab, y_lab, i, j):
        axes[i, j].plot(x, y)
        axes[i, j].set_xlabel(x_lab)
        axes[i, j].set_ylabel(y_lab)

    x = df['decade']
    x_lab = 'Decade'
    y_list = ['radiation', 'temperature', 'snow_ice_cover', 'ice_thickness']
    y_lab_list = ['Net Radiation (W/m^2)', 'Temperature (C)', 'Snow Ice Cover (%)', 'Ice Thickness (m?)']

    for num in range(4):
        i = num // 2
        j = num % 2
        y = df[y_list[num]]
        y_lab = y_lab_list[num]
        makeSubPlot(x, y, x_lab, y_lab, i, j)

    fig.tight_layout()
    plt.show()
    plt.savefig('ts_data.svg')

    print('data saved.')
    return


