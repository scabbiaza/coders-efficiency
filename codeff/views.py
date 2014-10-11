from flask import render_template

from codeff import app, stat


@app.route('/')
def home():
    conf = {
        'repo_path': None,
        'ignore': ['static/vendors/**', '2.py'],
        'min_days': 0,
        'min_loc': 0,
        'anonym': True,
    }

    team, authors = stat.get_authors_stat(conf)
    return render_template('home.html', conf=conf, team=team, authors=authors)
