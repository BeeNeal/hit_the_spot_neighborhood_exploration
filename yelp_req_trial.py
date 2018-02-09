import requests
import os
import json
from urllib import quote
from model import *
from flask_sqlalchemy import SQLAlchemy


from flask import Flask
app = Flask(__name__)
connect_to_db(app)

api_key = os.environ['API_KEY']

# r = requests.get('https://api.yelp.com/v3/businesses/matches/lookup')

# GET https://api.yelp.com/v3/businesses/matches/best

API_KEY = os.environ['API_KEY']


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

DEFAULT_TERM = 'dinner'
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

# Don't want to add all of these - only want to add places user has marked <- can change
# this if later down the line it seems too slow
# for i in range((len(places) - 1)):
#     for bus in places:
#         yelp_id, name, lat, lon, url = places['businesses'][0]['name']

# upon event click, call this function - does that mean I have to write it in JS?

# problem - can I get many values from dict all at once without a loop?

# already displaying the name

# impending problem - add event listener and fetch data for that specific business- 
# rn they're giving a LIST for the businesses, and so accessing the data by index, but
# can't select specific data to snatch that way. 

name = places['businesses'][0]['name']
url = places['businesses'][0]['url']
lat = float(places['businesses'][0]['coordinates']['latitude'])
lon = float(places['businesses'][0]['coordinates']['longitude'])
yelp_id = places['businesses'][0]['id']
pic = places['businesses'][0]['image_url']

# first_place = Location(yelp_id='yelp_id', name='name', latitude=lat,
#                        longitude=lon, yelp_url='url')

first_place = Location(yelp_id=yelp_id, name=name, latitude=lat, longitude=lon,
                       yelp_url=url, pic=pic)


db.session.add(first_place)
db.session.commit()

# When user clicks button to store to DB
# have the name of the business, and want to directly store that business

place = Location(yelp_id=yelp_id, name=name, latitude=lat, longitude=lon,
                       yelp_url=url, pic=pic)

for place in places['businesses']:
    if place[i]['name'] == business_name:
        


# if __name__ == '__main__':
