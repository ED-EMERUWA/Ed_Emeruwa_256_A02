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



@app.route('/create', methods =['GET', 'POST'])
def create():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            role = form.role.data
            print(email)

            add_user(email,role,password)
            return redirect(url_for('success'))  

# change to actual home page
@app.route('/success')
def success():
    return "<h1>Account Created Successfully!</h1>"
            
@app.route('/logout')
def logout():
     session.remove('username') 
     session.remove('role')

@app.route('/orders')
def pizza_orders():
    """Fetches orders, processes them, and passes data to template"""
    orders_data = get_file('./data/pizzaorders.json')  # Load JSON data
    orders_list = []  # Store processed orders

    for order in orders_data:
        order_info = {
            "type": order["type"],
            "crust": order["crust"],
            "size": order["size"],
            "quantity": int(order["quantity"]),
            "price_per": float(order["price_per"]),
            "order_date": order["order_date"],
            "subtotal": float(order["price_per"]) * int(order["quantity"]),
        }
        order_info["delivery_charge"] = order_info["subtotal"] * 0.1  # 10% delivery charge
        order_info["total"] = order_info["subtotal"] * 1.1  # Total = subtotal + 10%

        orders_list.append(order_info)  # Add to list

    return render_template('pizza_orders.html', orders=orders_list)
        
            



if __name__ == '__main__':
    app.run(port=6005, debug=True)
    app.run(port=(os.getenv('FLASK_RUN_PORT')), host=os.getenv('FLASK_RUN_HOST'))