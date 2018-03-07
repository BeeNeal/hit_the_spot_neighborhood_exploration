
"""Hit the Spot Neighborhood Exploration server"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import *
from db_helpers import *
from processing_functions import *
from maps import *
from yelp_req_trial import search, search_parks, search_by_coordinates
import sys
import os


API_KEY = os.environ['API_KEY']
api_key = API_KEY

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Display Homepage."""

    # if session['user_id']:
    #     return redirect('/explore')
    # else:
    return render_template("homepage.html")


@app.route('/questions')
def display_questions():
    """Display modal carousel of search term questions."""

    return render_template('question_modals.html')


@app.route('/questions', methods=['POST'])
def process_questions():
    """Update user table in DB with user answers to search term questions"""

    user_id = session.get('user_id')
    cuisine = request.form.get('cuisine')
    hobby = request.form.get('hobby')
    outdoorsy = request.form.get('outdoorsy')
    if user_id:
        add_answers_data(user_id, cuisine, hobby, outdoorsy)

    return jsonify({'answer': True})

    return redirect('/explore')


@app.route('/explore')
def search_by_address():
    """Get user input address, display locations for exploration."""

    if not User.query.get(session['user_id']).cuisine:
        return redirect('/questions')
    # if user is logged in, grab their main address off of their profile
    if session.get('user_id'):
        user_id = session['user_id']
        address = session['address']
        cuisine = User.query.get(session['user_id']).cuisine
        if session.get('address2'):
            address = session['address2']
        if request.args.get('address'):
            address = request.args.get('address')
            session['address2'] = address

        places = search(api_key, cuisine, address)
        if User.query.get(session['user_id']).outdoorsy is True:
            places2 = search_parks(api_key, address)  # FIXME - change to gardens
        else:
            places2 = search(api_key, 'cafe', address)

        places3 = search(api_key, 'hobby', address)
        locations_to_show = combine_location_dictionaries(places, places2,
                                                          places3, user_id)

        name = User.query.get(session['user_id']).fname

    else:
        address = request.args.get('address')
        locations_to_show = create_exploration_list(generate_exploration_data(address))
        name = 'there'

    return render_template("explore.html", places=locations_to_show,
                           name=name, address=address)



@app.route('/add-to-list', methods=['POST'])
def add_to_list():
    """Adds user selected POI to locations table in DB"""

    status = request.form.get('status')
    yelp_id = request.form.get('yelp_id')
    name = request.form.get('name')
    address = request.form.get('address')
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    url = request.form.get('url')
    pic = request.form.get('pic')

    # Check to see not already in locations table
    location = Location.query.get(yelp_id)

    # Check to see if in UserLocations table (make this a function when need to use again)
    user_location = (UserLocation.query
                     .filter(UserLocation.user_id == session['user_id'],
                             UserLocation.yelp_id == yelp_id).first())

    # if not already in locations table, add business to locations table
    if not location:
        add_business_to_Locations(yelp_id, name, latitude, longitude, address,
                                  url, pic)

    # if not already in Userlocation, add to userLocation table
    if not user_location:
        add_business_to_UserLocation(session['user_id'], yelp_id, status)

    if status == 'visited':
        change_to_visited(session['user_id'], yelp_id)

    if status == 'interested':
        change_to_interested(session['user_id'], yelp_id)

    # return status to AJAX to change button text based on status
    return jsonify({'status': status})


@app.route('/registration')
def display_registration_form():
    """displays registration form"""

    return render_template('registration_form.html')


@app.route('/register', methods=['POST'])
def register():
    """Add user info to DB"""

    fname = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')
    address_name = request.form.get('address_name')

    full_address = address + ", " + city + ", " + state + " " + zipcode
    coordinates = geocode(full_address)
    lon, lat = coordinates

    # Does user already exist in DB?
    current_username = User.query.filter_by(username=username).first()
    current_email = User.query.filter_by(email=email).first()

    if current_username or current_email:
        flash('user already exists! Please log in')
        return redirect('/registration')

        # If user doesn't already exist, register user by adding info to DB
    elif not current_username and not current_email:
        if password1 == password2:
            password = password1
            new_user = add_user_to_User(fname, username, email, password)
            add_address(new_user.user_id, address, city, state, zipcode, fname, 
                        lat, lon)

            # log the user in
            user = User.query.filter(User.email == email).first()
            login_user(user)
            return redirect('/questions')
        else:
            flash("Passwords don't match - please try again.")
            return redirect('/registration')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    user_info = request.form.get("user_info")
    password = request.form.get("password")

    user = User.query.filter((User.email == user_info) | (User.username ==
                                                          user_info)).first()
    if not user:
        return jsonify({'status': 'noUser'})
    elif user.password != password:
        return jsonify({'status': 'wrongPassword'})
    else:
        address_lon_lat = login_user(user)

    if user.cuisine:
        return jsonify({'status': 'success', 'lon_lat': address_lon_lat,
                        'answer': True})
    else:
        return jsonify({'status': 'success', 'lon_lat': address_lon_lat,
                        'answer': False})

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    del session['address']
    # session.clear()
    flash("Logged Out.")
    return redirect("/")


@app.route('/destinations')
def display_destinations():
    """Displays UserLocations - locations that user is interested in visiting"""

    user_id = session['user_id']
    destinations = destinations_list(user_id)
    geocoded_address = user_lon_lat(user_id)
    map_json = destination_lon_lats(user_id)
    if destinations:
        return render_template('destinations.html',
                               addressLonLat=geocoded_address,
                               places=destinations, map_json=map_json)
    else:
        flash("Where do you want to explore?")
        return redirect('/')


@app.route('/visited')
def display_places_visited():
    """Displays locations that user has visited"""

    user_id = session.get('user_id')
    places_visited = visited_list(user_id)
    geocoded_address = user_lon_lat(user_id)
    if places_visited:
        map_json = destination_lon_lats(user_id)
        return render_template('visited.html', places=places_visited,
                               addressLonLat=geocoded_address,
                               map_json=map_json)
    else:
        flash("Visited any of these places yet?")
        return redirect('/destinations')


@app.route('/add-notes', methods=['POST'])
def add_notes_to_DB():
    """Adds user notes to specific user locations in DB"""

    yelp_id = request.form.get('yelp_id')
    notes = request.form.get('notes')
    favorite = request.form.get('favorite')
    # rating = request.form.get('rating')
    user_id = session['user_id']
    #using default rating of 5 for now - change when add rating functionality
    add_notes(user_id, yelp_id, notes, favorite, 5)
    change_to_visited(user_id, yelp_id)
    
    return jsonify({'status': 'added'})
    # HERE need to change interested to visited (in prep for when it's coming from
        #explored list, change interested to null after check and change visited to True
        # should build a function in DB helpers)

@app.route('/meetup')
def display_meetup_spots():
    """display meetup spot page"""

    return render_template('meetup.html')


@app.route('/meetup', methods=['POST'])
def generate_meetup_spots():
    """generate midpoint locations, and display on map"""

    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    search_term = request.form.get('venue')
    if not search_term:
        search_term = ""

    a1_coordinates = geocode(address1)
    a2_coordinates = geocode(address2)
    map_center = meetup_root(address1, address2)
    lon, lat = map_center
    places_from_yelp = search_by_coordinates(api_key, lat, lon, search_term)
    places = create_meetup_list(places_from_yelp)

    return render_template('meetup_locations.html', places=places,
                           longitude=lon, latitude=lat, address1=address1,
                           address2=address2, a1_coordinates=a1_coordinates,
                           a2_coordinates=a2_coordinates, map_center=map_center)

# @app.route('/test', methods=['GET'])
# def display_carousel():
#     """caurousel form test"""

#     return render_template('carousel_form_IMPLEMENT_TO_EXPLORE.html')

if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

# my understanding of if name = main: when file is imported, only these things underneath run
# as opposed to the typical everything being run


# IDEA: Ask a few Qs at the beginning, and then make specific queries based on answers
# eg: Coffee drinker? More often go places to meet friends or make them? favorite cuisine?