from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # CSRF protection

class SignupForm(FlaskForm):
    email = StringField("Email", 
                        validators=[InputRequired(message="Email is required."), 
                                    Email(message="Invalid email address.")])

    password = PasswordField("Password", 
                             validators=[InputRequired(message="Password is required."), 
                                         Length(min=6, message="Password must be at least 6 characters long.")])

    confirm_password = PasswordField("Confirm Password", 
                                     validators=[InputRequired(message="Please confirm your password."), 
                                                 EqualTo('password', message="Passwords must match.")])

    role = RadioField("Role", choices=[('staff', 'Staff'), ('customer', 'Customer')], 
                      validators=[InputRequired(message="Please select a role.")])

    submit = SubmitField("Create Account")
