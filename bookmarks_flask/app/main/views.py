from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, logout_user, current_user
from . import main
from .. import db
from ..models import User, Bookmark, Category
from .forms import BookmarkForm

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
	bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
	print(bookmarks)
	return render_template('bookmarks.html', bookmarks=bookmarks)

@main.route('/books')
@login_required
def books():
	return render_template('books.html')

@main.route('/add_bookmark')
@login_required
def add_bookmark():
	form = BookmarkForm()
	return render_template('register_bookmark.html', form=form)
