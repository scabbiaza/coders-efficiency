# -*- coding: utf-8 -*-

# Algorithm
#
# 1. Get list of authors:
#    git log --format='%aN' | sort -u
#
# 2. Get list of not ignored files
#    git ls-files
#
# 3. Get working days for every author (any day that has commits – is working day):
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
# 7. Calculate team's efficiency as:
#    (total LOC / total working days) / total LOC => percent of the code created per day
#
# 8. Calculate authors' contribution and efficiency as:
#    contribution = author LOC / total LOC
#    efficiency = (author LOC * total working days) / author workink days


import os
import subprocess

from collections import OrderedDict


conf = {
    'repo_path': None,
}


def execute_in_shell(cmd, cwd=conf['repo_path']):
    result = []
    if cwd:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=cwd)
    else:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        result.append(line.rstrip(os.linesep))  # decode("utf-8").
    p.wait()
    return result


def get_authors_stat():
    team = {'loc': 0, 'days': 0, 'efficiency': 0}

    # Get list of authors
    result = execute_in_shell("git log --format='%aN' | sort -u")
    authors = {item: {'loc': 0, 'days': 0, 'contribution': 0, 'efficiency': 0} for item in result}

    # Get list of not ignored files
    files = execute_in_shell("git ls-files")

    # Get working days for every author
    # Get total working days
    result = execute_in_shell("git log --date=short --pretty=\"format:%ad %an\" | uniq")
    for author_name in authors:
        authors[author_name]['days'] = len([item for item in result if author_name in item])
    result = execute_in_shell("git log --date=short --pretty=\"format:%ad\" | uniq")
    team['days'] = len(result)

    # Get author for every line in every file, add this to author statistic
    # Get total LOC
    for file in files:
        result = execute_in_shell("git blame --line-porcelain {} | sed -n 's/^author //p' | sort | uniq -c | sort -rn".format(file))
        for item in result:
            loc, author = item.strip().split(' ')[:2]
            if author in authors:
                authors[author]['loc'] += int(loc)
            team['loc'] += int(loc)

    # Calculate team's efficiency
    team['efficiency'] = (float(team['loc']) / team['days']) / team['loc']

    # Calculate authors' stat
    for author_name in authors:
        authors[author_name]['contribution'] = (float(authors[author_name]['loc']) / team['loc'])

    potential_loc = {}
    for author_name in authors:
        potential_loc[author_name] = float(authors[author_name]['loc']) * team['days']
    try:
        min_potential_loc =min([loc for name, loc in potential_loc.iteritems() if loc > 0])
    except ValueError:
        min_potential_loc = 0

    if min_potential_loc:
        for author_name in authors:
            authors[author_name]['efficiency'] = potential_loc[author_name] / min_potential_loc

    authors = OrderedDict(sorted(authors.items(), key=lambda x: x[1]['efficiency']))

    return team, authors


if __name__ == '__main__':
    team, authors = get_authors_stat()
    print('team: ', team)
    print('')
    for author_name in authors:
        print(author_name)
        print(authors[author_name])
