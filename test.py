import unittest

from app import create_app, db
from app.auth.models import User


class TestAuth(unittest.TestCase):
    def setUp(self):
        # Use a separate test configuration
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = self.app.test_client()
        self.db = db

        with self.app.app_context():
            # Create the test database tables
            self.db.create_all()

            # Create a test user
            self.create_test_user()

    def tearDown(self):
        # Remove the test database tables after the test is complete
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def create_test_user(self):
        # Create a test user for testing login
        user = User(username='johnsmith', name='John', phone='1234567890', email='test@example.com')
        user.set_password('12345678')
        self.db.session.add(user)
        self.db.session.commit()

    def make_login_request(self, username, password):
        # Helper method to make login requests with varying data
        data = {'username': username, 'password': password}
        return self.client.post('/login', json=data)

    def test_login_success(self):
        # Test successful login
        response = self.make_login_request('johnsmith', '12345678')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json['data'])
        self.assertIn('refresh_token', response.json['data'])

    def test_login_invalid_username(self):
        # Test login with invalid username
        response = self.make_login_request('invaliduser', '12345678')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['message'], 'Invalid username or password')

    def test_login_invalid_password(self):
        # Test login with invalid password
        response = self.make_login_request('johnsmith', 'invalid_password')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['message'], 'Invalid username or password')

    def test_login_empty_username(self):
        # Test login with empty username
        response = self.make_login_request('', '12345678')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['message'], 'Missing required fields: username')

    def test_login_empty_password(self):
        # Test login with empty password
        response = self.make_login_request('johnsmith', '')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['message'], 'Missing required fields: password')

if __name__ == '__main__':
    unittest.main()
