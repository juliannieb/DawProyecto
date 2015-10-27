import os
from flask import render_template, redirect, request, url_for, flash, current_app, send_from_directory
from flask.ext.login import login_user, logout_user, current_user
from werkzeug import secure_filename
from werkzeug.security import safe_join
from . import users
from .. import db
from .. import config
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
		if form.profile_picture.data:
			file = request.files[form.profile_picture.name]
			filename = secure_filename(file.filename)
			username = form.username.data
			extension = filename.split('.')[1]
			directory = safe_join(os.path.join(current_app.config['UPLOAD_FOLDER']), username)
			print(directory)
			print(directory)
			print(directory)
			print(directory)
			print(directory)
			if not os.path.exists(directory):
				print("No existe")
				os.makedirs(directory)
			print("Salio")
			idx_act = 0
			picture_name = "%i.%s" % (idx_act, extension)
			path_picture = safe_join(os.path.join(directory), picture_name)
			while os.path.exists(path_picture):
				idx_act += 1
				picture_name = "%i.%s" % (idx_act, extension)
				path_picture = safe_join(os.path.join(directory), picture_name)
			file.save(path_picture)
			user.profile_picture = picture_name			
		db.session.add(user)
		db.session.commit()
		login_user(user)

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

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))

@users.route('/uploads/<username>/<filename>')
def get_file(filename, username):
	filename = safe_join(os.path.join(username), filename)
	upload_folder = safe_join(os.path.join(os.getcwd()), current_app.config['UPLOAD_FOLDER'])
	print(filename)
	return send_from_directory(upload_folder, filename)



