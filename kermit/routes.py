from flask import render_template, flash, redirect, url_for
from kermit import app
from kermit.forms import KermitProject, PickProject, SockMeasurements, MittenMeasurements
from kermit.worker import sock_calculate


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
        flash('New project started: {}'.format(form.username.data))
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
    form = SockMeasurements()
    if form.validate_on_submit():
        calcs = sock_calculate(form.data)
        print(calcs)
        return render_template('sock/pattern.html', title="Sock pattern", c=calcs)
    return render_template('sock/measurements.html', title="Sock measurements", form=form)


@app.route('/mitten/measurements', methods=['GET', 'POST'])
def input_mitten_measurements():
    form = MittenMeasurements()
    if form.validate_on_submit():
        return render_template('mitten/pattern.html', title="Mitten pattern", form=form)
    return render_template('mitten/measurements.html', title="Mitten measurements", form=form)
