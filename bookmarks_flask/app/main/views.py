from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, logout_user, current_user
from . import main
from .. import db
from ..models import User, Bookmark, Category
from .forms import BookmarkForm

def get_categories():
	categories = Category.query.all()
	return categories

def get_bookmarks(category_id):
	bookmarks = Bookmark.query.filter_by(user_id=current_user.id, category_id=category_id).all()
	return bookmarks

def get_bookmarks_count_dict(categories):
	bookmarks_count = dict()
	for category in categories:
		bookmarks = get_bookmarks(category.id)
		bookmarks_count[category.name] = len(bookmarks)
	return bookmarks_count

@main.route('/', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated():
		categories = get_categories()
		return render_template('index.html', categories=categories)
	else:
		return redirect(url_for('users.login'))

@main.route('/profile')
@login_required
def profile():
	categories = get_categories()
	bookmarks_count = get_bookmarks_count_dict(categories)
	social_id = ""
	if current_user.social_id:
		social_id = current_user.social_id.split('$')[1]
	return render_template('profile.html', categories=categories,
							bookmarks_count=bookmarks_count,
							social_id=social_id)

@main.route('/bookmarks/<category_id>')
@login_required
def bookmarks(category_id):
	category = Category.query.filter_by(id=category_id).first()
	category_name = ""
	if category:
		category_name = category.name
	categories = get_categories()
	bookmarks = get_bookmarks(category_id)
	return render_template('bookmarks.html', bookmarks=bookmarks,
							categories=categories,
							category_name=category_name,
							category_id=category_id)

@main.route('/books')
@login_required
def books():
	categories = get_categories()
	return render_template('books.html', categories=categories)

@main.route('/add_bookmark',  methods=['GET', 'POST'])
@login_required
def add_bookmark():
	categories = get_categories()
	form = BookmarkForm()
	return render_template('register_bookmark.html', form=form,
							categories=categories)
