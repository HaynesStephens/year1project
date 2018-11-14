from math import sin, radians

def percent(lat1, lat2, lon1, lon2):
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    area_tot = 4
    area_grid = (abs(sin(lat1_rad) - sin(lat2_rad)) * abs(lon1 - lon2)) / 180
    percent = area_grid / area_tot
    return percent

