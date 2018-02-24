
"""Hit the Spot Neighborhood Exploration server"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import *
from db_helpers import *
from processing_functions import *
from maps import geocode

from yelp_req_trial import search, search_parks
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


# this explore route is not yet operational - would need to make a call to the api again
# @app.route('/explore', methods=['GET'])
# def display_poi_options():
#     """Displays POIs that users can add to their list of places to explore"""

#     if session['user_id']:
#         name = User.query.get(session['user_id']).fname
#     else:
#         name = 'hi there'
#     address = name.address

#     return render_template('starting_places.html', name=name, address=address)


@app.route('/explore')  # , methods=['POST']
def search_by_address():
    """Get user input address, display locations for exploration."""

    # if user is logged in, grab their main address off of their profile
    if session.get('user_id'):
        user_id = session['user_id']
        address = session["address"]

        # FIXME need to refactor these API outs into the DB helpers
        places = search(api_key, 'dinner', address)
        parks = search_parks(api_key, address)

        locations_to_show = combine_location_dictionaries(places, parks, user_id)

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
    # In the ideal world, we won't be showing user places they've already checked off, but what do we
    # do if it's already in userLoc table? Just do normal response based on status as would already.

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
    lon, lat = geocode(full_address)

    # Does user already exist in DB?
    current_username = User.query.filter_by(username=username).first()
    current_email = User.query.filter_by(email=email).first()

    if current_username or current_email:
        flash('user already exists! Please log in')
        return redirect('/login')

    elif not current_username and not current_email:
        if password1 == password2:
            password = password1
            new_user = add_user_to_User(fname, username, email, password)
            add_address(new_user.user_id, address, city, state, zipcode, fname, lat, lon)
            return redirect('/login')
        else:
            flash("Passwords don't match - please try again.")
            return redirect('/login')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    user_info = request.form.get("user_info")
    password = request.form.get("password")

    user = User.query.filter((User.email == user_info) | (User.username ==
                                                          user_info)).first()
    if not user:
        # flash("No user for this email or username found")
        return jsonify({'status': 'noUser'})

    elif user.password != password:
        # flash("Incorrect password")
        return jsonify({'status': 'wrongPassword'})

    else:
    # make sure user has an address saved to profile, or this will break!
        user_address = Address.query.filter(Address.user_id == user.user_id)

        session["user_id"] = user.user_id
        session["address"] = user_address.first().address + " " + user_address.first().zipcode

        return jsonify({'status': 'success'})

    # return jsonify({'status': 'test'})
    # flash("Logged in")
    # return redirect("/")
    # Once created, make this redirect to user profile page which will have a link
    # to their destinations with a map of all the places they've been and link to
    # places they're interested in (first implementations of mapbox)


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
    # geocoded_address = geocode("2005 filbert st oakland ca")  # FIXME put in real address
    geocoded_address = [-122.42313, 37.788517]
    map_json = destination_lon_lats(user_id)

    return render_template('destinations.html', addressLngLat=geocoded_address,
                           places=destinations, map_json=map_json)


@app.route('/visited')
def display_places_visited():
    """Displays locations that user has visited"""

    user_id = session.get('user_id')
    places_visited = visited_list(user_id)
    if places_visited:
        map_json = destination_lon_lats(user_id)
        return render_template('visited.html', places=places_visited, 
                                addressLngLat=[-122.42313, 37.788517], 
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
    
    return "added notes"
    # HERE need to change interested to visited (in prep for when it's coming from
        #explored list, change interested to null after check and change visited to True
        # should build a function in DB helpers)

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

# my understanding of if name = main: when file is imported, only these things underneath run
# as opposed to the typical everything being run


# IDEA: Ask a few Qs at the beginning, and then make specific queries based on answers
# eg: Coffee drinker? More often go places to meet friends or make them? favorite cuisine?