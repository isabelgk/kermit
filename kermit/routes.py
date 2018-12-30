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
    if form.project_type.data == "sock":
        return redirect(url_for('input_sock_design'))
    if form.project_type.data == "Mitten":
        return redirect(url_for('input_mitten_design'))
    return render_template('pattern-type.html', title="Pattern Selection", form=form)


@app.route('/sock/design', methods=['GET', 'POST'])
def input_sock_design():
    form = SockDesignChoices()
    session['design'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('input_knitting_parameters'))
    return 'sock design placeholder'


@app.route('/mitten/design', methods=['GET', 'POST'])
def input_mitten_design():
    form = MittenDesignChoices()
    session['design'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('input_knitting_parameters'))
    return 'mitten design placeholder'


@app.route('/knitting-parameters', methods=['GET', 'POST'])
def input_knitting_parameters():
    form = KnittingParameters()
    session['knitting_parameters'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('input_measurement_type'))
    return 'knitting parameters placeholder'


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
    return 'measurement type placeholder'


@app.route('/sock/standard-measurements', methods=['GET', 'POST'])
def choose_standard_sock_measurements():
    form = StandardSockMeasurements()
    session['sock_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('sock_pattern'))
    return 'standard sock measurements placeholder'


@app.route('/mitten/standard-measurements', methods=['GET', 'POST'])
def choose_standard_mitten_measurements():
    form = StandardMittenMeasurements()
    session['mitten_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('mitten_pattern'))
    return 'standard mitten measurements placeholder'


@app.route('/sock/custom-measurements', methods=['GET', 'POST'])
def input_custom_sock_measurements():
    form = CustomSockMeasurements()
    session['sock_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('sock_pattern'))
    return 'custom sock measurements placeholder'


@app.route('/mitten/custom-measurements', methods=['GET', 'POST'])
def input_custom_mitten_measurements():
    form = CustomMittenMeasurements()
    session['mitten_measurements'] = form.data
    if form.validate_on_submit():
        return redirect(url_for('mitten_pattern'))
    return 'custom mitten measurements placeholder'


@app.route('/sock/pattern')
def sock_pattern():
    sock = Sock(metadata.data, gauge.data, measurements.data, design.data)
    return render_template('sock/pattern.html', title="Sock pattern", d=sock.get_pattern_text_dict())


@app.route('/mitten/pattern')
def mitten_pattern():
    mitten = Mitten()
    return render_template('mitten/pattern.html', title="Mitten pattern", d=mitten.get_pattern_text_dict())

