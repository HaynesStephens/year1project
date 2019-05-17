# This script merges separate *data.csv timeseries into a single file.
# It was used on the aqua and 1% runs because I stupidly had their restarts
# put into separate directories.
import pandas as pd

csv1 = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_aqua5L_TL_500yr/ts_data.csv'
csv2 = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_aqua5L_TL_500yr_rs2/ts_data.csv'
new_csv = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_aqua5L_TL_500yr/ts_data_tot.csv'

def mergeData(csv1, csv2):
    """
    Merge the two timeseries files into one total timeseries.
    :param csv1: filename of the first (older) timeseries
    :param csv2: filename of the second (newer) timeseries
    Done by appending csv2 to csv1 and creating a new csv file.
    :return: A new, total csv file
    """
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    result = df1.append(df2)
    result.index = range(len(result.index))
    result['decade'] = result.index #take the indexing of items and make that the number of decades.
    return result

def saveMergedData(result, new_csv):
    result.to_csv(new_csv)

result = mergeData(csv1, csv2)
saveMergedData(result, new_csv)
