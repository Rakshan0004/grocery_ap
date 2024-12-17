from flask import Flask, json, request, jsonify
import products_dao, uom_dao
from sql_connection import get_sql_connection

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    products = uom_dao.get_uoms(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_products():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id,
        'message': 'Product added successfully'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/editProduct', methods=['POST'])
def edit_product_route():
    request_payload = json.loads(request.form['data'])
    # Validate that product_id is provided
    if 'product_id' not in request_payload or not request_payload['product_id']:
        return jsonify({
            'success': False,
            'message': 'Product ID is missing. Update cannot proceed.'
        }), 400

    rows_affected = products_dao.edit_product(connection, request_payload)
    if rows_affected > 0:
        response = jsonify({
            'success': True,
            'message': 'Product updated successfully.'
        })
    else:
        response = jsonify({
            'success': False,
            'message': 'Product not found or no changes made.'
        })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



if __name__ == "__main__":
    print("Starting python flask server For Grocery Store Management System")
    app.run(port=5000)
