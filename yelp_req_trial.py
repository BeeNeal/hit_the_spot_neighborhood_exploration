import requests
import os
import json
from urllib import quote
from model import *
from flask_sqlalchemy import SQLAlchemy

API_KEY = os.environ['API_KEY']

api_key = API_KEY

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = '683 Sutter st San Francisco, CA'
SEARCH_LIMIT = 3


def request_call(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """

    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    # With these params, I take the highest rated, price $,
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'radius': 2415,
        'sort_by': 'rating',
        'price': '1',
    }

    return request_call(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def search_parks(api_key, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    # With these params, I take the highest rated, price $,
    url_params = {
        'term': 'park',
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'radius': 2415,
        'sort_by': 'rating',
        'categories': 'parks'
    }

    return request_call(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def search_by_coordinates(api_key, latitude, longitude, term=''):
    """Query the Search API by a search term and coordinates.

    Args:
        term (str): The search term passed to the API.
        latitude (float): The search latitude passed to the API.
        longitude(float): The search longitude passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': SEARCH_LIMIT,
        'radius': 2000,
        'sort_by': 'distance',
    }

    return request_call(API_HOST, SEARCH_PATH, api_key, url_params=url_params)
