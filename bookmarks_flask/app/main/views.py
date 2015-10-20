from flask import render_template, redirect, request, url_for, flash
from . import main
from .. import db
from .forms import ExampleForm
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	form = ExampleForm()
	return render_template('index.html', form=form)

@main.route('/profile')
def profile():
	return render_template('perfil.html')

@main.route('/bookmarks')
def bookmarks():
	return render_template('bookmarks.html')
