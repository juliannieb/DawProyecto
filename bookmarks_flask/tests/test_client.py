import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class FlaskClientTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client(use_cookies=True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_registration_page(self):
		response = self.client.get(url_for('users.register'))
		self.assertTrue('Registration' in response.get_data(as_text=True))

	def test_login_page(self):
		response = self.client.get(url_for('users.login'))
		data = response.get_data(as_text=True)
		self.assertTrue('Login' in data)

	def test_user_registration(self):
		response = self.client.post(url_for('users.register'), data={
				'username': 'user',
				'first_name': 'User', 
				'last_name': 'McUserson',
				'password': 'user',
				'confirm_password': 'user' 
			})
		self.assertTrue(response.status_code == 302)

		response = self.client.post(url_for('users.login'), data={
				'username': 'user',
				'password': 'user'
			}, follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue('Organiza' in data)


