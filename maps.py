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

    geocode = geocoder.google(address).latlng
    geocode_lnglat = []
    geocode_lnglat.append(geocode[1])
    geocode_lnglat.append(geocode[0])

    return geocode_lnglat
    
    # [37.789745, -122.4105791] (from python)

    # 37.789806 | -122.410709 (from yelp)

    # [-122.42313, 37.788517] (from mapbox)
