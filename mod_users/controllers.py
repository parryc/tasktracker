from flask import Blueprint, request, render_template, \
                  flash, redirect, url_for, abort
from mod_users.forms import *
from mod_users.models import *
from mod_projects.models import *
from mod_tasks.models import *
from flask_login import login_required, current_user
from helpers import *

mod_users = Blueprint('users', __name__, url_prefix='/users')
t = 'users'  # Title
m = 'users'  # Module

##########
# Routes #
##########


@mod_users.route('/', methods=['GET'])
@login_required
def index():
  """Display list of all users."""
  user_list = Users.query.all()
  return render_template('users/index.html'
                        ,user_list=user_list
                        ,t=t
                        ,m=m)


@mod_users.route('/<int:user_id>', methods=['GET'])
@login_required
def show(user_id):
  """Show user information, but only if admin."""
  if user_id != current_user.id:
    return abort(403)

  user = get_user(user_id)
  return render_template('users/show.html'
                        ,user=user
                        ,t=t
                        ,m=m)


@mod_users.route('/register', methods=['GET','POST'])
def add():
  """Display add user form, if admin."""
  form = RegisterForm(request.form)
  if form.validate_on_submit():
    username  = form.username.data
    password  = form.password.data
    email     = form.email.data
    
    save_result = add_user(username, password, email)
    if save_result['status']:
      # create a starter project
      save_result_project = add_project(save_result['entry'], 'my first project', [], 'an example project', True, 2)
      save_result_task = add_task(save_result['entry'].id, 'this is an example task', save_result_project['entry'].id, 'you can edit these notes', False, False, 2, '1970-01-01')
      flash(u'thanks for joining, %s. please login!' % username, 'success')
    else:
      flash(u'cannot register "%s". try a different username or email.' % username, 'error')
      return redirect(url_for('.add'))

    return redirect(url_for('login'))

  return render_template('users/register.html'
                        ,form=form
                        ,t=t
                        ,m=m)


@mod_users.route('/edit/<int:user_id>', methods=['GET','POST'])
@login_required
def edit(user_id):
  """Display edit user form, if admin."""
  if user_id != current_user.id:
    return abort(403)

  user = get_user(user_id)
  form = EditForm(obj=user)
  form.email.data = user.email

  if form.validate_on_submit():
    password = form.password.data
    username = form.username.data

    save_result = edit_user(user_id, password, username, user.active)
    user = save_result['entry']
    form = EditForm(request.form, obj=save_result['entry'])
    form.email.data = user.email
    return redirect(url_for('.index'))
  
  return render_template('users/edit.html'
                        ,form=form
                        ,user=user
                        ,t=t
                        ,m=m)
