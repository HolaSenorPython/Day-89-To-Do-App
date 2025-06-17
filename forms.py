from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Make Add task form
class AddTaskForm(FlaskForm):
    task = StringField("Enter the task.", validators=[DataRequired()])
    submit = SubmitField("Add task📎")