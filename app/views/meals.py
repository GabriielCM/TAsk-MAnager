from flask import Blueprint, render_template
from flask_login import login_required

meals = Blueprint('meals_views', __name__)

@meals.route('/')
@login_required
def index():
    return render_template('meals/index.html')

@meals.route('/add')
@login_required
def add():
    return render_template('meals/add.html')