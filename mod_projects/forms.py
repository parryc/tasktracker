from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required

class ProjectForm(FlaskForm):
  _priority_choices = [(1,'high'),(2,'medium'),(3,'low')]

  project  = TextField('project name', [Required(message='must provide a project name.')])
  notes    = TextAreaField('notes')
  priority = SelectField('priority', choices=_priority_choices, default=2, coerce=int)
  active   = BooleanField('active')