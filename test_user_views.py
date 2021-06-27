from unittest import TestCase
from app import app
from models import db, Follows, Likes, User, Message

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///warbler-test'

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """ tests for user views """
    def setUp(self):
        """ clean up existing users and create a test user """
        User.query.delete()
        user1 = User.signup(username="user1", email="test@email.com", password="password", image_url=None)
        db.session.add(user1)
        db.session.commit()
        self.user1 = user1
        self.user1_id = user1.id
    
    def tearDown(self):
        """ clean up any fouled transactions """
        db.session.rollback()

    def test_homepage_anonymous(self):
        """ test the homepage """
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4>New to Warbler?</h4>', html)
    
    def test_homepage_loggedIn(self):
        """ test homepage when a user is logged in """
        with app.test_client() as client:
            pass

    