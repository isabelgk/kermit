from flask import render_template, redirect, url_for
from kermit import app
from kermit.forms import *
from kermit.builder import sock_calculate, mitten_calculate


@app.route('/')
@app.route('/index')
def index():
    form = KermitProject()
    return render_template('index.html', title="Home", form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def start_new_project():
    form = KermitProject()
    if form.validate_on_submit():
        return redirect(url_for('select_type'))
    return render_template('index.html', title="Home", form=form)


@app.route('/pattern-type', methods=['GET', 'POST'])
def select_type():
    form = PickProject()
    if form.project_type.data == "Sock":
        return redirect(url_for('input_sock_measurements'))
    if form.project_type.data == "Mitten":
        return redirect(url_for('input_mitten_measurements'))
    return render_template('pattern-type.html', title="Pattern Selection", form=form)


@app.route('/sock/measurements', methods=['GET', 'POST'])
def input_sock_measurements():
    parameters = BasicParameters()
    measurements = SockMeasurements()
    design = SockDesignChoices()
    metadata = Metadata()
    if measurements.validate_on_submit():
        calcs = sock_calculate(parameters.data, measurements.data)
        print(calcs)
        return render_template('sock/pattern.html', title="Sock pattern", calcs=calcs)
    return render_template('sock/measurements.html', title="Sock measurements",
                           parameters=parameters, measurements=measurements, design=design,
                           metadata=metadata)


@app.route('/mitten/measurements', methods=['GET', 'POST'])
def input_mitten_measurements():
    form = MittenMeasurements()
    if form.validate_on_submit():
        calcs = mitten_calculate(form.data)
        return render_template('mitten/pattern.html', title="Mitten pattern", c=calcs)
    return render_template('mitten/measurements.html', title="Mitten measurements", form=form)
