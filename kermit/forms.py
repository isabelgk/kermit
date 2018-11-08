from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class KermitProject(FlaskForm):
    username = StringField('Name')
    submit = SubmitField('Start')


class PickProject(KermitProject):
    project_type_dropdown_list = [('Sock', 'Sock'), ('Mitten', 'Mitten')]
    project_type = SelectField('Project types', choices=project_type_dropdown_list)
    submit = SubmitField('Next')


class SockMeasurements(KermitProject):
    spi = DecimalField('Stitches per inch', validators=[DataRequired()])
    row_gauge = DecimalField('Rounds per inch (row gauge)')
    foot_circ = DecimalField('Foot circumference (in.)')
    ankle_circ = DecimalField('Ankle circumference (in.)')
    gusset_circ = DecimalField('Gusset circumference (in.)')
    foot_length = DecimalField('Foot length (in.)')
    low_calf_circ = DecimalField('Lower calf circumference (in.)')
    heel_diag = DecimalField('Heel diagonal (in.)')
    leg_length = DecimalField('Sock leg length (in.)')
    submit = SubmitField('Next')


class MittenMeasurements(FlaskForm):
    submit = SubmitField('Next')
