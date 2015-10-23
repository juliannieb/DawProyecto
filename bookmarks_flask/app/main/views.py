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
@login_required
def profile():
	return render_template('profile.html')

@main.route('/bookmarks')
@login_required
def bookmarks():
	return render_template('bookmarks.html')

@main.route('/books')
@login_required
def books():
	return render_template('books.html')
