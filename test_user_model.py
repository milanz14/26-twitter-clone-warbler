"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """ clean up existing users """
        User.query.delete()
        u1 = User.signup(username='user1', email='test@email.com', password="password", image_url=None)
        u2 = User.signup(username='user2', email='test1@email.com', password="password", image_url=None)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.user1 = u1
        self.user1_id = u1.id
        self.user2 = u2
        self.user2_id = u2.id


    def tearDown(self):
        """ roll back any fouled transactions """
        db.session.rollback();

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_followers_working(self):
        """ does is following successfully detect when user1 is following user2 or VV. """
        self.user1.following.append(self.user2)
        db.session.commit()
        self.assertEqual(len(self.user2.following),0)
        self.assertEqual(len(self.user2.followers),1)
        self.assertEqual(len(self.user1.followers),0)
        self.assertEqual(len(self.user1.following),1)

    def test_is_following_working(self):
        """ test if u2 following u1 works or not following etc """
        self.user1.following.append(self.user2)
        db.session.commit()
        self.assertFalse(self.user2.is_following(self.user1))
        self.assertTrue(self.user1.is_following(self.user2))

    def test_user_create(self):
        """ check if creation of user works """
        pass

    def test_authentication_works(self):
        """ test that the authentication works proper """
        user = User.authenticate(username=self.user1.username, password="password")
        self.assertIsNotNone(user)
        self.assertEqual(user.id,self.user1_id)
    
    def test_wrong_username(self):
        """ test that a wrong username doesn't return valid user """
        user = User.authenticate(username="wronguser", password="password")
        self.assertFalse(user)
    
    def test_wrong_password(self):
        """ test that a user isn't logged in if a wrong password is provided """
        user = User.authenticate(username=self.user1.username, password="wrongpassword")
        self.assertFalse(user)
        
