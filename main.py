from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import jsonify
from flask import redirect
import database_manager as dbHandler
import random


app = Flask(__name__)
app.secret_key = 'kelvinisnice1'

@app.route('/Login.html', methods=['POST','GET'])
@app.route('/', methods=['POST', 'GET'])
def login():
  if request.method == 'GET':
    return render_template('Login.html')
  elif request.method == 'POST':
    username = request.form['email']
    password = request.form['password']
    category, name = dbHandler.credentials(username, password)
    if category == 'StudentCredentials':
      session['username'] = username
      session['password'] = password
      session['name'] = name
      print("Login successful")
      return render_template('/Home.html')
    elif category == 'StaffCredentials':
      data = dbHandler.getAllOrders()
      print('Login successful')
      return render_template('/staff.html', orders = data)
    else:
      return render_template('Login.html')

@app.route('/Home.html')
def home():
  FoodData = dbHandler.getFoodData()
  return render_template('Home.html', FoodData=FoodData)

@app.route('/Food.html')
def FoodMenu():
  FoodData = dbHandler.getFoodData()
  SpecialsData = dbHandler.getSpecialsData()
  DrinksData = dbHandler.getDrinkData()
  return render_template('Food.html', FoodData=FoodData, SpecialsData=SpecialsData, DrinksData = DrinksData)
  
@app.route('/cart.html')
def cart():
  user = session['username']
  data = dbHandler.getCart(user)
  return render_template('cart.html', orders = data)

# In your Flask app (main.py)
@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    data = request.json
    food_name = data.get('food_name')
    price = data.get('price')
    description = data.get('description')
    image = data.get('image')
    user_name = session.get('username')
    quantity = data.get('quantity')
    if not session.get('username'):
      return jsonify({'success': False, 'error': 'Not logged in'}), 401
    status = 'not checked out'
    dbHandler.addOrder(user_name, food_name, price, description, image, status, quantity)
    return jsonify({'success': True})

@app.route('/staff.html')
def staff():
  return render_template('staff.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    user = session.get('username')
    if user:
        dbHandler.checkinOrders(user)
    used_numbers = set()
    def generate_unique_receipt_number(start, end):
      while True:
        number = random.randint(start, end)
        if number not in used_numbers:
          used_numbers.add(number)
          return number
        
    number = generate_unique_receipt_number(0, 500)
    user = session['username']
    data = dbHandler.getCart(user)
    return render_template('receipt.html', number = number, data = data)
  
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    order_id = request.form.get('order_id')
    if order_id:
        dbHandler.removeOrder(order_id)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '', 204  # No Content, for AJAX
    return redirect('/cart.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/Login.html')
  
  
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=10000)