
"""Hit the Spot Neighborhood Exploration server"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import *

from yelp_request import search
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
    address = request.form.get('address')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    url = request.form.get('url')
    pic = request.form.get('pic')

    print "Made it to add-to-list"
    return jsonify({'status': status})
    # add adding to DB func and logic checks here
    
    # Can I separate fetching data from adding to DB? (sep add to DB func)


@app.route('/registration')
def display_registration_form():
    """displays registration form"""

    return render_template('registration_form.html')


@app.route('/register', methods=['POST'])
def register():
    """Add user info to DB"""

    pass


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