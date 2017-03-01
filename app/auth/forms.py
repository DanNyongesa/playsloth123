from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField
fields = ['username', 'email', 'password']

class UserForm(Form):
    pass
