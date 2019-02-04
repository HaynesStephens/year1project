import numpy as np
import os
import pandas as pd

def showAvgNetRad(filename):
    df = pd.read_csv(filename)
    print(df['radiation'][-10:])
    print(np.mean(df['radiation'][-10:]))




