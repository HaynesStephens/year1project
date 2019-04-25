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
        'meridians':[],        'title':'Dynamic (5L), Aquaplanet'}

col_1 = {'filedir':filedir1,   'parallels':[-12, 12], 'SA':1,
        'meridians':[-15, 15], 'title':'Dynamic (5L), 1% SS Cont'}

col_4 = {'filedir':filedir4,   'parallels':[-16, 16], 'SA':4,
        'meridians':[-30, 30], 'title':'Dynamic (5L), 4% SS Cont'}

col_6 = {'filedir':filedir6,   'parallels':[-20, 20], 'SA':6,
        'meridians':[-35, 35], 'title':'Dynamic (5L), 6% SS Cont'}

col_11 = {'filedir':filedir11, 'parallels':[-24, 24], 'SA':11,
        'meridians':[-50, 50], 'title':'Dynamic (5L), 11% SS Cont'}

col_22 = {'filedir':filedir22, 'parallels':[-36, 36], 'SA':22,
        'meridians':[-70, 70], 'title':'Dynamic (5L), 22% SS Cont'}

col_26 = {'filedir':filedir26, 'parallels':[-40, 40], 'SA':26,
        'meridians':[-75, 75], 'title':'Dynamic (5L), 26% SS Cont'}

col_34 = {'filedir':filedir34, 'parallels':[-44, 44], 'SA':34,
        'meridians':[-90, 90], 'title':'Dynamic (5L), 34% SS Cont'}

col_39 = {'filedir':filedir39, 'parallels':[-48, 48], 'SA':39,
        'meridians':[-95, 95], 'title':'Dynamic (5L), 39% SS Cont'}


# ROWS REPRESENT DIFFERENT VARIABLES
row_frac_land =         {'var':'frac_land',
                         'ylabel':'Land \n Fraction \n [%]',
                         'title':'Land Fraction',
                         'units':'[%]'}

row_net_rad_planet =    {'var':'net_rad_planet',
                         'ylabel':'Net \n Planet \n Radiation \n [Wm$^{-2}$]',
                         'title':'Net Planet Radiation',
                         'units':'[Wm$^{-2}$]'}

row_tsurf =             {'var':'tsurf',
                         'ylabel':'Surface \n Temperature \n [C]',
                         'title':'Surface Temperature',
                         'units':'[$^{\circ}$C]'}

row_evap =              {'var':'evap',
                         'ylabel':'Evaporation \n [mm/day]',
                         'title':'Evaporation',
                         'units':'[mm/day]'}

row_prec =              {'var':'prec',
                         'ylabel':'Precipitation \n [mm/day]',
                         'title':'Precipitation',
                         'units':'mm/day'}

row_qatm =              {'var':'qatm',
                         'ylabel':'Atmospheric \n Water Vapor \n [kg/m^2]',
                         'title':'Atmospheric Water Vapor',
                         'units':'[kg/m^2]'}

row_snowicefr =         {'var':'snowicefr',
                         'ylabel':'Snow/Ice \n Fraction \n [%]',
                         'title':'Snow/Ice Fraction',
                         'units':'[%]'}

row_ZSI =               {'var':'ZSI',
                         'ylabel':'Sea Ice \n Thickness \n [m]',
                         'title':'Sea Ice Thickness',
                         'units':'[m]'}

row_lwp =               {'var':'lwp',
                         'ylabel':'Liquid \n Water \n Path \n [0.1kgm$^{-2}$]',
                         'title':'Liquid Water Path',
                         'units':'[0.1kgm$^{-2}$]'}

row_swcrf_toa =         {'var':'swcrf_toa',
                         'ylabel':'SW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]',
                         'title':'SW Cloud Rad Forcing',
                         'units':'[Wm$^{-2}$]'}

row_lwcrf_toa =         {'var':'lwcrf_toa',
                         'ylabel':'LW \n Cloud \n Rad \n Forcing \n [Wm$^{-2}$]',
                         'title':'LW Cloud Rad Forcing',
                         'units':'[Wm$^{-2}$]'}

row_pcldt =             {'var':'pcldt',
                         'ylabel':'Total Cloud \n Cover \n [%]',
                         'title':'Total Cloud Cover',
                         'units':'[%]'}

row_pscld =             {'var':'pscld',
                         'ylabel':'Shallow \n Convective \n Cloud \n Cover \n [%]',
                         'title':'Shallow Convective Cloud Cover',
                         'units':'[%]'}

row_pdcld =             {'var':'pdcld',
                         'ylabel':'Deep \n Convective \n Cloud \n Cover \n [%]',
                         'title':'Deep Convective Cloud Cover',
                         'units':'[%]'}

row_wtrcld =            {'var':'wtrcld',
                         'ylabel':'Water \n Cloud Cover \n [%]',
                         'title':'Water Cloud Cover',
                         'units':'[%]'}

row_icecld =            {'var':'icecld',
                         'ylabel':'Ice \n Cloud Cover \n [%]',
                         'title':'Ice Cloud Cover',
                         'units':'[%]'}
