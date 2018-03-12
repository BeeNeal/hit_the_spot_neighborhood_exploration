import geocoder
from mapbox import Geocoder
import requests
from math import cos, asin, sqrt, sin, atan2, radians
from urllib import quote
from time import sleep


ACCESS_TOKEN = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ'

def string_url_formatter(string):
    """Takes in string, returns string with spaces replaced by '%20' """

    formatted = string.replace(" ", '%20')
    c_formatted = formatted.replace(",", '%2')

    return c_formatted + '.json'


def mapbox_geocode(address):
    """Send a GET request to mapbox API which returns geocoded address."""

    host_path = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
    search_address = string_url_formatter(address)
    credentials_path = '?access_token=' + ACCESS_TOKEN
    url = host_path + search_address + credentials_path
    response = requests.request('GET', url)

    return response.json()['features'][0]['geometry']['coordinates']


def geocode(address):
    """Uses python geocoder to geocode"""

    # google geocoder returns latitude, longitude as list
    coordinates = geocoder.google(address).latlng
    if not coordinates:
        sleep(1)
        lon_lat = mapbox_geocode(address)   # catch the error, sleep python
    else:
        lat, lon = coordinates
        lon_lat = [lon, lat]

    # swap lat/lon to lon/lat to accommodate mapbox
        # lat, lon = coordinates
        # lon_lat = [lon, lat]

    return lon_lat

# Meetup spot
def meetup_root(address1, address2):
    """Take in 2 address, return Avg latitudes and longitudes.

    Used to generate coordinates of meetup spot
    """

    address1 = geocode(address1)
    address2 = geocode(address2)

    # save average lons/lats as list to pass to map and yelp api call
    meetup_coordinates = [((c1 + c2)/2) for c1, c2 in zip(address1, address2)]

    return meetup_coordinates


def get_distance_between_2_coordinates(lat1, lon1, lat2, lon2):
    """Use haversine formula to calculate dist between two locations """
    # p = 0.017453292519943295     #Pi/180
    # a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 -
    #                                                 cos((lon2 - lon1) * p)) / 2
    # return 12742 * asin(sqrt(a))

    # approximate radius of earth in km
    R = 6373.0
    dlon = radians(lon2) - radians(lon1)
    dlat = radians(lat2) - radians(lat1)

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000

    return distance


def check_meetup_distance(haversine_distance):
    """Checks distance b/w meetup addresses to scale location generation rad"""

    # about 1600 meters to 1 mile

    # if 200 mi or greater apart, search radius is yelp API max (25 mi)
    if haversine_distance >= 320000:
        search_radius = 40000
    elif haversine_distance <= 6400:
        search_radius = 450
    # elif haversine_distance <= 16000
    else:
        search_radius = haversine_distance/6

    return int(search_radius)


def get_search_radius(lat1, lon1, lat2, lon2):
    """Take in 2 addresses' coordinates, return search radius value in meters"""

    haversine_dist = get_distance_between_2_coordinates(lat1, lon1, lat2, lon2)
    search_radius = check_meetup_distance(haversine_dist)

    return search_radius
