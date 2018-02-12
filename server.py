
"""Hit the Spot Neighborhood Exploration server"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import *
from db_helpers import *

from yelp_req_trial import search
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

    return render_template("homepage.html")


@app.route('/get_address', methods=['POST'])
def search_by_address():
    """Get user input address."""

    address = request.form.get('address')
    places = search(api_key, 'dinner', address)

    amt_displayed = len(places['businesses'])

    return render_template("starting_places.html", address=address,
                                                   places=places,
                                                   amt_displayed=amt_displayed)


@app.route('/add-to-list', methods=['POST'])
def add_to_list():
    """Adds user selected POI to DB"""

    status = request.form.get('status')
    yelp_id = request.form.get('yelp_id')
    name = request.form.get('name')
    address = request.form.get('address')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    url = request.form.get('url')
    pic = request.form.get('pic')

    # Check to see not already in locations table
    location = Location.query.get(yelp_id)
    # add business to locations table
    if not location:
        add_business_to_Locations(yelp_id, name, latitude, longitude, address,
                                  url, pic)

    else:
    # Check to see if in UserLocations table
        user_location = (UserLocation.query
                         .filter(UserLocation.user_id == session[user_id],
                                 UserLocation.yelp_id == yelp_id).first())

        if not user_location:
            add_business_to_UserLocation

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

    # will add this to addresses table
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')

    if password1 == password2:
        password = password1
    else:
        flash("Passwords don't match - please try again.")

    # Does user already exist in DB?
    current_username = User.query.filter_by(username=username).first()
    current_email = User.query.filter_by(email=email).first()
    print current_username
    print current_email

    if not current_username and not current_email:
        new_user = add_user_to_User(fname, username, email, password)
        print new_user

  # at this point, does user have an id yet?

    add_start_address(new_user.user_id, address, city, state, zipcode)


@app.route('/destinations')
def display_destinations():
    """Displays UserLocations - locations that user is interested in visiting"""

    return render_template('destinations.html')


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