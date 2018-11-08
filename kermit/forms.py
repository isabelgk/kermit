from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewProject(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Start')


class PickProject(FlaskForm):
    pattern_type = BooleanField('Top-Down Sock')
    submit = SubmitField('Next')
