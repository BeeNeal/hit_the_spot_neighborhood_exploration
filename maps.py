import geocoder
from mapbox import Geocoder
import requests
from urllib import quote

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

    # swap lat/lon to lon/lat to accommodate mapbox

    lat, lon = coordinates
    lon_lat = [lon, lat]

    return lon_lat

    # [37.789745, -122.4105791] (from python)

    # 37.789806 | -122.410709 (from yelp)

    # [-122.42313, 37.788517] (from mapbox)

# Meetup spot
def meetup_root(address1, address2):
    """Avg latitudes and longitudes to produce coordinates of meetup spot"""

    address1 = geocode(address1)
    address2 = geocode(address2)

    # save average lons/lats as list to pass to map and yelp api call
    meetup_coordinates = [((c1 + c2)/2) for c1, c2 in zip(address1, address2)]

    return meetup_coordinates
