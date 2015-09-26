from flask_wtf import Form
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class NewsitemForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    active = BooleanField("Show to Actives")
    pledge = BooleanField("Show to Pledges")
    everyone = BooleanField("Show to Everyone")
    submit = SubmitField("Post News")