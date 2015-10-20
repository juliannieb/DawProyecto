from flask import render_template, redirect, request, url_for, flash
from . import main
from .. import db
from .forms import ExampleForm, RegistrationForm
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	form = ExampleForm()
	return render_template('index.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
					password=form.password.data)
		print(user)
		#db.session.add(user)
		#db.session.commit()
		return redirect(url_for('main.index'))
	return render_template('register.html', form=form)

@main.route('/test', methods=['GET', 'POST'])
def test():
	form = ExampleForm()
	return render_template('test.html', form=form)
