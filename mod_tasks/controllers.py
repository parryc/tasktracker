from flask import Blueprint, request, render_template, \
                  flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from mod_tasks.forms import *
from mod_tasks.models import *
from mod_projects.models import get_projects_by_user
from helpers import *
from app import csrf

mod_tasks = Blueprint('tasks', __name__, url_prefix='/tasks')
t = 'tasks'  # Title
m = 'tasks'  # Module

##########
# Routes #
##########

@mod_tasks.route('/', methods=['GET'])
@login_required
def index():
  if not hasattr(current_user, 'id'):
    return redirect(url_for('login'))

  tasks = get_tasks_by_user(current_user, number=-1)
  for task in tasks:
    task.priority = task.project.priority + task.due_when - task.high_priority
  tasks = sorted(tasks, key=lambda x:x.priority)

  return render_template('tasks/index.html'
                        ,tasks=tasks
                        ,t=t
                        ,m=m)

@mod_tasks.route('/add', methods=['GET','POST'])
@login_required
def add():
  form = TaskForm(request.form)
  form.project.query = get_projects_by_user(current_user)
  if form.validate_on_submit():
    task     = form.task.data
    project  = form.project.data.id
    print(project)
    notes    = form.notes.data
    due_when = form.due_when.data
    high_priority = form.high_priority.data
    
    save_result = add_task(current_user.id, task, project, notes, False, high_priority, due_when)
    if save_result['status']:
      flash(u'task added successfully.', 'success')
    else:
      flash(u'cannot create task. %s' % (task, save_result['message']), 'error')

    return redirect(url_for('.index'))

  return render_template('tasks/add.html'
                        ,form=form
                        ,t=t
                        ,m=m
                        ,hide_subnav=True)


@mod_tasks.route('/edit/<int:task_id>', methods=['GET','POST'])
@login_required
def edit(task_id):
  task = get_task(task_id)
  if task not in get_tasks_by_user(current_user, include_inactive=True):
    abort(403)

  form = TaskForm(obj=task)
  form.project.query = get_projects_by_user(current_user)
  if form.validate_on_submit():
    task     = form.task.data
    project  = form.project.data
    notes    = form.notes.data
    due_when = form.due_when.data
    high_priority = form.high_priority.data
    complete = form.complete.data
    
    save_result = edit_task(task_id, task, project, notes, complete, high_priority, due_when)
    if save_result['status']:
      flash(u'task was edited successfully.', 'success')
    else:
      flash(u'cannot edit "%s". %s' % (task, save_result['message']), 'error')

    return redirect(url_for('.edit', task_id=task_id))

  return render_template('tasks/edit.html'
                        ,form=form
                        ,task=task
                        ,t=t
                        ,m=m)

@mod_tasks.route('/complete/<int:task_id>', methods=['POST'])
@login_required
@csrf.exempt
def complete(task_id):
  task = get_task(task_id)
  if task not in get_tasks_by_user(current_user):
    abort(403)

  complete_task(task_id)
  return jsonify({'success':True})