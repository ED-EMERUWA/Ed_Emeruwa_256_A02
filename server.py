from flask import Flask, render_template, url_for, redirect, request, session, abort, jsonify
import json
from login_form import LoginForm
from signup_form import SignupForm
from order_form import PizzaOrderForm
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
            username = form.name.data  
            password = form.password.data 
            email = form.email.data  
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

@app.route('/')
def pizza_orders():
    """Fetches orders, processes them, and passes data to template"""
    orders_data = get_file('./data/pizzaorders.json')  
    orders_list = []  

    for order in orders_data:
        order_info = {
            "id": order["id"],
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
        
@app.route('/pizza', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pizza():
    form = PizzaOrderForm()
    if request.method == 'GET':
        if request.args.get('order_id'):
            
            order_id = int(request.args.get('order_id'))
            orders = get_file('./data/pizzaorders.json')  

            for order in orders:
                if order_id == order["id"]:
                    return render_template('edit_order.html', order = order, form =form)
                    
        else: 
            return render_template('order_form.html', form = form)  
    elif request.method == 'PUT':       
         try:
            # Load existing orders
            with open('./data/pizzaorders.json', 'r') as file:
                orders = json.load(file)

            # Get updated order data from the request
            updated_order = request.get_json()
            order_id = int(updated_order["id"])

            # Find and update the order
            for order in orders:
                if order["id"] == order_id:
                    order.update(updated_order)
                    break  

            # Save updated orders back to file
            with open('./data/pizzaorders.json', 'w') as file:
                json.dump(orders, file, indent=4)

            return jsonify({"message": "Order updated successfully!"}), 200

         except Exception as e:
             return jsonify({"error": str(e)}), 500
    elif request.method == 'DELETE':  
        try:
            del_order = request.get_json()
            del_order_id = int(del_order["id"])

            
            with open('./data/pizzaorders.json', 'r') as file:
                orders = json.load(file)

            # Compresssion
            orders = [order for order in orders if order["id"] != del_order_id]

            
            with open('./data/pizzaorders.json', 'w') as file:
                json.dump(orders, file, indent=4)

            return redirect(url_for('pizza_orders'))

        except Exception as e:
            return {"error": str(e)}, 500

    if request.method == 'POST':
     if form.validate_on_submit():
         orders = get_file('./data/pizzaorders.json')
         order_id = len(orders) + 1  # Generate a new order ID

         new_order = {
             "id": order_id,
             "type": form.type.data,
             "crust": form.crust.data,
             "size": form.size.data,
             "quantity": form.quantity.data,
             "price_per": 75.5,
             "order_date" : str(form.order_date.data)
             }



         orders.append(new_order)
         with open('./data/pizzaorders.json', 'w') as file:
             json.dump( orders, file, indent=4)

         return redirect(url_for('pizza_orders'))  
     return render_template('order_form.html', form=form)           

@app.route('/confirm', methods =['GET'])
def delete():
    if request.method == 'GET':
        if request.args.get('order_id'):
                orders =get_file('./data/pizzaorders.json')

                del_order_id = int(request.args.get('order_id'))

              

                for order in orders:
                    if order['id'] == del_order_id :
                        return render_template('confirm_delete.html', order = order)
    

if __name__ == '__main__':
    app.run(port=6005, debug=True)
    app.run(port=(os.getenv('FLASK_RUN_PORT')), host=os.getenv('FLASK_RUN_HOST'))