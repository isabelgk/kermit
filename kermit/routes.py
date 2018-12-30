# A Flask session holds:
#    name
#    project_type (i.e. 'sock', 'mitten')
#    design (dict containing relevant design choices as strings)
#    measurement_type (i.e. 'custom')
#    measurements (dict containing relevant measurements as floats)
#
# After the session has been filled with necessary information, routes.py sends the data to the right builder class
# which then returns the pattern section text that is rendered in the pattern html.


from flask import render_template, redirect, session, url_for

from kermit import app
from kermit.builders.mitten import Mitten
from kermit.builders.sock import Sock
from kermit.forms import *


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = KermitProject()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('choose_project_type'))
    return render_template('index.html', title="Home", form=form)


@app.route('/pattern-type', methods=['GET', 'POST'])
def choose_project_type():
    form = PickProject()
    session['project_type'] = form.project_type.data
    if form.project_type.data == 'sock':
        return redirect(url_for('input_sock_design'))
    if form.project_type.data == 'mitten':
        return redirect(url_for('input_mitten_design'))
    return render_template('pattern-type.html', title='Pattern Selection', form=form)


@app.route('/sock/design', methods=['GET', 'POST'])
def input_sock_design():
    form = SockDesignChoices()
    if form.validate_on_submit():
        session['sock_design'] = {'construction': form.construction.data,
                                  'ease': form.ease.data,
                                  'cuff_ribbing': form.cuff_ribbing.data,
                                  'heel_stitch_pattern': form.heel_stitch_pattern.data,
                                  'heel_turn': form.heel_turn.data,
                                  'toe_shaping': form.toe_shaping.data,
                                  }
        return redirect(url_for('input_knitting_parameters'))
    return render_template('sock/design.html', title='Sock Design', form=form)


@app.route('/mitten/design', methods=['GET', 'POST'])
def input_mitten_design():
    form = MittenDesignChoices()
    if form.validate_on_submit():
        session['mitten_design'] = dict()
        return redirect(url_for('input_knitting_parameters'))
    return 'Mitten design is not implemented yet.'  # TODO


@app.route('/knitting-parameters', methods=['GET', 'POST'])
def input_knitting_parameters():
    form = KnittingParameters()
    if form.validate_on_submit():
        session['knitting_parameters'] = {'spi': form.spi.data,
                                          'row_gauge': form.row_gauge.data,
                                          }
        return redirect(url_for('input_measurement_type'))
    return render_template('knitting-parameters.html', title='Knitting Parameters', form=form)


@app.route('/measurement-type', methods=['GET', 'POST'])
def input_measurement_type():
    form = MeasurementType()
    project_type = session.get('project_type')
    if form.validate_on_submit():
        session['measurement_type'] = form.measurement_type.data
        if session.get('measurement_type') == 'standard':
            if project_type == 'sock':
                return redirect(url_for('choose_standard_sock_measurements'))
            elif project_type == 'mitten':
                return redirect(url_for('choose_standard_mitten_measurements'))
        else:  # custom measurements
            if project_type == 'sock':
                return redirect(url_for('input_custom_sock_measurements'))
            elif project_type == 'mitten':
                return redirect(url_for('input_custom_mitten_measurements'))
    return 'Measurement type is not implemented yet.'  # TODO


@app.route('/sock/standard-measurements', methods=['GET', 'POST'])
def choose_standard_sock_measurements():
    form = StandardSockMeasurements()
    session['sock_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('sock_pattern'))
    return 'Standard sock measurement selection is not implemented yet.'  # TODO


@app.route('/mitten/standard-measurements', methods=['GET', 'POST'])
def choose_standard_mitten_measurements():
    form = StandardMittenMeasurements()
    session['mitten_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('mitten_pattern'))
    return 'Standard mitten measurement selection is not implemented yet.'  # TODO


@app.route('/sock/custom-measurements', methods=['GET', 'POST'])
def input_custom_sock_measurements():
    form = CustomSockMeasurements()
    if form.validate_on_submit():
        session['sock_measurements'] = {'foot_circ': form.foot_circ.data,
                                        'ankle_circ': form.ankle_circ.data,
                                        'gusset_circ': form.gusset_circ.data,
                                        'foot_length': form.foot_length.data,
                                        'low_calf_circ': form.low_calf_circ.data,
                                        'heel_diag': form.heel_diag.data,
                                        'leg_length': form.leg_length.data,
                                        }
        return redirect(url_for('sock_pattern'))
    return render_template('sock/custom-measurements.html', title="")  # TODO


@app.route('/mitten/custom-measurements', methods=['GET', 'POST'])
def input_custom_mitten_measurements():
    form = CustomMittenMeasurements()
    session['mitten_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('mitten_pattern'))
    return 'Custom mitten measurement selection is not implemented yet.'  # TODO


@app.route('/sock/pattern')
def sock_pattern():
    sock = Sock(metadata.data, gauge.data, measurements.data, design.data)
    return render_template('sock/pattern.html', title="Sock pattern", d=sock.get_pattern_text_dict())


@app.route('/mitten/pattern')
def mitten_pattern():
    mitten = Mitten()
    return render_template('mitten/pattern.html', title="Mitten pattern", d=mitten.get_pattern_text_dict())

