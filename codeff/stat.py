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
# 7. Calculate team's efficiency (part of the code created per day):
#    (total LOC / total working days) / total LOC
#
# 8. Calculate authors' contribution and efficiency as:
#    contribution = author LOC / total LOC (part of the code created by author)
#    potential LOC = author LOC per day * total working days
#    efficiency in team = potential LOC / min potential LOC


import os
import re
import subprocess
import fnmatch

from collections import OrderedDict


def execute_in_shell(cmd, cwd=None):
    result = []
    if cwd:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=cwd)
    else:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        result.append(line.rstrip(os.linesep))  # decode("utf-8").
    p.wait()
    return result


def get_authors_stat(conf):

    team = {'loc': 0, 'days': 0, 'efficiency': 0}

    # Check if folder is under git
    result = execute_in_shell("find .git", cwd=conf['repo_path'])
    if 'No such file or directory' in result:
        exit('Folder is not under Git VCS')

    # Get list of authors
    result = execute_in_shell("git log --format='%aN' | sort -u", cwd=conf['repo_path'])
    authors = {item: {'loc': 0, 'days': 0, 'contribution': 0, 'efficiency': 0} for item in result}

    # Get list of files (except excluded from .gitignore)
    files = execute_in_shell("git ls-files", cwd=conf['repo_path'])

    if conf['ignore']:
        for ignore in conf['ignore']:
            files = set(files) - set([file for file in files if fnmatch.fnmatchcase(file, ignore)])
    files = sorted(files)

    # Get working days for every author
    result = execute_in_shell("git log --date=short --pretty=\"format:%ad %an\" | sort | uniq", cwd=conf['repo_path'])
    for author_name in authors:
        authors[author_name]['days'] = len([item for item in result if author_name in item])

    # Get total working days
    result = execute_in_shell("git log --date=short --pretty=\"format:%ad\" | sort | uniq", cwd=conf['repo_path'])
    team['days'] = len(result)

    # Exclude authors that worked less then conf['min_days']
    authors = {author_name: author for author_name, author in authors.iteritems()
                                   if author['days'] >= conf['min_days']}

    # Get author for every line in every file, add this to author statistic
    # Get total LOC
    for file in files:
        result = execute_in_shell("git blame --line-porcelain {} | sed -n 's/^author //p' | sort | uniq -c | sort -rn".format(file), cwd=conf['repo_path'])
        for item in result:
            loc, author = item.strip().split(' ')[:2]
            if author in authors:
                authors[author]['loc'] += int(loc)
            team['loc'] += int(loc)

    # Exclude authors that created loc less then conf['min_loc']
    authors = {author_name: author for author_name, author in authors.iteritems()
                                   if author['loc'] >= conf['min_loc']}

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

    if min_potential_loc:
        for author_name in authors:
            authors[author_name]['efficiency'] = potential_loc[author_name] / min_potential_loc

    authors = OrderedDict(sorted(authors.items(), key=lambda x: x[1]['efficiency'], reverse=True))

    return team, authors


# def translate(shell_regex):
#     table = {
#         '?': '.',
#         '*': '[\w^/]+',
#         '**': '[\w]+',
#     }
#     for k, v in table.iteritems():
#         shell_regex = shell_regex.replace(k, v)
#     return shell_regex
