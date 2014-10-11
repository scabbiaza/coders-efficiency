from codeff import app
from codeff import stat


@app.route('/')
def index():
    conf = {
        'repo_path': None,
        'ignore': ['*.md', '2.py'],
        'min_days': 0,
        'min_loc': 0,
        'anonym': True,
    }

    team, authors = stat.get_authors_stat(conf)

    print("{:<10}{:>20}{:>20}{:>20}{:>20}"
          .format('Author', 'LOC total', 'Working days', 'Contribution, %', 'Efficiency'))
    i = 0
    for author_name, author in authors.iteritems():
        i += 1
        print("{:<10}{:>20}{:>20}{:>20.2%}{:>20.2}".format(author_name if not conf['anonym'] else 'Coder %d' % i, author['loc'], author['days'], author['contribution'], author['efficiency']))

    return ''
