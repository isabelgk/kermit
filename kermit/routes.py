from flask import render_template, flash, redirect, url_for
from kermit import app
from kermit.forms import NewProject, PickProject

@app.route('/')
@app.route('/index')
def index():
    form = NewProject()
    return render_template('index.html', title="Home", form=form)

@app.route('/index', methods=['GET', 'POST'])
def start_new_project():
    form = NewProject()
    if form.validate_on_submit():
        flash('New project started: {}'.format(form.username.data))
        return redirect(url_for('pattern_select'))
    return render_template('index.html', title="Home", form=form)


@app.route('/pattern', methods=['GET', 'POST'])
def pattern_select():
    form = PickProject()
    return render_template('pattern.html', title="Pattern Selection", form=form)
