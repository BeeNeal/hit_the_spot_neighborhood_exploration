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



        

# def add_status_to_dict(locations_to_show, user_id):
#     """adds if user has interacted with loc"""

#     # compare visited/interested values with queries about visited/interested,

#     destinations = set(destinations_list(user_id))
#     print locations_to_show
#     print type(locations_to_show)
    # for destination in destinations:
    #     locations_to_show[destination.yelp_id]['interested'] = True
    #     print locations_to_show[destination.yelp_id]['interested']

    # visited = set(visited_list(user_id))

    # update dict depending on visited/interested status
    # locations_to_show[poi]['visited'] = status
    # locations_to_show[poi]['interested'] = status

    # for item in destinations:
    #     if item.yelp_id == 

