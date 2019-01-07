import pandas as pd

csv1 = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_aqua5L_TL_500yr/ts_data.csv'
csv2 = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_aqua5L_TL_500yr_rs1/ts_data.csv'
new_csv = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_aqua5L_TL_500yr/ts_data_tot.csv'

def mergeData(csv1, csv2):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    result = df1.append(df2)
    return result

def saveMergedData(result, new_csv):
    result.to_csv(new_csv)

result = mergeData(csv1, csv2)
saveMergedData(result, new_csv)
