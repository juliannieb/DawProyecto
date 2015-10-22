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
		self.assertTrue('Registration' in responde.get_data(as_text=True))
