# Instructor Qs:
#1) infinite char string type? (needed for notes)

# Personal Qs:
# Look into yelp API and see if good idea to put yelp ID as PK id for Location
# Different name than list?
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User Model."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    location = db.relationship("Location", backref=db.backref('user'))


    def __repr__(self):
        """Provide representation when User object is printed."""

        return "<User username={} email={}>".format(self.username,
                                                    self.email)


class UserLocation(db.Model):
    """different locations users may have saved, eg: home and work Addresses"""

    __tablename__ = 'user_locations'

    ul_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey=('User.user_id'))
    loc_id = db.Column(db.Integer, ForeignKey=('Location.yelp_id'))
    notes = db.Column(db.String(250))
    rating = db.Column(db.Integer, nullable=True)


# Locations will be stored after searched and interacted with by user
class Location(db.Model):
    """Location Model."""

    __tablename__ = 'locations'

    yelp_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    yelp_url = db.Column(db.String(250))


class UserLocationCategory(db.Model):
    """Association table between User-locations and user categories"""

    __tablename__ = 'user_location_categories'

    ulc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ul_id = db.Column(db.Integer, ForeignKey='UserLocation.ul_id')
    cat_id = db.Column(db.Integer, ForeignKey='Category.cat_id')


class Category(db.Model):
    """Pre-set Categories such as 'good for date'

    one-to-many relationship with CatLocs
    """

    __tablename__ = 'categories'

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
        # name = entries in table: has_gone, want_to_go, good_for_date, etc.


class List(db.Model):
    """user generated categories eg: 'good for dinner with Louisa' """

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey=('User.user_id'))


class ListLocation(db.Model):
    """Association table for List and Location. """

    __tablename__ = 'list_locations'

    l_loc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, ForeignKey=('List.list_id'))
    loc_id = db.Column(db.Integer, ForeignKey=('Location.yelp_id'))


# Helper Functions Below
def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///explorations'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
