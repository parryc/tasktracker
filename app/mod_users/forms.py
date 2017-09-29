"""Forms for User interaction."""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, RadioField
from wtforms.validators import Required, Email

class RegisterForm(FlaskForm):
  """FlaskForm to register new users."""

  username  = TextField('Username', [
              Required(message='Must provide an email address.')])
  email     = TextField('Email Address', [Email(),
              Required(message='Must provide an email address.')])
  password  = PasswordField('Password', [
              Required(message='Must provide a password.')])

class EditForm(FlaskForm):
  """FlaskForm to edit existing users."""

  username  = TextField('Username', [
              Required(message='Must provide an email address.')])
  email     = TextField('Email Address', [Email(),
              Required(message='Must provide an email address.')])
  password  = PasswordField('Password')


class LoginForm(FlaskForm):
  """Login form."""

  email    = TextField('Email', [
              Required(message='Must provide an email address.')])
  password = PasswordField('Password', [
              Required(message='Must provide a password.')])
