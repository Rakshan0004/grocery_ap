from flask import Flask, json, request, jsonify
import products_dao, uom_dao, order_dao
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

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = order_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id,
        'message': 'Order added successfully'
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

@app.route('/editProduct', methods=['PUT'])
def edit_product():
    try:
        # Parse request payload
        request_payload = request.json
        product_id = request_payload.get('product_id')
        name = request_payload.get('name')
        uom_id = request_payload.get('uom_id')
        price_per_unit = request_payload.get('price_per_unit')
        # Check if all fields are provided
        if not all([product_id, name, uom_id, price_per_unit]):
            return jsonify({"error": "Missing required fields"}), 400
        # Call DAO to update product
        rows_affected = products_dao.edit_product(connection, request_payload)
        if rows_affected > 0:
            return jsonify({"message": "Product updated successfully"}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    print("Starting python flask server For Grocery Store Management System")
    app.run(port=5000)
