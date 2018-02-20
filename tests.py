from unittest import TestCase
from model import connect_to_db, db, example_data
# from test_data import example_data
from server import app
from flask import session


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

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/login',
                            data={'user_info': 'trin@unplugged.com',
                                  'password': 'l0lagent'},
                            follow_redirects=True
                            )
            self.assertEqual(session.get('user_id'), 1)
            self.assertIn("success", result.data)


    def test_wrong_password(self):
        """Test log in form with incorrect password"""

        with self.client as c:
            result = c.post('/login',
                            data={'user_info': 'trin@unplugged.com',
                                  'password': 'wrongpassword'},
                            follow_redirects=True
                            )
            self.assertEqual(session.get('user_id'), None)
            self.assertIn("wrongPassword", result.data)

    def test_no_user(self):
        """Test log in form where no username/email for that user"""

        with self.client as c:
            result = c.post('/login',
                            data={'user_info': 'morpheus@unplugged.com',
                                  'password': 'l0lagent'},
                            follow_redirects=True
                            )
            self.assertEqual(session.get('user_id'), None)
            self.assertIn("noUser", result.data)



class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

    def test_logout(self):
            """Test logout."""

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = 1

                result = self.client.get('/logout', follow_redirects=True)

                self.assertNotIn('user_id', sess)
                self.assertIn('Logged Out', result.data)



    # def test_logout(self):
    #     """Test logout route."""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess['user_id'] = '1'

    #         result = self.client.get('/logout', follow_redirects=True)

    #         self.assertNotIn('user_id', session)
    #         self.assertIn('Logged Out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
