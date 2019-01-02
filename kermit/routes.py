# A Flask session holds:
#    name
#    project_type (i.e. 'sock', 'mitten')
#    design (dict containing relevant design choices as strings)
#    knitting parameters (i.e. spi)
#    measurement_type (i.e. 'custom')
#    measurements (dict containing relevant measurements as floats)
#
# After the session has been filled with necessary information, routes.py sends the data to the right builder class
# which then returns the pattern section text that is rendered in the pattern html.


from flask import render_template, redirect, session, url_for

from kermit import app
from kermit.builders.mitten import Mitten
from kermit.builders.sock import Sock
from kermit.builders.standard_sock_sizer import sock_sizer
from kermit.forms import KermitProject, SockDesignChoices, KnittingParameters, MeasurementType, \
    CustomSockMeasurements, StandardSockMeasurements, StandardMittenMeasurements, CustomMittenMeasurements, \
    MittenDesignChoices


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = KermitProject()
    session['name'] = form.name.data
    if form.validate_on_submit():
        return redirect(url_for('choose_project_type'))
    return render_template('index.html', title="Home", form=form)


@app.route('/project-type', methods=['GET', 'POST'])
def choose_project_type():
    return render_template('pattern-type.html', title='Pattern Selection')


@app.route('/sock/design', methods=['GET', 'POST'])
def input_sock_design():
    session['project_type'] = 'sock'
    form = SockDesignChoices()
    session['sock_design'] = {'construction': form.construction.data,
                              'ease': form.ease.data,
                              'cuff_ribbing': form.cuff_ribbing.data,
                              'heel_stitch_pattern': form.heel_stitch_pattern.data,
                              'heel_turn': form.heel_turn.data,
                              'toe_shaping': form.toe_shaping.data,
                              }
    if form.validate_on_submit():
        return redirect(url_for('input_knitting_parameters'))
    return render_template('sock/design.html', title='Sock Design', form=form)


@app.route('/mitten/design', methods=['GET', 'POST'])
def input_mitten_design():
    session['project_type'] = 'mitten'
    form = MittenDesignChoices()
    session['mitten_design'] = dict()
    if form.validate_on_submit():
        return redirect(url_for('input_knitting_parameters'))
    return 'Mitten design is selection is under development. Try making socks instead.'  # TODO


@app.route('/knitting-parameters', methods=['GET', 'POST'])
def input_knitting_parameters():
    form = KnittingParameters()
    session['knitting_parameters'] = {'spi': form.spi.data,
                                      'row_gauge': form.row_gauge.data,
                                      'yarn': form.yarn.data,
                                      'needles': form.needles.data,
                                      }
    if form.validate_on_submit():
        return redirect(url_for('input_measurement_type'))
    return render_template('knitting-parameters.html', title='Knitting Parameters', form=form)


@app.route('/measurement-type', methods=['GET', 'POST'])
def input_measurement_type():
    form = MeasurementType()
    project_type = session.get('project_type')
    session['measurement_type'] = form.measurement_type.data
    if form.validate_on_submit():
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
    return render_template('measurement-type.html', title='Measurement Type', form=form)


@app.route('/sock/standard-measurements', methods=['GET', 'POST'])
def choose_standard_sock_measurements():
    form = StandardSockMeasurements()
    if form.validate_on_submit():
        session['sock_measurements'] = sock_sizer({'foot_sizing_standard': form.foot_sizing_standard.data,
                                                   'style': form.style.data,
                                                   'size': form.size.data,
                                                   })
        sock = Sock(session)
        return render_template('sock/pattern.html', title="Sock pattern", d=sock.get_pattern_text_dict())
    return render_template('sock/standard-measurements.html', title='Standard Sock Sizes', form=form)


@app.route('/mitten/standard-measurements', methods=['GET', 'POST'])
def choose_standard_mitten_measurements():
    form = StandardMittenMeasurements()
    session['mitten_measurements'] = form.data
    if form.validate_on_submit():
        return "redirect(url_for('mitten_pattern'))"  # TODO
    return 'Standard mitten measurement selection is under development. Try using custom.'  # TODO


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
        sock = Sock(session)
        return render_template('sock/pattern.html', title="Sock pattern", d=sock.get_pattern_text_dict())
    return render_template('sock/custom-measurements.html', title="Custom Sock Measurements", form=form)


@app.route('/mitten/custom-measurements', methods=['GET', 'POST'])
def input_custom_mitten_measurements():
    form = CustomMittenMeasurements()
    session['mitten_measurements'] = form.data
    if form.validate_on_submit():
        return "redirect(url_for('mitten_pattern'))"  # TODO
    return render_template('mitten/custom-measurements.html', title="Custom Mitten Measurements", form=form)


@app.route('/sock/pattern')
def sock_pattern():  # TODO
    sock = Sock(session)
    if form.validate_on_submit():
        return render_template('sock/pattern.html', title="Sock pattern", d=sock.get_pattern_text_dict())


@app.route('/mitten/pattern')
def mitten_pattern():  # TODO
    mitten = Mitten()
    return render_template('mitten/pattern.html', title="Mitten pattern", d=mitten.get_pattern_text_dict())

