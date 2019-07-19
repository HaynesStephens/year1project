from lat_lon_grid import *

# FILES REPRESENT DIRECTORIES FOR DIFFERENT RUNS
filebase='/project2/abbot/haynes/ROCKE3D_output/'
filedir0=filebase+'pc_proxcenb_aqua5L_TL_500yr_rs2'
filedir1=filebase+'pc_proxcenb_ssc5L_TL_500yr_rs2'
filedir4=filebase+'pc_proxcenb_ssc5L_TL_4p'
filedir6=filebase+'pc_proxcenb_ssc5L_TL_6p'
filedir11=filebase+'pc_proxcenb_ssc5L_TL_11p'
filedir22=filebase+'pc_proxcenb_ssc5L_TL_22p'
filedir26=filebase+'pc_proxcenb_ssc5L_TL_26p'
filedir34=filebase+'pc_proxcenb_ssc5L_TL_34p'
filedir39=filebase+'pc_proxcenb_ssc5L_TL_39p'


# COLUMNS REPRESENT DIFFERENT RUNS
col_0 = {'filedir':filedir0,   'parallels':[],        'SA':0,
        'meridians':[],        'title':'Aqua'}

col_1 = {'filedir':filedir1,   'parallels':[-12, 12], 'SA':1,
        'meridians':[-15, 15], 'title':'1% Land'}

col_4 = {'filedir':filedir4,   'parallels':[-16, 16], 'SA':4,
        'meridians':[-30, 30], 'title':'4% Land'}

col_6 = {'filedir':filedir6,   'parallels':[-20, 20], 'SA':6,
        'meridians':[-35, 35], 'title':'6% Land'}

col_11 = {'filedir':filedir11, 'parallels':[-24, 24], 'SA':11,
        'meridians':[-50, 50], 'title':'11% Land'}

col_22 = {'filedir':filedir22, 'parallels':[-36, 36], 'SA':22,
        'meridians':[-70, 70], 'title':'22% Land'}

col_26 = {'filedir':filedir26, 'parallels':[-40, 40], 'SA':26,
        'meridians':[-75, 75], 'title':'26% Land'}

col_34 = {'filedir':filedir34, 'parallels':[-44, 44], 'SA':34,
        'meridians':[-90, 90], 'title':'34% Land'}

col_39 = {'filedir':filedir39, 'parallels':[-48, 48], 'SA':39,
        'meridians':[-95, 95], 'title':'39% Land'}


# ROWS REPRESENT DIFFERENT VARIABLES

############
# ATMOSPHERE
############
row_frac_land =         {'var':'frac_land',
                         'ylabel':'Land \n Fraction \n [%]',
                         'title':'Land Fraction',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_net_rad_planet =    {'var':'net_rad_planet',
                         'ylabel':'Net \n Planet \n Radiation \n [Wm$^{-2}$]',
                         'title':'Net Planet Radiation',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_tsurf =             {'var':'tsurf',
                         'ylabel':'Surface \n Temperature \n [C]',
                         'title':'Surface Temperature',
                         'units':'[$^{\circ}$C]',
                         'lat':lat,
                         'lon':lon}

row_evap =              {'var':'evap',
                         'ylabel':'Evaporation \n [mm/day]',
                         'title':'Evaporation',
                         'units':'[mm/day]',
                         'lat':lat,
                         'lon':lon}

row_prec =              {'var':'prec',
                         'ylabel':'Precipitation \n [mm/day]',
                         'title':'Precipitation',
                         'units':'mm/day',
                         'lat':lat,
                         'lon':lon}

row_qatm =              {'var':'qatm',
                         'ylabel':'Atmospheric \n Water Vapor \n [kg/m^2]',
                         'title':'Atmospheric Water Vapor',
                         'units':'[kg/m^2]',
                         'lat':lat,
                         'lon':lon}

row_snowicefr =         {'var':'snowicefr',
                         'ylabel':'Snow/Ice \n Fraction \n [%]',
                         'title':'Snow/Ice Fraction',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_ZSI =               {'var':'ZSI',
                         'ylabel':'Sea Ice \n Thickness \n [m]',
                         'title':'Sea Ice Thickness',
                         'units':'[m]',
                         'lat':lat,
                         'lon':lon}

row_lwp =               {'var':'lwp',
                         'ylabel':'Liquid \n Water \n Path \n [0.1kgm$^{-2}$]',
                         'title':'Liquid Water Path',
                         'units':'[0.1kgm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_swcrf_toa =         {'var':'swcrf_toa',
                         'ylabel':'SW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]',
                         'title':'SW Cloud Rad Forcing',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_lwcrf_toa =         {'var':'lwcrf_toa',
                         'ylabel':'LW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]',
                         'title':'LW Cloud Rad Forcing',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_srnf_toa =          {'var':'srnf_toa',
                         'ylabel':'Net Solar \n TOA \n [Wm$^{-2}$]',
                         'title':'Net Solar TOA',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_incsw_toa =         {'var':'incsw_toa',
                         'ylabel':'Incident Solar \n TOA \n [Wm$^{-2}$]',
                         'title':'Incident Solar TOA',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_srnf_grnd =         {'var':'srnf_grnd',
                         'ylabel':'Net Solar \n Surf \n [Wm$^{-2}$]',
                         'title':'Net Solar Surf',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_incsw_grnd =         {'var':'incsw_grnd',
                         'ylabel':'Incident Solar \n Surf \n [Wm$^{-2}$]',
                         'title':'Incident Solar Surf',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_trup_surf =         {'var':'trup_surf',
                         'ylabel':'Thermal Up \n Surf \n [Wm$^{-2}$]',
                         'title':'Thermal Up Surf',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_trnf_toa =         {'var':'trnf_toa',
                         'ylabel':'Thermal Net \n TOA \n [Wm$^{-2}$]',
                         'title':'Thermal Net TOA',
                         'units':'[Wm$^{-2}$]',
                         'lat':lat,
                         'lon':lon}

row_pcldt =             {'var':'pcldt',
                         'ylabel':'Total Cloud \n Cover \n [%]',
                         'title':'Total Cloud Cover',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_pcldl =             {'var':'pcldl',
                         'ylabel':'Low \n Level \n Clouds \n [%]',
                         'title':'Low Level Clouds',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_pcldm =             {'var':'pcldm',
                         'ylabel':'Middle \n Level \n Clouds \n [%]',
                         'title':'Middle Level Clouds',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_pcldh =             {'var':'pcldh',
                         'ylabel':'High \n Level \n Clouds \n [%]',
                         'title':'High Level Clouds',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_pscld =             {'var':'pscld',
                         'ylabel':'Shallow \n Convective \n Cloud \n Cover \n [%]',
                         'title':'Shallow Convective Cloud Cover',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_pdcld =             {'var':'pdcld',
                         'ylabel':'Deep \n Convective \n Cloud \n Cover \n [%]',
                         'title':'Deep Convective Cloud Cover',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_wtrcld =            {'var':'wtrcld',
                         'ylabel':'Water \n Cloud Cover \n [%]',
                         'title':'Water Cloud Cover',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_icecld =            {'var':'icecld',
                         'ylabel':'Ice \n Cloud Cover \n [%]',
                         'title':'Ice Cloud Cover',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_plan_alb =           {'var':'plan_alb',
                         'ylabel':'Planetary \n Albedo \n [%]',
                         'title':'Planetary Albedo',
                         'units':'[%]',
                         'lat':lat,
                         'lon':lon}

row_temp =               {'var':'temp',
                         'ylabel':'Temperature \n [C]',
                         'title':'Temperature',
                         'units':'[C]',
                         'lat':lat,
                         'lon':lon,
                         'z':plm}

row_tb =                 {'var':'tb',
                         'ylabel':'Temperature \n [C]',
                         'title':'Temperature',
                         'units':'[C]',
                         'lat':lat2,
                         'lon':lon2,
                         'z':plm}

row_ub =                 {'var':'ub',
                         'ylabel':'Zonal Wind \n [m/s]',
                         'title':'Zonal Wind',
                         'units':'[m/s]',
                         'lat':lat2,
                         'lon':lon2,
                          'z':plm}

row_vb =                 {'var':'vb',
                         'ylabel':'Meridional Wind \n [m/s]',
                         'title':'Meridional Wind',
                         'units':'[m/s]',
                         'lat':lat2,
                         'lon':lon2,
                          'z':plm}

row_w =                  {'var':'w',
                         'ylabel':'Omega \n [Pa/s]',
                         'title':'Omega',
                         'units':'[Pa/s]',
                         'lat':lat,
                         'lon':lon,
                          'z':plm}


#########
# OCEAN
#########
row_o_dens =             {'var':'dens',
                         'ylabel':'Density \n [kgm$^{-3}$] \n (- 1000)',
                         'title':'Density',
                         'units':'[kgm$^{-3}$] (- 1000)',
                         'lat':lato,
                         'lon':lono,
                         'z':zoc}

row_o_pot_dens =         {'var':'pot_dens',
                         'ylabel':'Pot. Density \n [kgm$^{-3}$] \n (- 1000)',
                         'title':'Pot. Density',
                         'units':'[kgm$^{-3}$] (- 1000)',
                         'lat':lato,
                         'lon':lono,
                         'z':zoc}

row_o_pot_temp =         {'var':'pot_temp',
                         'ylabel':'Pot. Temp. \n [C]',
                         'title':'Pot. Temp.',
                         'units':'[C]',
                         'lat':lato,
                         'lon':lono,
                         'z':zoc}

row_o_salt =               {'var':'salt',
                         'ylabel':'Salinity \n [psu]',
                         'title':'Salinity',
                         'units':'[psu]',
                         'lat':lato,
                         'lon':lono,
                         'z':zoc}

row_o_u =                {'var':'u',
                         'ylabel':'East-West \n Velocity \n [cm/s]',
                         'title':'East-West Velocity',
                         'units':'[cm/s]',
                         'lat':lato,
                         'lon':lono2,
                         'z':zoc}

row_o_v =                {'var':'v',
                         'ylabel':'North-South \n Velocity \n [cm/s]',
                         'title':'North-South Velocity',
                         'units':'[cm/s]',
                         'lat':lato2,
                         'lon':lono,
                         'z':zoc}

row_o_w =                {'var':'w',
                         'ylabel':'Downward \n Velocity \n [cm/s]',
                         'title':'Downward Velocity',
                         'units':'[cm/s]',
                         'lat':lato,
                         'lon':lono,
                         'z':zoce}
