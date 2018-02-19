import os
import sys

from db_helpers import *
from yelp_req_trial import search, search_parks

API_KEY = os.environ['API_KEY']
api_key = API_KEY

def generate_exploration_data(address):
    """Create exploration location list"""

    # Makes call to yelp API to generate places
    cafes = search(api_key, 'cafe', address)
    dinners = search(api_key, 'dinner', address)
    parks = search_parks(api_key, address)

    # return a tuple that we will pass to create_exploration_list()
    return cafes, dinners, parks

# want to be able to take in any number of args
def create_exploration_list(api_results):
    """Take in tuple of API results, return dictionary with these results"""

    locations_to_show = {}

    for result in api_results:
        # print result['businesses']
        for i in range(len(result['businesses'])):
            poi = result['businesses'][i]['id']

    # Separate API calls, so there could be overlap in businesses, and we don't
    # want to show same place twice
            if poi not in locations_to_show:
                locations_to_show[poi] = {}
                locations_to_show[poi]['yelp_id'] = poi
                locations_to_show[poi]['name'] = result['businesses'][i]['name']
                locations_to_show[poi]['address'] = " ".join(result['businesses'][i]['location']['display_address'])
                locations_to_show[poi]['latitude'] = result['businesses'][i]['coordinates']['latitude']
                locations_to_show[poi]['longitude'] = result['businesses'][i]['coordinates']['longitude']
                locations_to_show[poi]['url'] = result['businesses'][i]['url']
                locations_to_show[poi]['pic'] = result['businesses'][i]['image_url']

    return locations_to_show


def combine_location_dictionaries(places, parks, user_id):
    """Takes in yelp API data, passes this data to function that combines resulting dicts """

    locations_dict = add_API_search_data_to_dict(places, user_id)
    locations_dict.update(add_API_search_data_to_dict(parks, user_id))

    return locations_dict


def add_API_search_data_to_dict(api_results, user_id):
    """Adds yelp API search results to dict - adding only the relevant data"""

# could make dict with above funct, and then del keys based on if in their list

    locations_to_show = {}

    x = user_locations_list(user_id)
    user_locations = [place.yelp_id for place in x]

    for i in range(len(api_results['businesses'])):
        poi = api_results['businesses'][i]['id']
        
        if poi not in user_locations:
            locations_to_show[poi] = {}
            locations_to_show[poi]['yelp_id'] = poi
            locations_to_show[poi]['name'] = api_results['businesses'][i]['name']
            locations_to_show[poi]['address'] = " ".join(api_results['businesses'][i]['location']['display_address'])
            locations_to_show[poi]['latitude'] = api_results['businesses'][i]['coordinates']['latitude']
            locations_to_show[poi]['longitude'] = api_results['businesses'][i]['coordinates']['longitude']
            locations_to_show[poi]['url'] = api_results['businesses'][i]['url']
            locations_to_show[poi]['pic'] = api_results['businesses'][i]['image_url']

    return locations_to_show