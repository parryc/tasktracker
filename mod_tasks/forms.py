from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email

_due_choices = [(1,'asap'),(2,'soon'),(3,'later'),(4,'whenever'),(10,'backlog')]

class TaskForm(FlaskForm):
  task          = TextField('task', [Required(message='must provide a task.')])
  project       = QuerySelectField(get_label='project')
  notes         = TextAreaField('notes')
  high_priority = BooleanField('high priority')
  due_when      = SelectField('priority', choices=_due_choices, default=2, coerce=int)
  complete      = BooleanField('high priority')