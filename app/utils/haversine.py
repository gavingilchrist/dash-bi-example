from math import sin, cos, asin, radians


def haversine(*args):
    """
    Calculate Haversine distance in miles between points (degree coords)
    """
    lat0,long0,lat1,long1 = [radians(i) for i in args]
    return (7918 
            * asin(((sin((lat0-lat1)/2)**2) 
                    + (cos(lat0)*cos(lat1)*sin((long0-long1)/2)**2)) 
                   ** 0.5))