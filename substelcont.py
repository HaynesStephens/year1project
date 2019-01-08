import numpy as np
from netCDF4 import Dataset as ds


def openNC(fdir, fname):
    """
    Load the Dataset nc file.
    """
    filename = '/home/haynes13/code/python/input_files/' + fdir + '/' + fname
    nc = ds(filename, 'r+', format='NETCDF4') #ssc = substellar continent
    print(nc)
    print('Dataset Loaded Successfully.')
    return nc


def emptyMap(shape = (46, 72)):
    """
    Create a blank template of zeros
    with the same shape as a given grid map.
    """
    empty_map = np.zeros(shape)
    return empty_map


def changeMap(nc, map_in, lat_lo, lat_hi, lon_lo, lon_hi, val=1, n_dim=2, ocean=False):
    """
    Put VAL in a given area of your grid map.
    This function is designed so that hi values are included in the indexing,
    so there will be ones at lat_hi and lon_hi.
    All LAT/LON inputs in this function should be integer values that correspond to
    the appropriate latitude and longitude values to be used in ROCKE-3D.
    """
    assert lat_lo <= lat_hi, "Your highest latitude cannot be lower than your lowest latitude."
    assert lon_lo <= lon_hi, "Your highest longitude cannot be lower than your lowest longitude."

    def returnIndex(nc, name, coord, ocean):
        if ocean:
            name = name + 'o'
        index_arr = np.where(nc[name][:]==coord)[0]
        assert index_arr.size == 1, "There is no value {0} in the {1} array".format(coord, name)
        return index_arr[0]

    lat_lo_i = returnIndex(nc, 'lat', lat_lo, ocean)
    lat_hi_i = returnIndex(nc, 'lat', lat_hi, ocean)
    lon_lo_i = returnIndex(nc, 'lon', lon_lo, ocean)
    lon_hi_i = returnIndex(nc, 'lon', lon_hi, ocean)

    if n_dim==3:
        num_layers = map_in.shape[0]
        for i in range(num_layers):
            map_in[i][lat_lo_i : lat_hi_i + 1, lon_lo_i: lon_hi_i + 1] = val
    elif n_dim==2:
        map_in[lat_lo_i : lat_hi_i + 1, lon_lo_i: lon_hi_i + 1] = val

    map_out = map_in

    return map_out


def changeVar(var, new_map, nc):
    """
    Change the VAR array on the NC file.
    to the NEW_MAP.
    """
    nc[var][:] = new_map
    return nc


def alterOIC(fdir, fname, lat_lo, lat_hi, lon_lo, lon_hi):
    var_list = ['mo', 'g', 'gz', 's', 'sz']
    nc = openNC(fdir, fname)
    for var_i in var_list:
        new_map = changeMap(nc, nc[var_i][:], lat_lo, lat_hi, lon_lo, lon_hi, val=0, n_dim=3, ocean=True)
        nc = changeVar(var_i, new_map, nc)
    return


def alterTOPO(fdir, fname, lat_lo, lat_hi, lon_lo, lon_hi):
    var_list = ['focean', 'fgrnd']
    nc = openNC(fdir, fname)
    for var_i in var_list:

        if var_i == 'focean':
            val = 0
        else:
            val = 1

        new_map = changeMap(nc, nc[var_i][:], lat_lo, lat_hi, lon_lo, lon_hi, val=val, n_dim=2, ocean=False)
        nc = changeVar(var_i, new_map, nc)
    return


def alterTOPO_OC(fdir, fname, lat_lo, lat_hi, lon_lo, lon_hi):
    var_list = ['focean', 'zocean']
    nc = openNC(fdir, fname)
    for var_i in var_list:

        if var_i == 'focean':
            val = 0
        else:
            val = 30

        new_map = changeMap(nc, nc[var_i][:], lat_lo, lat_hi, lon_lo, lon_hi, val=val, n_dim=2, ocean=True)
        nc = changeVar(var_i, new_map, nc)
    return


fdir = '4p'
fbase_name = '.ssc.latpn14.lonpn27_5.4p.nc'

lat = 16 # lat given from spreadsheet that outlines ACTUAL continent, NOT from GRID coords (see spreadsheet)
         # https://docs.google.com/spreadsheets/d/1Cp85DWFq9kVjZ96rZPasCS9Nhny64671wVQjHS_XUNI/edit#gid=0
         # you can see in the fbase_name that the GRID coordinates are given there, and they are
         # different from the ACTUAL coordinates
lat_lo = (lat - 2) * (-1)
lat_hi = lat - 2

lon = 30 # lat given from spreadsheet that outlines ACTUAL continent, NOT from GRID coords (see spreadsheet)
         # https://docs.google.com/spreadsheets/d/1Cp85DWFq9kVjZ96rZPasCS9Nhny64671wVQjHS_XUNI/edit#gid=0
         # you can see in the fbase_name that the GRID coordinates are given there, and they are
         # different from the ACTUAL coordinates
lon_lo = (lon - 2.5) * (-1)
lon_hi = (lon - 2.5)

alterOIC(fdir, 'OIC' + fbase_name, lat_lo, lat_hi, lon_lo, lon_hi)
alterTOPO(fdir, 'Z' + fbase_name, lat_lo, lat_hi, lon_lo, lon_hi)
alterTOPO_OC(fdir, 'OZ' + fbase_name, lat_lo, lat_hi, lon_lo, lon_hi)

