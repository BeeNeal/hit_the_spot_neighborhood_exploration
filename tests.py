from unittest import TestCase
from model import connect_to_db, db
from test_data import example_data
from server import app
from flask import session

# def init_app():
#     # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
#     from flask import Flask
#     app = Flask(__name__)

#     connect_to_db(app)
#     print "Connected to DB."


# def connect_to_db(app):
#     """Connect the database to our Flask app."""

#     # Configure to use our database.
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
#     app.config['SQLALCHEMY_ECHO'] = False
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("want to explore?", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'trin@unplugged.com',
                                  'password': 'l0lagent'},
                            follow_redirects=True
                            )
            self.assertEqual(session['user_id'], 1)
            self.assertIn("Welcome back!", result.data)


    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('Logged Out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
