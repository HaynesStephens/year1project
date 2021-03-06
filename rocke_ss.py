# From Stephanie Olson's Original ROCKE_SS.py script

# encoding: utf-8

# SCRIPT TO GENERATE TIME SERIES OF GLOBALLY AVERAGED ROCKE-3D DATA
# User must specify runid and may need to modify the calendar settings.

import numpy as np
import os
import subprocess
from netCDF4 import Dataset
import pandas as pd
from glob import glob

## ***SPECIFY EXPERIMENT & ITS LOCATION ON MIDWAY***
runid = 'pc_proxcenb_ssc5L_TL_39p'
rundirectory = '/project2/abbot/haynes/ROCKE3D_output/' + runid

endyear_dict = {'0p':3500, '1p':4140, '4p':3549, '6p':4179,
                '11p':4379, '22p':3729, '26p':3649, '34p':2769, '39p':2649}
endyear = endyear_dict['39p']
startyear = endyear - 99
# startyear = ####




## ***DEFINE TIME INTERVAL***
# NOTE: Change year_list for runs < 1 year.

# year_list = [1960, 1999]
year_list = range(startyear, endyear, 10)

# PREPARE THE DATA FOR ANALYSIS (use GISS'scaleacc' diagnostic tool)

os.chdir(rundirectory)  # Switch on over to the run directory.
file_start = 'ANM'

for y in year_list:
    beg_dec = str(y)
    end_dec = str(y + 9)

    accfilename = file_start + beg_dec + '-' + end_dec + '.acc' + runid + '.nc'

    print(accfilename)
    ext_list = ['aijk', 'aijl', 'aij', 'icij', 'oijl', 'oij']
    tot_list = ['aj', 'areg', 'consrv', 'ajl', 'agc', 'aij', 'aijmm', 'aijl', 'aijk', 'adiurn', 'hdiurn'
                'ijhc', 'oij', 'oijmm', 'oijl', 'olnst', 'ojl', 'otj, icij']
    for ext in ext_list:
        subprocess.call(["scaleacc", accfilename, ext])
    # subprocess.call(["scaleacc", accfilename, 'aij'])  # convert atmospheric output
    # subprocess.call(["scaleacc", accfilename, 'oij']) #convert oceananic output
    # subprocess.call(["scaleacc", accfilename, 'oijl'])  # convert oceananic output

''' NOT TRYING TO REPRODUCE ALL DATA AGAIN THIS TIME
# First, determine array size
total_decs = len(year_list)

# Create output arrays
global_rad = np.zeros((total_decs, 1))  # net radiation
global_ave_temp = np.zeros((total_decs, 1))  # temperature
global_snow_ice_cover = np.zeros((total_decs, 1))
global_ice_thickness = np.zeros((total_decs, 1))

# IMPORT THE DATA!

i = 0  # start the calendar counter
for y in year_list:
    beg_dec = str(y)
    end_dec = str(y + 9)

    aijfilename  = file_start + beg_dec + '-' + end_dec + '.aij'  + runid + '.nc'
    oijfilename  = file_start + beg_dec + '-' + end_dec + '.oij'  + runid + '.nc'
    oijlfilename = file_start + beg_dec + '-' + end_dec + '.oijl' + runid + '.nc'

    # READ THE NETCDF FILES
    atm_data = Dataset(aijfilename)
    ocn_data=Dataset(oijfilename)
    ocnl_data = Dataset(oijlfilename)

    # GET AREAS -- this could probably be moved outside of the for loop... but, is necessary for
    grid_cell_area = atm_data['axyp'][:]  # Area of each grid cell (m^2)
    planet_area = sum(sum(grid_cell_area))  # Surface area of planet (m^2)

    # NET RADIATION
    net_rad = atm_data['net_rad_planet'][:]  # Spatially resolved net radiation (W/m^2) from netcdf
    tot_rad = sum(sum(net_rad * grid_cell_area))  # Total global radiation (W)
    tot_rad = tot_rad / planet_area  # Spread across planet's surface
    global_rad[i] = tot_rad  # Record globally averaged net radiation

    # SURFACE TEMPERATURE
    surf_temp = atm_data['tsurf'][:]  # Spatially resolved surface temperature (C)
    surf_temp_aw = sum(
        sum((surf_temp * grid_cell_area))) / planet_area  # Area weighted global average surface temp.
    global_ave_temp[i] = surf_temp_aw  # Record the global average

    # SNOW AND ICE COVERAGE
    snow_ice_cover = atm_data['snowicefr'][:]  # Spatially resolved snow/ice coverage (%)
    snow_ice_area = sum(sum((snow_ice_cover * grid_cell_area)))  # Snow and ice area (m2)
    global_snow_ice_cover[i] = snow_ice_area / planet_area  # Global snow and ice coverage (%)

    # SEA ICE THICKNESS
    sea_ice_thickness = atm_data['ZSI'][:]  # Spatially resolved sea ice thickness (m)
    sea_ice_thickness[sea_ice_thickness.mask] = 0

    ocnfr = atm_data['ocnfr'][:]
    ocean_area = (ocnfr / 100) * grid_cell_area

    total_thickness = np.sum(sea_ice_thickness * ocean_area)
    sea_ice_thickness_aw = total_thickness / np.sum(ocean_area)

    global_ice_thickness[i] = sea_ice_thickness_aw

    i = i + 1  # advance the calendar counter.


# PRINT FINAL VALUE
# print 'The global net radiative is: '+ global_rad[-1] +' W/m^2'
# print 'The global average temperature is: '+ global_ave_temp[-1]+ ' C'
# print 'Snow and ice cover '+ glocal_snow_ice_cover[-1]+ '% of the globe'

# SAVE DATA TO FILE:
np.savetxt('radiation_ts.txt', global_rad)
np.savetxt('temperature_ts.txt', global_ave_temp)
np.savetxt('snow_ice_ts.txt', global_snow_ice_cover)
np.savetxt('ice_thickness_ts.txt', global_ice_thickness)


a_df = pd.DataFrame({'decade': np.arange(total_decs), 'radiation': global_rad.reshape(total_decs),
                   'temperature': global_ave_temp.reshape(total_decs),
                   'snow_ice_cover': global_snow_ice_cover.reshape(total_decs),
                   'ice_thickness': global_ice_thickness.reshape(total_decs)})
a_df.to_csv('a_ts_data.csv')
'''

''' DONT NEED TO DELETE, NEED TO FIGURE OUT HOW TO SEPARATE OIJ AND OIJL FIRST
## Delete all but the last 10 aij files to use in the matrix map plots.
aij_list = sorted(glob('*aij*')) # Get a list of all the aij files made.
for aij_file in aij_list[:-10]: # Cycle through a list of all but the last 10 aij files.
    os.system('rm {0}'.format(aij_file)) # Delete the aij file.

## Delete all but the last 10 oij files to use in the matrix map plots.
oij_list = sorted(glob('*oij*')) # Get a list of all the oij files made.
for oij_file in oij_list[:-10]: # Cycle through a list of all but the last 10 oij files.
    os.system('rm {0}'.format(oij_file)) # Delete the oij file.

## Delete all but the last 10 oijl files to use in the matrix map plots.
oijl_list = sorted(glob('*oijl*')) # Get a list of all the oijl files made.
for oij_file in oijl_list[:-10]: # Cycle through a list of all but the last 10 oijl files.
    os.system('rm {0}'.format(oijl_file)) # Delete the oijl file.
'''
