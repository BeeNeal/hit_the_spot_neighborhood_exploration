import geocoder
from mapbox import Geocoder
import requests
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
    lat, lon = coordinates
    lon_lat = [lon, lat]

    # swap lat/lon to lon/lat to accommodate mapbox
    if not coordinates:
        sleep(1)
        coordinates = geocoder.google(address).latlng   # catch the error, sleep python
        lat, lon = coordinates
        lon_lat = [lon, lat]

    return lon_lat

# Meetup spot
def meetup_root(address1, address2):
    """Take in 2 address, return Avg latitudes and longitudes.

    Used to generate coordinates of meetup spot
    """

    address1 = geocode(address1)
    print 'address 1 {}'.format(address1)
    address2 = geocode(address2)
    print address2

    # save average lons/lats as list to pass to map and yelp api call
    meetup_coordinates = [((c1 + c2)/2) for c1, c2 in zip(address1, address2)]

    print meetup_coordinates
    return meetup_coordinates
