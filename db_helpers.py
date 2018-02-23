from model import *
from yelp_req_trial import search, search_parks

def add_business_to_Locations(yelp_id, name, lat, lon, address, url, pic):
    """Adds business to Location class"""

    business = Location(yelp_id=yelp_id, name=name, latitude=lat, longitude=lon,
                        address=address, yelp_url=url, pic=pic)

    db.session.add(business)
    db.session.commit()


def add_business_to_UserLocation(user_id, yelp_id, status, notes=None,
                                 rating=None, favorite=None):
    """Adds business to UserLocation"""

    user_location = UserLocation(user_id=user_id, yelp_id=yelp_id)

    # updates "visited"/"interested" based on user button 
    if status == "visited":
        user_location.visited = True
    elif status == "interested":
        user_location.interested = True

    db.session.add(user_location)
    db.session.commit()


def add_user_to_User(fname, username, email, password):
    """Adds user to User table based on registration info"""

    user = User(fname=fname, username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return user


def add_address(user_id, address, city, state, zipcode, name):
    """Adds address to addresses table. """

    start_address = Address(user_id=user_id, address=address, city=city,
                            state=state, zipcode=zipcode, name=name)
    db.session.add(start_address)
    db.session.commit()


def destinations_list(user_id):
    """Queries DB to produce destinations for that user_id"""

    destinations = UserLocation.query.filter(UserLocation.user_id == user_id,
               UserLocation.interested == True).all()

    return destinations


def visited_list(user_id):
    """Queries DB to provide places that user_id has marked as visited"""

    visited_places = UserLocation.query.filter(UserLocation.user_id == user_id,
               UserLocation.visited == True).all()

    return visited_places


def user_locations_list(user_id):
    """Provides all locations saved to locations table for that user"""

    return UserLocation.query.filter(UserLocation.user_id == user_id).all()


def get_user_location_by_yelp_and_user_ids(user_id, yelp_id):
    """Queries DB with yelp_id and user_id to return user location"""

    user_location = UserLocation.query.filter(UserLocation.user_id == user_id,
                                              UserLocation.yelp_id == yelp_id).first()

    return user_location


def add_notes(user_id, yelp_id, notes, favorite, rating):
    """Adds user notes/favorite/rating to specific user_location"""

    user_location = get_user_location_by_yelp_and_user_ids(user_id, yelp_id)
    user_location.notes = notes
    user_location.favorite = favorite
    user_location.rating = rating

    db.session.commit()


def change_to_visited(user_id, yelp_id):
    """Change userLocation location status to visited"""

    user_location = get_user_location_by_yelp_and_user_ids(user_id, yelp_id)

    user_location.visited = True
    user_location.interested = False

    db.session.commit()


def destination_lon_lats(user_id):
    """take in destinations and return all lon/lats"""

    # Get all userLocations objects for user destinations
    destinations = destinations_list(user_id)

    # Location objects for user destinations (will use if want to add info
    # to markers)

    # destination_location_objs = [place.location for place in destinations]
    #     return destination_location_objs

    # provide all lon/lats in list
    destination_lon_lats = []
    for item in destinations:
        destination_lon_lats.append([item.location.longitude,
                                     item.location.latitude])

    return destination_lon_lats
# [[place.location.longitude, place.location.latitude]
# for place in destinations]


def visited_lon_lats(user_id):
    """take in visited locations and return all lon/lats"""

    # Get all userLocations objects for user visited places
    visited = visited_list(user_id)

    # provide all lon/lats in list
    visited_lon_lats = []
    for place in visited:
        visited_lon_lats.append([place.location.longitude,
                                 place.location.latitude])

    return visited_lon_lats
