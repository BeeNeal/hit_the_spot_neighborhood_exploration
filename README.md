# Hit the Spot! A neighborhood exploration app

![homepage image](https://github.com/BeeNeal/hit_the_spot_neighborhood_exploration/blob/master/static/homepage.png)

Try out all the best spots in your neighborhood with Hit the Spot! This app provides inspiration to get you to visit that cute little cafe down the street, or the art gallery you always pass by on your daily commute. Need help choosing a place to meet a friend at a location convenient for both of you? A handy meetup feature has you covered.

# Technology stack

Backend: Python, Flask, PostgreSQL, SQLAlchemy

Frontend: JavaScript, jQuery, Jinja, AJAX, HTML, CSS, Bootstrap

APIs: Yelp, Mapbox

# Overview

Once the user arrives at Hit the Spot! they can enter an address, and have a list of 

# Setup

-- Clone or fork this repo.

-- Create a virtual environment in your local directory:

```sh
$ virtualenv env
$ source env/bin/activate
```
-- Install requirements.txt:

```sh
$ pip install -r requirements.txt
```

-- Get your own secret key for Yelp and add to a file titled secrets.sh

-- Create the database

```sh
$ createdb explorations
$ python -i model.py

>>> db.create_all() 
```

-- Run the app:

```sh
$ python server.py
```

-- Navigate to localhost:5000 in your browser, create an account, and get started!


# Author

Brittany is a software engineer based out of Oakland, CA. 
Learn more about her here: https://www.linkedin.com/in/brittanyneal22/
