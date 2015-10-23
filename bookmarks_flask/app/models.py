from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


class User(UserMixin, db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	password_hash = db.Column(db.String(128))
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
