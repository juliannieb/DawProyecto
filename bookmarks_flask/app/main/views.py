from flask import render_template, redirect, request, url_for, flash
from forms import ExampleForm, RegistrationForm
from . import main
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	form = ExampleForm()
	return render_template('index.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	flash("dasdasdas")
	print(form.errors)
	if form.validate():
		print("smthn")
	if form.validate_on_submit():
		user = User(username=form.username.data,
					password=form.password.data)
		#db.session.add(user)
		#db.session.commit()
		return redirect(url_for('register'))
	return render_template('register.html', form=form)
