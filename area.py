from math import sin, radians

def percent(lat1, lat2, lon1, lon2):
    """
    Return the percent of surface area covered between the coordinates.
    :param lat1: First latitude coordinate (degrees)
    :param lat2: Second latitude coordinate (degrees)
    :param lon1: First longitude coordinate (degrees)
    :param lon2: Second longitude coordinate (degrees)
    :return: Percent coverage of surface area (%)
    """
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    area_tot = 4
    area_grid = (abs(sin(lat1_rad) - sin(lat2_rad)) * abs(lon1 - lon2)) / 180
    percent = area_grid / area_tot
    return percent

