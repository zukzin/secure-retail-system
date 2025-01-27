from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import reqparse
from database import add_product, view_products, update_product, delete_product
from auth import register, login, verify_otp

# Flask app setup
app = Flask(__name__)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["100 per hour"])

# Input parser for validation
parser = reqparse.RequestParser()
parser.add_argument("id", type=str, required=True, help="Product ID is required.")
parser.add_argument("name", type=str, required=True, help="Product name is required.")
parser.add_argument("price", type=float, required=True, help="Product price is required.")
parser.add_argument("stock", type=int, required=True, help="Product stock is required.")

# Defines root route
@app.route('/')
def hello():
    return jsonify({
        "message": "Welcome to the Secure Retail System API",
        "endpoints": [
            {"GET /products": "View all products"},
            {"POST /products": "Add a new product (requires authentication)"},
            {"PUT /products/<id>": "Update a product (requires authentication)"},
            {"DELETE /products/<id>": "Delete a product (requires authentication)"}
        ]
    }), 200

# Authenticate routes
@app.route('/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "customer")
    email = data.get("email")
    result = register(username, password, role, email)
    return jsonify({"message": result}), 200

# Defines routes for login
@app.route('/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    result = login(username, password)
    if "OTP sent successfully" in result:
        return jsonify({"message": result}), 200
    return jsonify({"error": result}), 401

# Defines routes for verifying OTP
@app.route('/verify_otp', methods=['POST'])
def api_verify_otp():
    data = request.json
    username = data.get("username")
    otp = data.get("otp")
    result = verify_otp(username, otp)
    if "Login successful" in result:
        return jsonify({"message": result}), 200
    return jsonify({"error": result}), 401

# Define product routes
@app.route('/products', methods=['GET'])
@limiter.limit("10 per minute")
def get_products():
    return jsonify(view_products()), 200

@app.route('/products', methods=['POST'])
def create_product():
    args = parser.parse_args()
    return jsonify(add_product(args["id"], args["name"], args["price"], args["stock"])), 201

@app.route('/products/<product_id>', methods=['PUT'])
def modify_product(product_id):
    data = request.json
    return jsonify(update_product(product_id, data.get("name"), data.get("price"), data.get("stock"))), 200

@app.route('/products/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    return jsonify(delete_product(product_id)), 200

if __name__ == '__main__':
    app.run(debug=True)
