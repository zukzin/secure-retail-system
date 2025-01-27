import auth
import database
from logger import log_action
from security import check_brute_force, track_failed_attempt

def main():
    print("Welcome to the Secure Retail System CLI")
    while True:
        # Menu handling options
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Verify OTP & Get Token")
        print("4. Add Product (Admin Only)")
        print("5. View Products")
        print("6. Exit")

        # Get user choice
        choice = input("Enter your choice: ")

        # Handle each menu option
        if choice == "1": # Register a user
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (admin/customer): ")
            email = input("Enter Email for MFA: ")
            result = auth.register(username, password, role, email)
            print(result)

        elif choice == "2": # Login
            username = input("Enter username: ")

            # Check brute force prevention
            brute_force_msg = check_brute_force(username)
            if brute_force_msg:
                print(brute_force_msg)
                continue

            password = input("Enter password: ")
            result = auth.login(username, password)
            print(result)

            if "OTP sent successfully" in result:
                log_action("Login initiated", username)
            else:
                track_failed_attempt(username)

        elif choice == "3": # Verify OTP
            username = input("Enter username: ")
            otp = input("Enter the OTP received: ")
            result = auth.verify_otp(username, otp)
            print(result)
            if "Login successful" in result:
                log_action("Logged in successfully", username)

        elif choice == "4": # Add product (Admin only)
            username = input("Enter admin username: ")
            token = input("token: ")
            role = auth.authenticate(token)
            if role != "admin":
                print("Unauthorized Only admins can add products.")
                continue

            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            stock = int(input("Enter stock count: "))
            result = database.add_product(product_id, name, price, stock)
            print(result)
            log_action("Added product", username)

        elif choice == "5": # View products
            products = database.view_products()
            if isinstance(products, dict):
                for product_id, details in products.items():
                    print(f"ID: {product_id}, Name: {details['name']}, Price: {details['price']}, Stock: {details['stock']}")
            else:
                print(products)

        elif choice == "6": # Exit the application
            print("Exiting CLI. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

    if __name__ == "__main__":
        main()

