import sqlite3 as sql
import json

def listExtension():
  con = sql.connect("database/data_source.db")
  cur = con.cursor()
  data = cur.execute('SELECT * FROM extension').fetchall()
  con.close()
  return data

def credentials(username, password):
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM StudentCredentials WHERE email = ? AND password = ?', (username, password))
    studentRow = cur.fetchone()
    if studentRow == None:
        cur.execute('SELECT *FROM StaffCredentials where email = ? AND password = ?', (username, password))
        staffRow = cur.fetchone()
        if staffRow == None:
            con.close()
            return 'None', None
        else:
            con.close()
            return 'StaffCredentials', staffRow[2]
    else:
        con.close()
        return 'StudentCredentials', studentRow[2]
    
    
def getFoodData():
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    data = cur.execute("SELECT * FROM FoodItems WHERE Special = 'Not special' AND Classification = 'Meal'").fetchall()
    con.close()
    return data

def getDrinkData():
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    data = cur.execute("SELECT * FROM FoodItems WHERE Classification = 'Drink'").fetchall()
    con.close()
    return data

def getSpecialsData():
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    data = cur.execute("SELECT * FROM FoodItems WHERE Special = 'Special' AND Classification = 'Meal'").fetchall()
    con.close()
    return data

def getFoodByName(name):
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM FoodItems WHERE name = ?', (name,))
    food = cur.fetchone()
    con.close()
    return food

def addOrder(user_name, food_name, price, description, image, status, quantity):
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    # Insert a new row for each order
    cur.execute(
        "INSERT INTO orders (user, items, price, description, image, status, amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_name, food_name, price, description, image, status, quantity)
    )
    con.commit()
    con.close()

def getCart(user):
    con = sql.connect('database/data_source.db')
    cur=con.cursor()
    data = cur.execute(
        "SELECT * FROM orders WHERE user = ?", (user,)
    )
    data = cur.fetchall()
    con.close()
    return data

def getAllOrders():
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    data = cur.execute("SELECT * FROM orders where status = 'checked out'").fetchall()
    con.close()
    return data

def checkinOrders(user):
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    cur.execute("UPDATE orders SET status = 'checked out' WHERE user = ?", (user,))
    con.commit()
    con.close()
    
def removeOrder(order_id):
    con = sql.connect('database/data_source.db')
    cur = con.cursor()
    cur.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    con.commit()
    con.close()