from flask import render_template, redirect, request, url_for, flash
from . import main
from .. import db
from .forms import ExampleForm
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	form = ExampleForm()
	return render_template('index.html', form=form)


