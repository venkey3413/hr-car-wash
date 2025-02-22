import datetime
import mysql.connector
from mysql.connector import Error

# Define car wash prices
CAR_WASH_PRICES = {
    "SUV": 700,
    "XUV": 600,
    "Sedan": 500
}

# Database configuration
DB_CONFIG = {
    'host': 'localhost',  # Replace with your MySQL host
    'database': 'car_wash_db',  # Replace with your database name
    'user': 'root',  # Replace with your MySQL username
    'password': 'password'  # Replace with your MySQL password
}

# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create the car_wash_orders table
def create_table():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                CREATE TABLE IF NOT EXISTS car_wash_orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_name VARCHAR(255) NOT NULL,
                    customer_number VARCHAR(15) NOT NULL,
                    car_model VARCHAR(50) NOT NULL,
                    car_number VARCHAR(20) NOT NULL,
                    car_year INT NOT NULL,
                    wash_type VARCHAR(50) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            cursor.execute(query)
            connection.commit()
            print("Table created successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to insert data into the database
def insert_data(customer_name, customer_number, car_model, car_number, car_year, wash_type, price):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO car_wash_orders 
                (customer_name, customer_number, car_model, car_number, car_year, wash_type, price) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (customer_name, customer_number, car_model, car_number, car_year, wash_type, price)
            cursor.execute(query, values)
            connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to generate receipt
def generate_receipt(customer_name, customer_number, car_model, car_number, car_year, wash_type, price):
    # Create receipt content
    receipt_header = "HR Waterwash\n"
    receipt_header += "-------------------------\n"
    receipt_content = f"Customer Name: {customer_name}\n"
    receipt_content += f"Customer Number: {customer_number}\n"
    receipt_content += f"Car Model: {car_model}\n"
    receipt_content += f"Car Number: {car_number}\n"
    receipt_content += f"Car Year: {car_year}\n"
    receipt_content += f"Wash Type: {wash_type}\n"
    receipt_content += f"Price: ₹{price}\n"
    receipt_content += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    receipt_content += "-------------------------\n"
    receipt_content += "Thank you for choosing HR Waterwash!\n"

    # Combine header and content
    receipt = receipt_header + receipt_content

    # Save receipt to a file
    file_name = f"{customer_name}_receipt.txt"
    with open(file_name, "w") as file:
        file.write(receipt)
    
    print(f"Receipt generated and saved as {file_name}")

# Main function
def main():
    print("Welcome to HR Car Wash App!")
    
    # Create the table if it doesn't exist
    create_table()
    
    # Input customer details
    customer_name = input("Enter Customer Name: ")
    customer_number = input("Enter Customer Number: ")
    car_model = input("Enter Car Model (SUV/XUV/Sedan): ").strip().capitalize()
    car_number = input("Enter Car Number: ")
    car_year = input("Enter Car Year: ")
    
    # Validate car model
    if car_model not in CAR_WASH_PRICES:
        print("Invalid car model. Please choose from SUV, XUV, or Sedan.")
        return
    
    # Select wash type
    wash_type = input("Select Wash Type (Full Wash/Body Wash): ").strip().capitalize()
    if wash_type not in ["Full Wash", "Body Wash"]:
        print("Invalid wash type. Please choose Full Wash or Body Wash.")
        return
    
    # Calculate price
    price = CAR_WASH_PRICES[car_model]
    
    # Insert data into the database
    insert_data(customer_name, customer_number, car_model, car_number, car_year, wash_type, price)
    
    # Generate receipt
    generate_receipt(customer_name, customer_number, car_model, car_number, car_year, wash_type, price)

# Run the app
if __name__ == "__main__":
    main()
