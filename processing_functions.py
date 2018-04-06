import os
import sys

from db_helpers import *
from yelp_req_trial import search, search_parks

from flask import session

API_KEY = os.environ['API_KEY']
api_key = API_KEY

def login_user(user):
    """Logs user in"""

    user_address = Address.query.filter(Address.user_id == user.user_id)

    session["user_id"] = user.user_id
    session["address"] = user_address.first().address + " " + user_address.first().zipcode
    address_lon_lat = user_lon_lat(user.user_id)

    return address_lon_lat

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
    """Take in json of API results, return dictionary with these results"""

    locations_to_show = {}
    if api_results:
        for result in api_results:
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


def combine_location_dictionaries(places, places2, places3, user_id):
    """Takes in yelp API data, passes this data to function that combines resulting dicts """

    locations_dict = add_API_search_data_to_dict(places, user_id)
    locations_dict.update(add_API_search_data_to_dict(places2, user_id))
    locations_dict.update(add_API_search_data_to_dict(places3, user_id))

    return locations_dict


def add_API_search_data_to_dict(api_results, user_id):
    """Adds yelp API search results to dict - adding only the relevant data"""

# could make dict with above funct, and then del keys based on if in their list

    locations_to_show = {}

    all_user_locations = user_locations_list(user_id)
    user_locations = [place.yelp_id for place in all_user_locations]

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


def create_meetup_list(api_results):
    """Take in json of API results, return dictionary with these results"""

    meetup_spots = {}
    for i in range(len(api_results['businesses'])):
        poi = api_results['businesses'][i]['id']

# Separate API calls, so there could be overlap in businesses, and we don't
# want to show same place twice
        if poi not in meetup_spots:
            meetup_spots[poi] = {}
            meetup_spots[poi]['yelp_id'] = poi
            meetup_spots[poi]['name'] = api_results['businesses'][i]['name']
            meetup_spots[poi]['address'] = " ".join(api_results['businesses'][i]['location']['display_address'])
            meetup_spots[poi]['latitude'] = api_results['businesses'][i]['coordinates']['latitude']
            meetup_spots[poi]['longitude'] = api_results['businesses'][i]['coordinates']['longitude']
            meetup_spots[poi]['url'] = api_results['businesses'][i]['url']
            meetup_spots[poi]['pic'] = api_results['businesses'][i]['image_url']

    return meetup_spots


def check_if_enough_locations(lat, lon, term):
    """Checks to ensure enough places were generated from Yelp call"""

    # if not enough locations were generated, expand search radius
    places = search_by_coordinates(api_key, lat, lon, term, 450)
    if len(places) < 10:
        places = search_by_coordinates(api_key, lat, lon, term, 750)
    return places


def get_locations_to_show(lat, lon, user_id, cuisine, hangout, outdoorsy):
    """Take in user info, return dict of locations"""

    places = check_if_enough_locations(lat, lon, cuisine)
    places2 = check_if_enough_locations(lat, lon, hangout)
    places3 = return_parks_or_cafe(lat, lon, outdoorsy)

    return combine_location_dictionaries(places, places2, places3, user_id)


def return_parks_or_cafe(lat, lon, outdoorsy):
    """If outdoorsy is True/no pref, return parks otherwise, return cafes"""

    if outdoorsy_response is True:
            places = check_if_enough_locations(lat, lon, 'park')
    else:
        places = check_if_enough_locations(lat, lon, 'cafe')

    return places
