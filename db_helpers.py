from model import *

def add_business_to_Locations(yelp_id, name, lat, lon, address, url, pic):
    """Adds business to Location class"""

    business = Location(yelp_id=yelp_id, name=name, latitude=lat, longitude=lon,
                        address=address, yelp_url=url, pic=pic)

    db.session.add(business)
    db.session.commit()


def add_business_to_UserLocation(user_id, yelp_id, status, notes=None,
                                 rating=None, favorite=None):
    """Adds business to UserLocation"""

    # Need to add reg/login to create user before can add to UserLoc - or could just hardcode
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

def destinations_list(user_id, status):
    """Queries DB to produce list of destinations"""

    destinations = UserLocation.query.filter(UserLocation.user_id == user_id,
                   UserLocation.interested == True).all()
