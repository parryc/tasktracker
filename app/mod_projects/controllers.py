from flask import Blueprint, request, render_template, \
                  flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.mod_projects.forms import *
from app.mod_projects.models import *
from app.helpers import *

mod_projects = Blueprint('projects', __name__, url_prefix='/projects')
t = 'Projects'  # Title
m = 'Projects'  # Module

##########
# Routes #
##########


@mod_projects.route('/', methods=['GET'])
@login_required
def index():
  projects = get_projects_by_user(current_user)
  return render_template('projects/index.html'
                        ,projects=projects
                        ,t=t
                        ,m=m)


@mod_projects.route('/add', methods=['GET','POST'])
@login_required
def add():
  form = ProjectForm(request.form)
  print(form.priority.data)
  if form.validate_on_submit():
    project  = form.project.data
    notes    = form.notes.data
    priority = form.priority.data
    
    save_result = add_project(current_user, project, [], notes, True, priority)
    if save_result['status']:
      flash(u'Project %s was successfully added.' % project, 'success')
    else:
      flash(u'Cannot add %s to database. %s' % (project, save_result['message']), 'error')

    return redirect(url_for('.index'))

  return render_template('projects/add.html'
                        ,form=form
                        ,t=t
                        ,m=m)
