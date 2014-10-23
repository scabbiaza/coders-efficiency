import os

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError

from .gitapi import GitAPI


def repo_path_validate(form, field):
    repo_path = field.data
    if not os.path.isdir(repo_path):
        raise ValidationError('Absolute path to the repository is not exist')
    API = GitAPI(repo_path)
    if not API.is_repo():
        raise ValidationError('There is not GIT repo in {}'.format(repo_path))


def ignore_pathes_validate(form, field):
    repo_path = form.repo_path.data
    ignore_pathes = field.data.splitlines()
    if not ignore_pathes:
        return
    for path in ignore_pathes:
        if path[0] == '/':
            raise ValidationError('Path %s is not relative' % path)


def min_days_validate(form, field):
    min_days = field.data
    if min_days < 0:
        raise ValidationError('Minimal working days value should be more then zero')


def min_loc_validate(form, field):
    min_loc = field.data
    if min_loc < 0:
        raise ValidationError('Minimal LOC value should be more then zero')


class ConfigForm(Form):
    repo_path = StringField('Absolute path to the repository', [DataRequired('Field is required'), repo_path_validate])
    ignore_pathes = TextAreaField('List of ignored folders and files', [ignore_pathes_validate])
    min_days = IntegerField('Minimal working days', [Optional(), min_days_validate])
    min_loc = IntegerField('Minimal LOC', [Optional(), min_loc_validate])
    anonym = BooleanField('Anonym mode')
    submit = SubmitField('Get Rate')
