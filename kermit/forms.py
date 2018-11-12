from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class KermitProject(FlaskForm):
    submit = SubmitField('Submit')


class PickProject(FlaskForm):
    project_type = SelectField('Project types',
                               choices=[('Sock', 'Sock'), ('Mitten', 'Mitten')]
                               )
    submit = SubmitField('Next')


class BasicParameters(FlaskForm):
    spi = DecimalField('Stitches per inch', default=Decimal(8.0), validators=[DataRequired()])
    row_gauge = DecimalField('Rounds per inch (row gauge)', validators=[Optional()])
    submit = SubmitField('Next')


class Metadata(FlaskForm):
    name = StringField('Name')
    yarn = StringField('Yarn')
    needles = StringField('Needles')
    submit = SubmitField('Next')


class SockMeasurements(FlaskForm):
    foot_circ = DecimalField('Foot circumference (in.)')
    ankle_circ = DecimalField('Ankle circumference (in.)')
    gusset_circ = DecimalField('Gusset circumference (in.)')
    foot_length = DecimalField('Foot length (in.)')
    low_calf_circ = DecimalField('Lower calf circumference (in.)')
    heel_diag = DecimalField('Heel diagonal circumference (in.)')
    leg_length = DecimalField('Sock leg length (in.)')
    submit = SubmitField('Next')


class SockDesignChoices(FlaskForm):
    construction = SelectField('Construction style',
                                 choices=[('top_down', 'Top-down (start from cuff)')])
    ease = DecimalField('Ease', default=Decimal(0.9), validators=[Optional()])
    cuff_ribbing = SelectField('Cuff ribbing',
                               choices=[('one_by_one', '1x1 rib'), ('two_by_two', '2x2 rib')]
                              )
    heel_stitch_pattern = SelectField('Heel stitch pattern',
                                      choices=[('stockinette', 'Stockinette'), ('slip_stitch', 'Slip-stitch'),
                                               ('eye_of_partridge', 'Eye of Partridge')]
                                      )
    toe_shaping = SelectField('Toe shaping',
                              choices=[('half_and_half', 'Half and half'), ('simple', 'Simple'),
                                       ('barn', 'Barn')]
                             )
    submit = SubmitField('Next')


class MittenMeasurements(FlaskForm):
    palm_circumference = DecimalField('Palm (hand) circumference (in.)')
    submit = SubmitField('Next')
