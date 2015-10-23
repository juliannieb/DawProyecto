from flask.ext.wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, RadioField, BooleanField, \
        SubmitField, IntegerField, FormField, StringField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import Required, EqualTo, DataRequired, Length, Regexp
from wtforms.widgets import Input
from ..models import User, Bookmark

class RegistrationForm(Form):
    username = TextField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    first_name = TextField('First name', validators=[Required(), Length(1, 64)])
    last_name = TextField('Last name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')


class LoginForm(Form):
	username = TextField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me', description='Checkboxes can be tricky.')
	submit = SubmitField('Login')