from flask import render_template
from forms import ExampleForm
from . import main

@main.route('/')
def index():
	form = ExampleForm()
	return render_template('index.html', form=form)
