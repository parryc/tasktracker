from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email

_due_choices = [(1,'ASAP'),(2,'Soon'),(3,'Later'),(4,'Whenever')]

class TaskForm(FlaskForm):
  task          = TextField('Task', [Required(message='Must provide a task.')])
  project       = QuerySelectField(get_label='project')
  notes         = TextAreaField('Notes')
  high_priority = BooleanField('High Priority')
  due_when      = SelectField('Priority', choices=_due_choices, default=2, coerce=int)
