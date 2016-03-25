from wtforms import StringField, TextAreaField, validators, PasswordField
from wtforms import Form


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=128)])
    password = PasswordField('Password', [validators.Length(min=1, max=128)])


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content')
