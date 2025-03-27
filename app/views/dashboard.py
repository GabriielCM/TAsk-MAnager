from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint('dashboard_views', __name__)

@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')