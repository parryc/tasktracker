from flask import Blueprint, request, render_template, \
                  flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.mod_tasks.forms import *
from app.mod_tasks.models import *
from app.helpers import *

mod_tasks = Blueprint('tasks', __name__, url_prefix='/tasks')
t = 'Tasks'  # Title
m = 'Tasks'  # Module

##########
# Routes #
##########


@mod_tasks.route('/<int:number>', methods=['GET'])
@login_required
def index(number):
  """Display list of all users."""
  task_list = get_tasks_by_user(current_user, number=number)
  return render_template('tasks/index.html'
                        ,task_list=task_list
                        ,t=t
                        ,m=m)