import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.drop_all()
db.create_all()

class MessageModelTestCase(TestCase):
    """ Test views for messages model """

    def setUp(self):
        """ clean up existing users and create a dummy user for testing """
        User.query.delete()
        user1 = User.signup(username="user1", email="test@email.com", password="password", image_url=None)
        db.session.add(user1)
        db.session.commit()
        self.user1 = user1
        self.user1_id = user1.id

    def tearDown(self):
        """ clean up any fouled transactions """
        db.session.rollback()

    def test_message_model(self):
        """ does the message model work """
        message = Message(text="this is a message", user_id=self.user1_id,timestamp=None)
        db.session.add(message)
        db.session.commit()

        self.assertEqual(len(self.user1.messages),1)
    