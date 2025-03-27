from flask import Blueprint, render_template
from flask_login import login_required

tasks = Blueprint('tasks_views', __name__)

@tasks.route('/')
@login_required
def index():
    return render_template('tasks/index.html')

@tasks.route('/<int:task_id>')
@login_required
def task_detail(task_id):
    return render_template('tasks/detail.html', task_id=task_id)