
"""Hit the Spot Neighborhood Exploration server"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import *

from yelp_request import search
import sys
import os


API_KEY=os.environ['API_KEY']
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
    

    # need to JSONIFY (loads? dumps?)
    # Should I use an ajax call to display the data on the screen when they press "explore"
    # and then from there send the data to backend to store? 

    return render_template("starting_places.html", address=address, starting_places=places)


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