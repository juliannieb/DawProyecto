from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, logout_user, current_user
from . import main
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated():
		return render_template('index.html')
	else:
		return redirect(url_for('users.login'))

@main.route('/profile')
def profile():
	return render_template('profile.html')

@main.route('/bookmarks')
def bookmarks():
	return render_template('bookmarks.html')

@main.route('/books')
def books():
	return render_template('books.html')
