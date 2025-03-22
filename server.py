from flask import Flask, render_template, url_for, redirect, request, session, abort
from login_form import LoginForm
from signup_form import SignupForm
import os
import json
from dotenv import load_dotenv  

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

def get_file(file):
    with open(file, 'r') as whole_file:
        file_content = json.load(whole_file)
    return file_content  # Return the loaded JSON data

def check_login(email, password):
    users = get_file('./data/user.json')
   
    for user in users:
        print(user)
        if user["email"] == email and user["password"] == password :
            return user
        

def add_user(email, role, password):
    users = get_file('./data/user.json')  # Load existing users

    new_user = {
        "email": email,
        "password": password,
        "role": role
    }

    users.append(new_user)  # Add new user to the list

    # Correct indentation for writing back to the file
    with open('./data/user.json', 'w') as json_file:
        json.dump(users, json_file, indent=4)  # Write the entire updated list

    
@app.route('/login', methods =['GET', 'POST'])
def login():
    # if not session.get('username') and session.get('username'):
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():  # Check if the form is submitted and valid
            username = form.name.data  # Access the name field from the form
            password = form.password.data  # Access the password field from the form
            email = form.email.data  # Access the email field from the form
            role = form.role.data
            
            user_found=check_login(email, password)

            if user_found :
                session['username'] = username
                session['role'] = role
            else:
                return render_template('login.html', form=form)


        
            



if __name__ == '__main__':
    app.run(port=6005, debug=True)
    app.run(port=(os.getenv('FLASK_RUN_PORT')), host=os.getenv('FLASK_RUN_HOST'))