from app import db
from datetime import datetime
from helpers.helpers_db import *
from datetime import timedelta


class Projects(db.Model):
  """Model for a project"""

  __tablename__   = 'projects'

  id          = db.Column(db.Integer, primary_key=True)
  user        = db.Column(db.Integer, db.ForeignKey('users.id'))
  project     = db.Column(db.Text())
  tasks       = db.relationship('Tasks', backref='project', lazy='dynamic')
  notes       = db.Column(db.Text())
  active      = db.Column(db.Boolean)
  priority    = db.Column(db.Integer)

  creation_datetime  = db.Column(db.DateTime)
  last_modified      = db.Column(db.DateTime)

  def __init__(self, user, project, tasks, notes, active,
               priority, creation_datetime=None,
               last_modified=None):

    self.user          = user
    self.project       = project
    self.tasks         = tasks
    self.notes         = notes
    self.active        = active
    self.priority      = priority

    if creation_datetime is None:
        creation_datetime = datetime.utcnow()
    if last_modified is None:
        last_modified = datetime.utcnow()
    self.creation_datetime  = creation_datetime
    self.last_modified      = last_modified

  def __repr__(self):
    """<project (project_id)>."""
    return '<project %r>' % (self.id)

##########
# CREATE #
##########


def add_project(user, project, tasks, notes, active, priority):
  project_entry = Projects(user=user.id
                    ,project=project
                    ,tasks=tasks
                    ,notes=notes
                    ,active=active
                    ,priority=priority)
  db.session.add(project_entry)
  return commit_entry(project_entry)

##########
# UPDATE #
##########


def edit_project(id, project, notes, active, priority):
  _project = get_project(id)
  _project.project = project
  _project.notes = notes
  _project.active = active
  _project.priority = priority
  _project.last_modified = datetime.utcnow()
  return commit_entry(_project)


def inactive_project(id):
  _project = get_project(id)
  _project.active = False
  return commit_entry(_project)


###########
# GETTERS #
###########


def get_project(id):
  """Get single project by id."""
  return db.session.query(Projects).get(id)


def get_projects_by_user(user):
  return Projects.query.filter_by(user=user.id)