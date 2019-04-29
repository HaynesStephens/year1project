import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from files_n_vars import *
import latLonAvgPlot as llap
import globalValPlot as gvp


def loadCSV(filename):
    df = pd.read_csv(filename)
    return np.array(df)


def correctLon(arr):
    x = arr.copy()
    x[:, 0][x[:, 0] > 180] = x[:, 0][x[:, 0] > 180] - 360
    x = x[x[:,0].argsort()]
    return x


def correctT(arr):
    x = arr.copy()
    x[:, 1] = x[:, 1] - 273.15
    return x


def correctAndPlot(arr, ax, label):
    x = arr.copy()
    x = correctLon(x)
    x = correctT(x)
    ax.plot(x[:,0], x[:,1], label=label, linestyle='-.')


def plotLonTsurf():
    tsurf_aqua = loadCSV('LewisLonTsurfAqua.csv')
    tsurf_b2 = loadCSV('LewisLonTsurfB2.csv')
    tsurf_b7 = loadCSV('LewisLonTsurfB7.csv')

    col_list = [col_0, col_6, col_34]
    row = row_tsurf
    fig, ax = plt.subplots()

    llap.makeSubplot(col_list, ax, row, filetype='aijpc', avg_coord='lon')

    correctAndPlot(tsurf_aqua, ax, label="Aqua_L")
    correctAndPlot(tsurf_b2, ax, label='7% L')
    correctAndPlot(tsurf_b7, ax, label='34% L')
    ax.legend()
    fig.tight_layout(w_pad=2.25)
    file_name = 'plots/lewis_tsurf'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name + '.pdf')
    plt.show()


def plotGlobalVal(var):
    col_list = [col_0, col_1, col_4, col_6, col_11, col_22, col_26, col_34, col_39]

    if var =='tsurf':
        row = row_tsurf
        filename = 'LewisGlobalTsurf.csv'
    elif var =='evap':
        row = row_evap
        filename = 'LewisGlobalEvap.csv'
    label = 'Lewis'
    data = loadCSV(filename)

    fig, ax = plt.subplots()

    gvp.makeSubplot(col_list, ax, row, filetype='aijpc')
    ax.plot(data[:, 0], data[:, 1], label=label, color='r', marker='x', markersize=10)


    fig.tight_layout(w_pad = 2.25)
    file_name = 'plots/lews_global_tsurf'
    # plt.savefig(file_name+'.svg')
    plt.savefig(file_name+'.pdf')
    plt.show()

plotGlobalVal('tsurf')
