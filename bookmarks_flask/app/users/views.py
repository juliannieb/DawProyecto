from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user
from . import users
from .. import db
from .forms import RegistrationForm, LoginForm
from ..models import User


@users.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
					password=form.password.data,
					first_name=form.first_name.data,
					last_name=form.last_name.data)
		db.session.add(user)
		db.session.commit()
		#login_user(user)
		return redirect(url_for('main.index'))
	return render_template('users/register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(url_for('main.index'))
		flash('Invalid username or password')
		print("could not login")
	return render_template('users/login.html', form=form)
