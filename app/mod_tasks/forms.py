from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import Required, Email

_priority_choices = [('High',1),('Medium',2),('Low'),3]

class TaskForm(FlaskForm):
  task  = TextField('Task', [Required(message='Must provide a task.')])
  #notes    = TextAreField('Notes')
  #priority = SelectField('Priority', choices=_priority_choices, default='Low')