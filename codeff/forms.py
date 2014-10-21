from flask.ext.wtf import Form

from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional


class ConfigurationsForm(Form):
    repo_path = StringField('Absolute path to the repository', [DataRequired('Field is required')])
    ignore = TextAreaField('List of ignored folders and files')
    min_days = IntegerField('Minimal working days', [Optional()])
    min_loc = IntegerField('Minimal LOC', [Optional()])
    anonym = BooleanField('Anonym mode')
    submit = SubmitField('Get Rate')
