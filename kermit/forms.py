from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class KermitProject(FlaskForm):
    name = StringField('Your name', default="Your name", validators=[Optional()])
    submit = SubmitField('Submit')


class PickProject(FlaskForm):
    project_type = SelectField('Project types',
                               choices=[('sock', 'Sock'), ('mitten', 'Mitten')]
                               )
    submit = SubmitField('Next')


class KnittingParameters(FlaskForm):
    spi = FloatField('Stitches per inch', default=8, validators=[DataRequired()])
    row_gauge = FloatField('Rounds per inch (row gauge)', default=11, validators=[Optional()])
    yarn = StringField('Yarn', validators=[Optional()])
    needles = StringField('Needles', validators=[Optional()])
    submit = SubmitField('Next')


class MeasurementType(FlaskForm):
    measurement_type = SelectField('Measurement input',
                                   choices=[('standard', 'Standard'), ('custom', 'Custom')])
    submit = SubmitField('Next')


class StandardSockMeasurements(FlaskForm):
    foot_sizing_standard = SelectField('Foot sizing standard',
                                       choices=[('us', 'US/Canadian'), ('eu', 'EU'), ('uk', 'UK')]
                                       )
    style = SelectField('Style',
                         choices=[('men', "Men's"), ('women', "Women's"), ('child', "Child's"), ('kid', "Kid's")]
                        )
    size = FloatField('Size', default=8.5)
    submit = SubmitField('Next')


class CustomSockMeasurements(FlaskForm):
    foot_circ = FloatField('Foot circumference (in.)', default=9.25, validators=[Optional()])
    ankle_circ = FloatField('Ankle circumference (in.)', validators=[Optional()])
    gusset_circ = FloatField('Gusset circumference (in.)', validators=[Optional()])
    foot_length = FloatField('Foot length (in.)', validators=[Optional()])
    low_calf_circ = FloatField('Lower calf circumference (in.)', validators=[Optional()])
    heel_diag = FloatField('Heel diagonal circumference (in.)', validators=[Optional()])
    leg_length = FloatField('Sock leg length (in.)', validators=[Optional()])
    submit = SubmitField('Next')


class SockDesignChoices(FlaskForm):
    construction = SelectField('Construction style',
                               choices=[('top_down', 'Top-down (start from cuff)')],
                               validators=[Optional()])
    ease = FloatField('Ease', default=0.9, validators=[Optional()])
    cuff_ribbing = SelectField('Cuff ribbing',
                               choices=[('one_by_one', '1x1 rib'), ('two_by_two', '2x2 rib')],
                               validators=[Optional()]
                               )
    heel_stitch_pattern = SelectField('Heel stitch pattern',
                                      choices=[('stockinette', 'Stockinette'), ('slip_stitch', 'Slip-stitch'),
                                               ('eye_of_partridge', 'Eye of Partridge')],
                                      validators=[Optional()]
                                      )
    heel_turn = SelectField('Heel construction',
                            choices=[('square_heel', 'Square (Dutch) Heel'), ('round_heel', 'Round (French) Heel'),
                                     ('v_heel', 'V-Heel (Handkerchief Heel)'),
                                     ('band_heel', 'Band (German Strap) Heel')],
                            validators=[Optional()]
                            )
    toe_shaping = SelectField('Toe shaping',
                              choices=[('half_and_half', 'Half and half'), ('simple', 'Simple')],
                              validators=[Optional()]
                             )
    submit = SubmitField('Next')


class MittenDesignChoices(FlaskForm):
    # TODO
    pass


class CustomMittenMeasurements(FlaskForm):
    palm_circumference = FloatField('Palm (hand) circumference (in.)')
    submit = SubmitField('Next')


class StandardMittenMeasurements(FlaskForm):
    submit = SubmitField('Next')
