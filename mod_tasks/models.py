from app import db
from datetime import datetime
from helpers.helpers_db import *
from datetime import timedelta


class Tasks(db.Model):
  """Model for a task"""

  __tablename__   = 'tasks'

  id          = db.Column(db.Integer, primary_key=True)
  user        = db.Column(db.Integer, db.ForeignKey('users.id'))
  project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'))
  task        = db.Column(db.Text())
  notes       = db.Column(db.Text())
  complete    = db.Column(db.Boolean)

  high_priority = db.Column(db.Boolean)
  due_when      = db.Column(db.Integer)
  due_date      = db.Column(db.DateTime)

  creation_datetime  = db.Column(db.DateTime)
  last_modified      = db.Column(db.DateTime)
  completed_datetime = db.Column(db.DateTime)

  def __init__(self, user, project_id, task, notes, complete,
               high_priority, due_when, due_date, creation_datetime=None,
               last_modified=None, completed_datetime=None):

    self.user          = user
    self.project_id    = project_id
    self.task          = task
    self.notes         = notes
    self.complete      = complete
    self.high_priority = high_priority
    self.due_when      = due_when
    self.due_date      = due_date

    if creation_datetime is None:
        creation_datetime = datetime.utcnow()
    if last_modified is None:
        last_modified = datetime.utcnow()
    self.creation_datetime  = creation_datetime
    self.last_modified      = last_modified
    self.completed_datetime = completed_datetime

  def __repr__(self):
    """<task (task_id)>."""
    return '<task %r>' % (self.id)

##########
# CREATE #
##########


def add_task(user, task, project, notes, complete, high_priority, due_when, due_date):
  task_entry = Tasks(user=user
                    ,project_id=project
                    ,task=task
                    ,notes=notes
                    ,complete=complete
                    ,high_priority=high_priority
                    ,due_when=due_when
                    ,due_date=due_date)
  db.session.add(task_entry)
  return commit_entry(task_entry)

##########
# UPDATE #
##########


def edit_task(id, task, project, notes, complete, high_priority, due_when, due_date):
  _task = get_task(id)
  _task.project = project
  _task.task = task
  _task.notes = notes
  _task.complete = complete
  if complete:
    _task.completed_datetime = datetime.utcnow()
  else:
    _task.completed_datetime = None
  _task.high_priority = high_priority
  _task.due_when = due_when
  _task.due_date = due_date
  _task.last_modified = datetime.utcnow()
  return commit_entry(_task)


def complete_task(id):
  _task = get_task(id)
  _task.complete = True
  _task.completed_datetime = datetime.utcnow()
  return commit_entry(_task)


###########
# GETTERS #
###########


def get_task(id):
  """Get single task by id."""
  return db.session.query(Tasks).get(id)

def get_tasks_by_user(user, number=-1, include_complete=False, include_backlog=True):
  query = Tasks.query.filter_by(user=user.id)
  
  if not include_complete:
    query = query.filter_by(complete=False)

  if not include_backlog:
    query = query.filter(Tasks.due_when < 10)

  if number == -1:
    return query.all()
  else:
    return query.limit(number).all()