from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import Required

class ProjectForm(FlaskForm):
  _priority_choices = [(1,'high'),(2,'medium'),(3,'low')]

  project  = TextField('Project Name', [Required(message='Must provide a project name.')])
  notes    = TextAreaField('Notes')
  priority = SelectField('Priority', choices=_priority_choices, default=2, coerce=int)