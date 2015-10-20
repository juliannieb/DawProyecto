from flask import render_template, redirect, request, url_for, flash
from . import users
from .. import db
from .forms import RegistrationForm
from ..models import User


@users.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('main.index'))
	return render_template('register.html', form=form)
