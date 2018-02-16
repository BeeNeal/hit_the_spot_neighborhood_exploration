
"""Hit the Spot Neighborhood Exploration server"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import *
from db_helpers import *
from processing_functions import *

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
@app.route('/explore', methods=['GET'])
def display_poi_options():
    """Displays POIs that users can add to their list of places to explore"""

    name = User.query.get(session['user_id'])
    address = name.address
    return render_template('starting_places.html', name=name.fname, address=address)


@app.route('/get_address', methods=['POST'])
def search_by_address():
    """Get user input address, display locations for exploration."""

    address = request.form.get('address')
    # these functions can be modified based on user answers of person they are
    places = search(api_key, 'dinner', address)
    parks = search_parks(api_key, address)

    locations_to_show = combine_location_dictionaries(places, parks, session['user_id'])
    print locations_to_show
    # if a user is logged in, this shouldn't matter anyway because will tie
    # to their main address on profile
    if session.get('user_id'):
        name = User.query.get(session['user_id']).fname
    else:
        name = 'there'

    return render_template("starting_places.html", places=locations_to_show,
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
            add_address(new_user.user_id, address, city, state, zipcode, fname)
            return redirect('/login')
        else:
            flash("Passwords don't match - please try again.")
            return redirect('/login')


@app.route('/login', methods=['GET'])
def login_form():
    """Display login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    user_info = request.form.get("user_info")
    password = request.form.get("password")

    user = User.query.filter((User.email == user_info) | (User.username == user_info)).first()

    if not user:
        flash("No user for this email or username found")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/")
    # Once created, make this redirect to user profile page which will have a link
    # to their destinations with a map of all the places they've been and link to
    # places they're interested in (first implementations of mapbox)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")
# Is there a better way to do the login than just a normal route/html


@app.route('/destinations')
def display_destinations():
    """Displays UserLocations - locations that user is interested in visiting"""

    destinations = destinations_list(session['user_id'])

    return render_template('destinations.html', places=destinations)


@app.route('/visited')
def display_places_visited():
    """Displays locations that user has visited"""

    places_visited = visited_list(session['user_id'])
    num_places = len(places_visited)
    if num_places:
        return render_template('visited.html', places=places_visited)
            # 'places_visited.html',
            #                    places=places_visited,
            #                    num_places=num_places)
    else:
        return render_template('visited.html', places=places_visited)    
    # else:
    #     flash("Visited any of these places yet?")
    #     return redirect('/destinations')


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