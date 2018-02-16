from db_helpers import *


def combine_location_dictionaries(places, parks, user_id):
    """Takes in yelp API data, passes this data to add_API_search_data_to_dict,

     combines resulting dicts """

    locations_dict = add_API_search_data_to_dict(places, user_id)
    locations_dict.update(add_API_search_data_to_dict(parks, user_id))

    return locations_dict


def add_API_search_data_to_dict(api_results, user_id):
    """Adds yelp API search results to dict - adding only the relevant data"""

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