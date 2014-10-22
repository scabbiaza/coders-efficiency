from flask import render_template, flash

from . import app
from .forms import ConfigForm
from .statistic import Statistic


@app.route('/', methods=['GET', 'POST'])
def home():
    rate = None
    form = ConfigForm(csrf_enabled=False)
    if form.validate_on_submit():
        Stat = Statistic()
        Stat.populate_config(form)
        rate = Stat.get_rate()
    return render_template('home.html', form=form, rate=rate)
