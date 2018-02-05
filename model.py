class User(db.Model):
    """User Model."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))


class User_Location(db.Model):
    """different locations users may have saved, eg: home and work Addresses"""

    __tablename__ = 'user_locations'

    uloc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey=('User.user_id') 

# 
class Location(db.Model):
    """Location Model."""

    __tablename__ = 'locations'

    yelp_id = 
    name
    latitude
    longitude
    yelp_url

# 

class CategoryLocations(db.Model):
    """Association table between locations and user categories"""


class Category(db.Model):
    """Categories such as 'good for date', and user choice such as 
    'good for dinner with Louisa' 

    one-to-many relationship with CatLocs
    """

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)