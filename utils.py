from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim, Photon


def haversine(coord1: float, coord2: float) -> float:
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [coord1[1], coord1[0], coord2[1], coord2[0]])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of Earth in kilometers
    return c * r


def find_central_point(gps_points: list[tuple[float, float]]) -> tuple[float, float]:
    lat = sum(point[0] for point in gps_points) / len(gps_points)
    lon = sum(point[1] for point in gps_points) / len(gps_points)
    return lat, lon


def get_city_name(latitude, longitude):
    geolocator = Nominatim(user_agent="measurements")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    city = address.get('city', '')
    return city
