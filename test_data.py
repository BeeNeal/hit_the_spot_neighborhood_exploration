from flask_sqlalchemy import SQLAlchemy
from model import *
db = SQLAlchemy()


def example_data():
    """Create some sample data in explorations DB."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Location.query.delete()

    # Add sample users and locations

    trinity = User(fname='Trinity', email='trin@unplugged.com',
                   username='questionit', password='l0lagent')
    neo = User(fname='Neo', email='theone@unplugged.com',
               username='neo', password='l0lagent')

    tacorea = Location(yelp_id='tacorea-san-francisco', name='Tacorea',
                       latitude='37.7749', longitude='122.3392',
                       address='809 Bush St, San Francisco, CA 94108',
                       yelp_url='tacorea@yelp.com', pic='pic')

    db.session.add_all([trinity, neo, tacorea])
    db.session.commit()
