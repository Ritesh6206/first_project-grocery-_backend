'''from flask import Flask, jsonify, request
from products_dao import get_all_products, insert_new_product, delete_product, update_product
import mysql.connector
from sql_connection import get_sql_connection
import products_dao

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():


    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
   

@app.route('/createProduct', methods=['POST'])
def create_product():
    connection = get_sql_connection()
    product_id = insert_new_product(connection, request.get_json())
    connection.close()
    return jsonify({"product_id": product_id})

@app.route('/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product_endpoint(product_id):
    connection = get_sql_connection()
    result = delete_product(connection, product_id)
    connection.close()
    return jsonify({"deleted": result})

@app.route('/updateProduct/<int:product_id>', methods=['PUT'])
def update_product_endpoint(product_id):
    connection = get_sql_connection()
    result = update_product(connection, product_id, request.get_json())
    connection.close()
    return jsonify({"updated": result})

if __name__ == "__main__":
    print("Starting the Flask server...")
    app.run(port=5000, debug=True)'''


from flask import Flask, jsonify, request, render_template

from products_dao import (
    get_all_products,
    insert_new_product,
    delete_product,
    update_product
)

from sql_connection import get_sql_connection


app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
            
            )


# ============================
# HOME PAGE
# ============================

@app.route('/')
def home():
    return render_template('product_page.html')


# ============================
# GET ALL PRODUCTS
# ============================

@app.route('/getProducts', methods=['GET'])
def get_products():

    connection = get_sql_connection()

    try:
        products = get_all_products(connection)

        response = jsonify(products)
        response.headers.add(
            'Access-Control-Allow-Origin',
            '*'
        )

        return response

    finally:
        connection.close()


# ============================
# CREATE PRODUCT
# ============================

@app.route('/createProduct', methods=['POST'])
def create_product():

    connection = get_sql_connection()

    try:

        product = request.get_json()

        product_id = insert_new_product(
            connection,
            product
        )

        return jsonify({
            "product_id": product_id
        })

    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 400

    finally:
        connection.close()


# ============================
# DELETE PRODUCT
# ============================

@app.route(
    '/deleteProduct/<int:product_id>',
    methods=['DELETE']
)
def delete_product_endpoint(product_id):

    connection = get_sql_connection()

    try:

        result = delete_product(
            connection,
            product_id
        )

        return jsonify({
            "deleted": result
        })

    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 400

    finally:
        connection.close()


# ============================
# UPDATE PRODUCT
# ============================

@app.route(
    '/updateProduct/<int:product_id>',
    methods=['PUT']
)
def update_product_endpoint(product_id):

    connection = get_sql_connection()

    try:

        product = request.get_json()

        result = update_product(
            connection,
            product_id,
            product
        )

        return jsonify({
            "updated": result
        })

    except Exception as e:

        connection.rollback()

        return jsonify({
            "error": str(e)
        }), 400

    finally:
        connection.close()







# ============================
# START SERVER
# ============================

if __name__ == "__main__":

    print("Starting the Flask server...")

    app.run(
        port=5000,
        debug=True
    )