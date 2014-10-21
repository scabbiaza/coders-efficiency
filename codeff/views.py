from flask import render_template

from . import app, stat
from .forms import ConfigurationsForm


@app.route('/', methods=['GET', 'POST'])
def home():
    conf = team = authors = None
    form = ConfigurationsForm(csrf_enabled=False)
    if form.validate_on_submit():
        conf = {}
        conf['repo_path'] = form['repo_path'].data
        conf['ignore'] = form['ignore'].data.splitlines() if form['ignore'].data else []
        conf['min_days'] = form['min_days'].data if form['min_days'].data else 0
        conf['min_loc'] = form['min_loc'].data if form['min_loc'].data else 0
        conf['anonym'] = True if form['anonym'].data else False
        team, authors = stat.get_authors_stat(conf)
    return render_template('home.html', form=form, conf=conf, team=team, authors=authors)
