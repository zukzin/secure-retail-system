import json
from security import sanitize_inputs

# File paths for product and order storage
PRODUCT_DB_FILE = "src/products.json"
ORDER_DB_FILE = "src/orders.json"

# Helper function to load data from a JSON file
def load_data(file_path):
    """
    Loads data from a JSON file. If the file does not exist, returns and empty dictionary.
    Args:
        file_path (str): Path to the JSON file.
    Returns:
        dict: Data from the file or an empty dictionary.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Helper function to save data to a JSON file
def save_data(file_path, data):
    """
    Saves data to a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        data (dict): Data to be saved.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# CREATE: Add a new product
def add_product(product_id, name, price, stock):
    """
        Adds a new product to the product database.
    Args:
        product_id (str): Unique identifier for the product.
        name (str): Name of the product.
        price (float): Price of the product.
        stock (int): Stock quantity of the product
    Returns:
        str: Success or error message.
    """
    products = load_data(PRODUCT_DB_FILE)

    if product_id in products:
        return  "Product ID already exists!"

    if not sanitize_inputs(name):
        return "Invalid product name detected!"

    # Add the new product to the dictionary
    products[product_id] = {
        "name": name,
        "price": price,
        "stock": stock
    }

    # Save the updated product list
    save_data(PRODUCT_DB_FILE, products)
    return "Product added successfully!"

# Read: View all products
def view_products():
    """
    Retrieves all products from the product database.
    Returns:
        dict or str: Dictionary of products or an error message if empty.
    """
    products = load_data(PRODUCT_DB_FILE)
    return  products if products else  "No products available."

# UPDATE: Modify an existing product
def update_product(product_id, name=None, price=None, stock=None):
    """
    Updates an existing product in the product database.
    Args:
        product_id(str): Unique identifier for the product.
        name (str, optional): New name for the product.
        price (float, optional): New price for the product.
        stock (int, optional): New stock quantity for the product.
    Returns:
        str: Success or error message.
    """
    products = load_data(PRODUCT_DB_FILE)

    if product_id not in products:
        return "Product not found!"

    if name and sanitize_inputs(name):
        products[product_id]["name"] = name
    if price is not None:
        products[product_id]["price"] = price
    if stock is not None:
        products[product_id]["stock"] = stock

    save_data(PRODUCT_DB_FILE, products)
    return "Products updated successfully!"

# DELETE: Remove a product
def delete_product(product_id):
    """
    Deletes a product from the product database.
    Args:
        product_id (str): Unique identifier for the product.
    Returns:
        str: Success or error message.
    """
    products = load_data(PRODUCT_DB_FILE)

    if product_id not in products:
        return "Product not found!"

    del products[product_id]
    save_data(PRODUCT_DB_FILE, products)
    return "Product deleted successfully!"

