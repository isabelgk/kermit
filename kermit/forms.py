from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class NewProject(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Start')


class PickProject(FlaskForm):
    project_type_dropdown_list = [('Sock', 'Sock'), ('Mitten', 'Mitten')]
    project_type = SelectField('Project types', choices=project_type_dropdown_list)
    submit = SubmitField('Next')


class SockMeasurements(FlaskForm):
    submit = SubmitField('Next')


class MittenMeasurements(FlaskForm):
    submit = SubmitField('Next')
