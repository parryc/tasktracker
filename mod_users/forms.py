"""Forms for User interaction."""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, RadioField
from wtforms.validators import Required, Email

class RegisterForm(FlaskForm):
  """FlaskForm to register new users."""

  username  = TextField('username', [
              Required(message='must provide an email address.')])
  email     = TextField('email address', [Email(),
              Required(message='must provide an email address.')])
  password  = PasswordField('password', [
              Required(message='must provide a password.')])

class EditForm(FlaskForm):
  """FlaskForm to edit existing users."""

  username  = TextField('username', [
              Required(message='must provide an email address.')])
  email     = TextField('email address', [Email(),
              Required(message='must provide an email address.')])
  password  = PasswordField('password')


class LoginForm(FlaskForm):
  """Login form."""

  email    = TextField('email', [
              Required(message='must provide an email address.')])
  password = PasswordField('password', [
              Required(message='must provide a password.')])
