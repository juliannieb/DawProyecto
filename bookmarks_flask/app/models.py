from flask import current_app, redirect, url_for, request, session
from flask.ext.login import UserMixin
from rauth import OAuth2Service
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
import json


class User(UserMixin, db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	social_id = db.Column(db.String(64), nullable=True)
	username = db.Column(db.String(64))
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	password_hash = db.Column(db.String(128))
	profile_picture = db.Column(db.String(255))
	bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

	def __repr__(self):
		return '<User: %r>' % self.username

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Bookmark(db.Model):
	__tablename__='bookmarks'
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.String(2200))
	title = db.Column(db.String(64))
	description = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

	def __repr__(self):
		return '<Bookmark: %r>' % self.title


class Category(db.Model):
	__tablename__='categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	bookmarks = db.relationship('Bookmark', backref='category', lazy='dynamic')

	def __repr__(self):
		return '<Category: %r>' % self.name

""" Facebook OAuthSignInMethods """

class OAuthSignIn(object):
	providers = None

	def __init__(self, provider_name):
		self.provider_name = provider_name
		credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
		self.consumer_id = credentials['id']
		self.consumer_secret = credentials['secret']

	def authorize(self):
		pass

	def callback(self):
		pass

	def get_callback_url(self):
		return url_for('users.oauth_callback', provider=self.provider_name, _external=True)

	@classmethod
	def get_provider(self, provider_name):
		if self.providers is None:
			self.providers = {}
			for provider_class in self.__subclasses__():
				provider = provider_class()
				self.providers[provider.provider_name] = provider
		return self.providers[provider_name]

class FacebookSignIn(OAuthSignIn):
	def __init__(self):
		super(FacebookSignIn, self).__init__('facebook')
		self.service = OAuth2Service(
			name='facebook',
			client_id=self.consumer_id,
			client_secret=self.consumer_secret,
			authorize_url='https://graph.facebook.com/oauth/authorize',
			access_token_url='https://graph.facebook.com/oauth/access_token',
			base_url='https://graph.facebook.com/'
		)

	def authorize(self):
		return redirect(self.service.get_authorize_url(
			scope='email',
			response_type='code',
			redirect_uri=self.get_callback_url())
		)

	def callback(self):
		if 'code' not in request.args:
			return None, None
		oauth_session = self.service.get_auth_session(
			data={'code': request.args['code'],
			'grant_type': 'authorization_code',
			'redirect_uri': self.get_callback_url()}
		)
		me = oauth_session.get('me').json()
		print(me)
		print("HOLA\n"*10)
		return(
			'facebook$' + me['id'],
			#me.get('email').split('@')[0]
			me['name']
		)
