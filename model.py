# Instructor Qs:

# Can confirm my current tables are fine for new implementation of idea?
# Efficiency Q: better to make one huge call to yelp API, and parse data from

# Personal Qs:
# to-do rename Classes
# figure out EXACTLY what planning on doing. Make another user flow. Potentially 
#update model

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

    # don't need location relationship, b/c get through targetLocation
    # location = db.relationship("Location", backref=db.backref('user'))
    group = db.relationship("Group", backref=db.backref('user'))
    poi = db.relationship("UserLocation", backref=db.backref('user'))


    def __repr__(self):
        """Provide representation when User object is printed."""

        return "<User username={} email={}>".format(self.username,
                                                    self.email)



# Locations will be stored after searched and interacted with by user
class Location(db.Model):
    """Location Model."""

    __tablename__ = 'locations'

    yelp_id = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    yelp_url = db.Column(db.String(250))
    pic = db.Column(db.String(250))

    def __repr__(self):
        """Provide representation when Location object is printed."""

        return "<Location name={} ".format(self.name)


class UserLocation(db.Model):
    """info about different locations that users have saved"""

    __tablename__ = 'user_locations'

    user_loc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    yelp_id = db.Column(db.String(250), db.ForeignKey('locations.yelp_id'))
    visited = db.Column(db.Boolean)
    interesed = db.Column(db.Boolean)
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=True)
    favorite = db.Column(db.String(250))


class UserLocationCategory(db.Model):
    """Association table between user_locations and categories"""

    __tablename__ = 'user_loc_categories'

    user_loc_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_loc_id = db.Column(db.Integer, db.ForeignKey('user_locations.user_loc_id'))
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'))

    category = db.relationship('Category', backref=db.backref('user_loc_category'))
    place = db.relationship('UserLocation', backref=db.backref('user_loc_category'))

# MVP
class Category(db.Model):
    """Pre-set Categories such as 'good for date' """

    __tablename__ = 'categories'

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # name = entries in table: has_gone, want_to_go, good_for_date, etc.

    # Should has_gone and want_to_go be boolean?

# 2.0
class Group(db.Model):
    """User generated categories eg: 'good for dinner with Louisa' """

    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    group_loc = db.relationship('GroupLocation', backref=db.backref('group'))

# 2.0
class GroupLocation(db.Model):
    """Association table for Group and Location. """

    __tablename__ = 'group_locations'

    group_loc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    yelp_id = db.Column(db.String(250), db.ForeignKey('locations.yelp_id'))


#2.0
class Address(db.Model):
    """Different generation points saved by user, eg: home and work Addresses"""

    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)

    user = db.relationship("User", backref=db.backref('address'))


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
