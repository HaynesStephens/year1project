# From Stephanie Olson's Original ROCKE_SS.py script

# encoding: utf-8

# SCRIPT TO GENERATE TIME SERIES OF GLOBALLY AVERAGED ROCKE-3D DATA
# User must specify runid and may need to modify the calendar settings. 

## ***SPECIFY EXPERIMENT & ITS LOCATION ON MIDWAY***
runid = 'pc_proxcenb_aqua5L_TL_500yr_rs2'
rundirectory = '/project2/abbot/haynes/ROCKE3D_output/' + runid
startyear = 2440
endyear = 2950


def createVarsByMonth(runid = runid, rundirectory = rundirectory):
    ## ***DEFINE TIME INTERVAL***
    # NOTE: Change year_list for runs < 1 year.

    # year_list = [1960, 1999]
    year_list = range(startyear, endyear + 1)

    ## ***DEFINE THE CALENDAR***
    #  NOTE: month_list and month_per_year may need to be modified for planets with non-std. calendars.
    #        This is particularly likely for short orbital periods / tidally locked planets.
    #        The calendar for each experiment is reported in the .PRT file

    month_list = ['D+J']
    # month_list = ['D+J', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV']
    month_per_year = 1

    # PREPARE THE DATA FOR ANALYSIS (use GISS'scaleacc' diagnostic tool)
    import subprocess
    import os

    os.system('loadmods')

    os.chdir(rundirectory)  # Switch on over to the run directory.

    for y in year_list:
        year = str(y)

        for m in month_list:
            month = str(m)
            accfilename = month + year + '.acc' + runid + '.nc'
            print(accfilename)
            subprocess.call(["scaleacc", accfilename, 'aij'])  # convert atmospheric output
        # subprocess.call(["scaleacc", accfilename, 'oij']) #convert oceananic output

    # ALLOCATE ARRAYS, ETC.
    import numpy as np

    # First, determine array size
    total_months = len(month_list) * len(year_list)

    # Create time arrays
    time_months = np.linspace(0, total_months, total_months, endpoint=False)
    time_years = time_months / month_per_year  # convert to years. NOTE: this

    # Create output arrays
    global_rad = np.zeros((total_months, 1))  # net radiation
    global_ave_temp = np.zeros((total_months, 1))  # temperature
    global_snow_ice_cover = np.zeros((total_months, 1))
    global_ice_thickness = np.zeros((total_months, 1))
    return year_list, global_rad, global_ave_temp, global_snow_ice_cover, global_ice_thickness


def createVarsByDec(runid = runid, rundirectory = rundirectory):
    ## ***DEFINE TIME INTERVAL***
    # NOTE: Change year_list for runs < 1 year.

    # year_list = [1960, 1999]
    year_list = range(startyear+10, endyear + 1, 10)

    # PREPARE THE DATA FOR ANALYSIS (use GISS'scaleacc' diagnostic tool)
    import subprocess
    import os

    os.system('loadmods')

    os.chdir(rundirectory)  # Switch on over to the run directory.

    for y in year_list:
        beg_dec = str(y - 9)
        end_dec = str(y)

        accfilename = 'AN8' + beg_dec + '-' + end_dec + '.acc' + runid + '.nc'

        print(accfilename)
        subprocess.call(["scaleacc", accfilename, 'aij'])  # convert atmospheric output
        # subprocess.call(["scaleacc", accfilename, 'oij']) #convert oceananic output

    # ALLOCATE ARRAYS, ETC.
    import numpy as np

    # First, determine array size
    total_decs = len(year_list)

    # Create time arrays
    # time_months = np.linspace(0, total_months, total_months, endpoint=False)
    # time_years = time_months / month_per_year  # convert to years. NOTE: this

    # Create output arrays
    global_rad = np.zeros((total_decs, 1))  # net radiation
    global_ave_temp = np.zeros((total_decs, 1))  # temperature
    global_snow_ice_cover = np.zeros((total_decs, 1))
    global_ice_thickness = np.zeros((total_decs, 1))
    return year_list, global_rad, global_ave_temp, global_snow_ice_cover, global_ice_thickness


def getVarsByMonth(year_list, global_rad, global_ave_temp,
                   global_snow_ice_cover, global_ice_thickness):
    # IMPORT THE DATA!
    from netCDF4 import Dataset

    i = 0  # start the calendar counter
    for y in year_list:
        year = str(y)

        for m in month_list:
            month = str(m)
            aijfilename = month + year + '.aij' + runid + '.nc'
            # oijfilename = month + year +'.oij' + runid + '.nc'

            # READ THE NETCDF FILES
            atm_data = Dataset(aijfilename)
            # ocn_data=Dataset(oijfilename)

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
            sea_ice_thickness = atm_data['ZSI'][:]  # Spatially resolved snow/ice coverage (%)
            land = np.isnan(sea_ice_thickness)
            ocean_area = planet_area - sum(grid_cell_area[land])
            sea_ice_thickness[land] = 0
            sea_ice_thickness_aw = sum(sum((sea_ice_thickness * grid_cell_area))) / ocean_area  # Snow and ice area (m2)
            global_ice_thickness[i] = sea_ice_thickness_aw

            i = i + 1  # advance the calendar counter.
    return global_rad, global_ave_temp, global_snow_ice_cover, global_ice_thickness


def getVarsByDec(year_list, global_rad, global_ave_temp,
                 global_snow_ice_cover, global_ice_thickness):
    # IMPORT THE DATA!
    from netCDF4 import Dataset

    i = 0  # start the calendar counter
    for y in year_list:
        beg_dec = str(y - 9)
        end_dec = str(y)

        aijfilename = 'AN8' + beg_dec + '-' + end_dec + '.aij' + runid + '.nc'
        # oijfilename = month + year +'.oij' + runid + '.nc'

        # READ THE NETCDF FILES
        atm_data = Dataset(aijfilename)
        # ocn_data=Dataset(oijfilename)

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
        sea_ice_thickness = atm_data['ZSI'][:]  # Spatially resolved snow/ice coverage (%)
        land = np.isnan(sea_ice_thickness)
        ocean_area = planet_area - sum(grid_cell_area[land])
        sea_ice_thickness[land] = 0
        sea_ice_thickness_aw = sum(sum((sea_ice_thickness * grid_cell_area))) / ocean_area  # Snow and ice area (m2)
        global_ice_thickness[i] = sea_ice_thickness_aw

        i = i + 1  # advance the calendar counter.
    return global_rad, global_ave_temp, global_snow_ice_cover, global_ice_thickness


def saveData(global_rad, global_ave_temp,
             global_snow_ice_cover, global_ice_thickness):

    # PRINT FINAL VALUE
    # print 'The global net radiative is: '+ global_rad[-1] +' W/m^2'
    # print 'The global average temperature is: '+ global_ave_temp[-1]+ ' C'
    # print 'Snow and ice cover '+ glocal_snow_ice_cover[-1]+ '% of the globe'

    # SAVE DATA TO FILE:
    np.savetxt('radiation_ts.txt', global_rad)
    np.savetxt('temperature_ts.txt', global_ave_temp)
    np.savetxt('snow_ice_ts.txt', global_snow_ice_cover)
    np.savetxt('ice_thickness_ts.txt', global_ice_thickness)

    import pandas as pd


    df = pd.DataFrame({'decade': np.arange(total_months), 'radiation': global_rad.reshape(total_months),
                       'temperature': global_ave_temp.reshape(total_months),
                       'snow_ice_cover': global_snow_ice_cover.reshape(total_months),
                       'ice_thickness': global_ice_thickness.reshape(total_months)})
    df.to_csv('ts_data.csv')

    os.system('rm *aij*')
