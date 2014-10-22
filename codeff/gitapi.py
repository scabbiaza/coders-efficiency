import os
import re
import subprocess


class GitAPI:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def execute_in_shell(self, cmd, cwd=None):
        cwd = cwd if cwd else self.repo_path
        result = []
        if cwd:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=cwd)
        else:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            result.append(line.rstrip(os.linesep))  # decode("utf-8").
        p.wait()
        return result

    def is_repo(self):
        result = self.execute_in_shell("find .git")
        return False if 'No such file or directory' in result else True  # TODO: looks like a hack

    def get_authors(self):
        return self.execute_in_shell("git log --format='%aN' | sort -u")

    def get_files(self):
        return self.execute_in_shell("git ls-files")  # except excluded from .gitignore

    def get_working_days(self, format="%ad"):
        return self.execute_in_shell("git log --date=short --pretty=\"format:{}\" | sort | uniq".format(format))

    def get_loc_per_author(self, file):
        return self.execute_in_shell("git blame --line-porcelain {} | sed -n 's/^author //p' | sort | uniq -c | sort -rn".format(file))

# def translate(shell_regex):
#     table = {
#         '?': '.',
#         '*': '[\w^/]+',
#         '**': '[\w]+',
#     }
#     for k, v in table.iteritems():
#         shell_regex = shell_regex.replace(k, v)
#     return shell_regex
