from database import *
import random
import os
import re
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)
 
host = 'localhost'
root = 'root'
password = open('database\password', 'r').readline()
databse_name = 'project2'
db = Database(host,root,password,databse_name)
connection = db.create_server_connection()

# generate ID in given length
def ID_generator(length):
    result=''
    for i in range(length):
        result += f'{random.randint(0,9)}'
    return result
def addItem(id, name, description,type, image_path):
    args = (int(id), name, description,type, image_path)
    query = 'INSERT INTO projectTwo VALUES(%s, %s, %s, %s, %s)'
    db.execute_query(connection, query, args)
def deleteItem(id):
    query = f'DELETE FROM projectTwo where ID={id};'
    db.execute_query(connection, query, None)
def updateItem(id, name, description,category, imagePath):
    query = f'''UPDATE projectTwo 
                SET name='{name}', description='{description}', category='{category}', image_path='{imagePath}'
                WHERE ID={id};'''
    db.execute_query(connection, query, None)
def getAllItems():
    return db.read_query(connection, 'select * from projectTwo;')
def getItemById(id):
    return db.read_query(connection, f'SELECT * from projectTwo where ID ={id};')
def searchItem(value):
    query = f'''
            SELECT * FROM projectTwo
            WHERE name LIKE '%{value}%'
            OR category LIKE '%{value}%';'''
    return db.read_query(connection, query)
def checkAllDigit(str):
    nonDigit = re.compile(r"[^0-9]")
    return bool(nonDigit.search(str))
    

class Products():
    def __init__(self, products):
        self.products = products
    def getProducts(self):
        return self.products
    def setProducts(self, products):
        self.products = products
# Product class
list_product = Products(None)

@app.route('/index')
def index():
    if(list_product.getProducts() == None): 
        list_product.setProducts(getAllItems())
    products = list_product.getProducts()
    sortBy = ['ID', 'Name']
    return render_template('index.html', products = products, sortBy = sortBy)

@app.route('/refresh', methods=['POST', 'GET'])
def refresh():
    list_product.setProducts(None)
    return redirect('/index')
# Handle adding items
@app.route('/add_item')
def add_item():
    return render_template('add_item.html')
@app.route('/add', methods=['POST'])
def item():
    id = ID_generator(9)
    name = request.form.get("name")
    description = request.form.get("description")
    category = request.form.get("category")
    image = request.files['imageFile']
    image.filename = f'database\static\images\{id}.png'
    image.save(image.filename)
    file_path = f'images/{id}.png'
    addItem(id, name, description, category, file_path)
    list_product.setProducts(None)
    return redirect('/index')
# Handle Deleting Items
@app.route('/delete/<id>')
def delete(id):
    deleteItem(int(id))
    os.remove(f'database\static\images\{id}.png')
    list_product.setProducts(None)
    return redirect('/index')
# Handle Updating items
@app.route('/update/<id>', methods=['POST'])
def update(id):
    name = request.form.get("name")
    description = request.form.get("description")
    category = request.form.get("category")
    image = request.files['imageFile']
    image.filename = f'database\static\images\{id}.png'
    image.save(image.filename)
    file_path = f'images/{id}.png'
    updateItem(int(id), name, description, category, file_path)
    list_product.setProducts(None)
    return redirect('/index')
# display item
@app.route('/view/<id>')
def display(id):
    items = getItemById(int(id))
    return render_template('view.html', items=items)
# Handle search
@app.route('/search', methods=['POST', 'GET'])
def search():
    value = request.form.get("searchID")
    if checkAllDigit(value): products = searchItem(value)
    else: products = getItemById(int(value))
    list_product.setProducts(products)
    return redirect('/index')
# Handle sorting
@app.route('/sorting', methods=['POST', 'GET'])
def sort():
    sortBy = request.form.get('sortBy')
    products = list_product.getProducts()
    if sortBy == 'ID': sorted_List = sorted(products, key=lambda x: x[0])
    elif sortBy == 'Name': sorted_List = sorted(products, key=lambda x: x[1])
    else: sorted_List = products
    list_product.setProducts(sorted_List)
    return redirect('/index')





# @app.route('/templates')
# def display():
#     items = getAllItems()
#     print(items)
#     connection.close()
#     return render_template('home.html', items = items)

# @app.route('/success/<name>')
# def success(name):
#     return 'welcome %s' % name
# @app.route('/display/')


# @app.route('/search/<id>')
# def searchById(id):
#     lst = getItemById(id)
#     return render_template('templates\home.html', items=lst)
 
# @app.route('/index', methods=['POST', 'GET'])
# def main():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('searchById', id=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('searchById', id=user))

if __name__ == '__main__':
    app.run(debug=True)