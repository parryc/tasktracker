from app import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from helpers.helpers_db import *
from flask_permissions.models import UserMixin
from datetime import timedelta
import uuid


class Users(UserMixin):
  """Model for a user of Caine."""

  __tablename__   = 'users'
  __table_args__  = (db.UniqueConstraint('username', 'email', name='_user_uc'),)
  # Identify the class to differentiate between sub-types of the UserMixin.
  # This can be any unique value except 'usermixin'.
  __mapper_args__ = {'polymorphic_identity': 'user'}

  id          = db.Column(db.Integer, db.ForeignKey('fp_user.id'), primary_key=True)
  username    = db.Column(db.Text(), unique=True)
  email       = db.Column(db.Text(), unique=True)
  password    = db.Column(db.Text())

  active      = db.Column(db.Boolean)
  logged_in   = db.Column(db.Boolean)

  creation_datetime = db.Column(db.DateTime)
  last_logged_in    = db.Column(db.DateTime)

  def __init__(self, username, email, password, active=True
              ,logged_in=False, creation_datetime=None, last_logged_in=None):
    """Create user in database."""
    self.username       = username
    self.email          = email
    self.password       = password
    self.active         = active
    self.logged_in      = logged_in

    if creation_datetime is None:
        creation_datetime = datetime.utcnow()
    if last_logged_in is None:
        last_logged_in = datetime.utcnow()
    self.creation_datetime = creation_datetime
    self.last_logged_in    = last_logged_in

    UserMixin.__init__(self)

  def __repr__(self):
    """<user (username)>."""
    return '<user %r>' % (self.username)

  def hash_password(self, password):
    """Hash password user library functions."""
    self.password = pwd_context.encrypt(password)

  def validate_password(self, password):
    """Validate that the entered password is correct."""
    return pwd_context.verify(password, self.password)

  # following functions must be created for flask-login to work
  def is_authenticated(self):
    """Check if user is logged in."""
    return self.logged_in

  def is_active(self):
    """Check if user is active."""
    return self.active

  def is_anonymous(self):
    """Check if current user is anonymous or lgged in.

    From Flask-Login docs
    Returns True if this is an anonymous user. (Actual users should return False instead.)
    """
    return False

  def get_id(self):
    """Return user id as unicode string.

    This is to support Flask-Login functions.
    """
    return unicode(self.id)

##########
# CREATE #
##########


def add_user(username, password, email):
  """Add user to database."""
  user_entry = Users(username=username
                    ,password='secret_dummy! lol!'
                    ,email=email)
  user_entry.hash_password(password)
  db.session.add(user_entry)
  return commit_entry(user_entry)

##########
# UPDATE #
##########


def edit_user(_id, password, username, active):
  """Update user in database."""
  user           = get_user(_id)
  user.username  = user.username
  if password.strip():
      user.hash_password(password)
  user.username  = username
  user.active    = active
  # so as not to erase the last logged in time
  user.last_logged_in = user.last_logged_in

  return commit_entry(user)


##########
# DELETE #
##########


def delete_user(_id):
  """Delete single user from database."""
  return delete_entry(get_user(_id))


###########
# GETTERS #
###########


def get_user(user_id):
  """Get single user by ID."""
  return Users.query.filter_by(id=user_id).first()


def get_user_by_username(username):
  """Get single user by username."""
  return Users.query.filter_by(username=username).first()


def get_user_by_email(email):
  """Get single user by email."""
  return Users.query.filter_by(email=email).first()
