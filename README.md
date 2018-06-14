# Hit the Spot! A neighborhood exploration app

Try out all the best spots in your neighborhood with Hit the Spot! This app provides inspiration to get you to visit that cute little cafe down the street, or the art gallery you always pass by on your daily commute. Need help choosing a place to meet a friend at a location convenient for both of you? A handy meetup feature has you covered.

![homepage](https://github.com/BeeNeal/hit_the_spot_neighborhood_exploration/blob/master/static/homepage.png)

## Technology stack

Backend: Python, Flask, PostgreSQL, SQLAlchemy

Frontend: JavaScript, jQuery, Jinja, AJAX, HTML, CSS, Bootstrap

APIs: Yelp, Mapbox

## Overview

Once the user arrives at Hit the Spot! they can enter an address, and have a list of highly rated  locations in a 1.5mi radius suggested to them. They can also access the meetup feature. The other features include saving destinations, and writing notes about visited locations require the user to register and login. The exploration list for the users that are logged in is tailored to the user, using the answers they've provided to some brief questions as the basis of the location list generation.

![question 3](https://github.com/BeeNeal/hit_the_spot_neighborhood_exploration/blob/master/static/outdoorsy.png)

## Visited Locations

Once the user has visited a location, they have a convenient location to record notes
about the place. They also have the option to 'star' it, which acts as a bookmarking
function.

![Visited Locations](https://github.com/BeeNeal/hit_the_spot_neighborhood_exploration/blob/master/static/visited_page.png)

## Meetup Spot

The user can input two addresses, and a list of suggested locations will be generated around the midpoint of these two addresses.The map displays markers for the two inputted addresses, the midpoint, and the suggested locations.

![Meetup page](https://github.com/BeeNeal/hit_the_spot_neighborhood_exploration/blob/master/static/meetup.png)


## Setup

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

-- Get your own secret key for the Yelp API and add to a file titled secrets.sh

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

Brittany Neal is a software engineer based out of Oakland, CA. 
Learn more about her here: https://www.linkedin.com/in/brittanyneal22/
