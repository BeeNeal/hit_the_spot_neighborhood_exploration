import requests
import os
import json
from urllib import quote

api_key = os.environ['API_KEY']

# r = requests.get('https://api.yelp.com/v3/businesses/matches/lookup')

# GET https://api.yelp.com/v3/businesses/matches/best

API_KEY = os.environ['API_KEY']


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.

# test location: 683 Sutter st., 
DEFAULT_TERM = 'bar'
DEFAULT_LOCATION = '683 Sutter st San Francisco, CA'
SEARCH_LIMIT = 3

def request(host, path, api_key, url_params=None):
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
        'price': '1'
    }

    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


# search_results = search(api_key, DEFAULT_TERM, DEFAULT_LOCATION)
# print search(api_key, 'Philz', DEFAULT_LOCATION)

places = search(api_key, 'dinner', DEFAULT_LOCATION)

# places_dict = json.loads(places)
# print places_dict


# Want to make as few queries to Yelp API as possible for efficiency - better to ask
# yelp once, and then divvy up the data as needed.
first_bus = places['businesses'][0]['name']

# current prob - 