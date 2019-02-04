import numpy as np
import os
import pandas as pd

filedir = '/project2/abbot/haynes/ROCKE3D_output/pc_proxcenb_ssc5L_TL_22p/'
filename = filedir+'ts_data.csv'

df = pd.read_csv(filename)

print(df['radiation'][-10:])

print(df['radiation'][-10:] / 10)


