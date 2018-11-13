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
    row_gauge = DecimalField('Rounds per inch (row gauge)', default=Decimal(11), validators=[Optional()])
    submit = SubmitField('Next')


class Metadata(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    yarn = StringField('Yarn', validators=[Optional()])
    needles = StringField('Needles', validators=[Optional()])
    submit = SubmitField('Next', validators=[Optional()])


class SockMeasurements(FlaskForm):
    foot_circ = DecimalField('Foot circumference (in.)', default=Decimal(9.25), validators=[Optional()])
    ankle_circ = DecimalField('Ankle circumference (in.)', validators=[Optional()])
    gusset_circ = DecimalField('Gusset circumference (in.)', validators=[Optional()])
    foot_length = DecimalField('Foot length (in.)', validators=[Optional()])
    low_calf_circ = DecimalField('Lower calf circumference (in.)', validators=[Optional()])
    heel_diag = DecimalField('Heel diagonal circumference (in.)', validators=[Optional()])
    leg_length = DecimalField('Sock leg length (in.)', validators=[Optional()])
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
    heel_turn = SelectField('Heel construction',
                            choices=[('square_heel', 'Square (Dutch) Heel'), ('round_heel', 'Round (French) Heel'),
                                     ('v_heel', 'V-Heel (Handkerchief Heel)'),
                                     ('band_heel', 'Band (German Strap) Heel')]
                            )
    toe_shaping = SelectField('Toe shaping',
                              choices=[('half_and_half', 'Half and half'), ('simple', 'Simple')]
                             )
    submit = SubmitField('Next')


class MittenMeasurements(FlaskForm):
    palm_circumference = DecimalField('Palm (hand) circumference (in.)')
    submit = SubmitField('Next')
