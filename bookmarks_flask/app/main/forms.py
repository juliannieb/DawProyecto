from flask.ext.wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, RadioField, BooleanField, \
        SubmitField, IntegerField, FormField, StringField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import Required, EqualTo, DataRequired
from wtforms.widgets import Input
from ..models import User, Bookmark

class BookmarkForm(Form):
    link = TextField('Link', validators=[Required()])
    submit = SubmitField('Submit')


