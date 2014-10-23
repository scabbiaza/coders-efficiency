# Algorithm
#
# 1. Get list of authors:
#    git log --format='%aN' | sort -u
#
# 2. Get list of not ignored files
#    git ls-files
#
# 3. Get working days for every author (any day that has commits => is working day):
#    git log --date=short --pretty="format:%ad" --author=<author>
#    (remove duplicates)
#
# 4. Get total working days
#
# 5. Get author for every line in every file, add this to author statistic:
#    git blame <filename> -w
#
# 6. Get total LOC
#
# 7. Calculate team's efficiency (part of the code created per day):
#    (total LOC / total working days) / total LOC
#
# 8. Calculate authors' contribution and efficiency as:
#    contribution = author LOC / total LOC (part of the code created by author)
#    potential LOC = author LOC per day * total working days
#    efficiency in team = potential LOC / min potential LOC

import fnmatch

from collections import OrderedDict

from .gitapi import GitAPI


class Statistic:

    config = {}

    def get_rate(self):

        API = GitAPI(repo_path=self.config['repo_path'])

        team = {'loc': 0, 'days': 0, 'efficiency': 0}

        # Get list of authors
        authors = {item: {'loc': 0, 'days': 0, 'contribution': 0, 'efficiency': 0} for item in API.get_authors()}
        # Get list of files, exclude ignored files
        files = API.get_files()
        if self.config['ignore_pathes']:
            for ignore in self.config['ignore_pathes']:
                files = set(files) - set([file for file in files if fnmatch.fnmatchcase(file, ignore)])
        files = sorted(files)

        # Get working days for every author
        result = API.get_working_days(format="%ad %an")
        for author_name in authors:
            authors[author_name]['days'] = len([item for item in result if author_name in item])

        # Get total working days
        team['days'] = len(API.get_working_days())

        # Exclude authors that worked less then config['min_days']
        authors = {author_name: author for author_name, author in authors.iteritems()
                                       if author['days'] >= self.config['min_days']}

        # Get author for every line in every file, add this to author statistic
        # Get total LOC
        for file in files:
            result = API.get_loc_per_author(file)
            for item in result:
                item = item.strip()
                delimiter = item.find(' ')
                loc  = item[:delimiter]
                author = item[delimiter+1:]
                if author in authors:
                    authors[author]['loc'] += int(loc)
                team['loc'] += int(loc)

        # Exclude authors that created less LOC then config['min_loc']
        authors = {author_name: author for author_name, author in authors.iteritems()
                                       if author['loc'] >= self.config['min_loc']}

        # Calculate team's efficiency
        team['efficiency'] = (float(team['loc']) / team['days']) / team['loc']

        # Calculate authors' contribution
        for author_name in authors:
            authors[author_name]['contribution'] = (float(authors[author_name]['loc']) / team['loc'])

        # Calculate authors' potential_loc
        potential_loc = {}
        for author_name, author in authors.iteritems():
            potential_loc[author_name] = (float(author['loc']) / author['days']) * team['days']
        try:
            min_potential_loc = min([loc for name, loc in potential_loc.iteritems() if loc > 0])
        except ValueError:
            min_potential_loc = 0

        # Calculate authors' efficiency
        if min_potential_loc:
            for author_name in authors:
                authors[author_name]['efficiency'] = potential_loc[author_name] / min_potential_loc

        authors = OrderedDict(sorted(authors.items(), key=lambda x: x[1]['efficiency'], reverse=True))

        return {'team': team, 'authors': authors}

    def populate_config(self, form):
        self.config['repo_path'] = form['repo_path'].data
        self.config['ignore_pathes'] = form['ignore_pathes'].data.splitlines() if form['ignore_pathes'].data else []
        self.config['min_days'] = form['min_days'].data if form['min_days'].data else 0
        self.config['min_loc'] = form['min_loc'].data if form['min_loc'].data else 0
        self.config['anonym'] = True if form['anonym'].data else False
