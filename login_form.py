from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import InputRequired, Length
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # CSRF protection

class LoginForm(FlaskForm):
    name = StringField("Name of Student:", validators=[InputRequired(), Length(min=2, max=50)])
    role = RadioField("Role:", choices=[('c', 'Consumer'), ('s', 'Staff')], validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired(), Length(min=6)])
    email = StringField("Email:", validators=[InputRequired()])
    submit = SubmitField("Login")
