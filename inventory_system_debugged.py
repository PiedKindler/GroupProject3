# This program utilizes the Inventory class to create an inventory system. 
# The user can add, remove, and search for items in the inventory, as well as keep track of inventory and sales.
# The program also keeps tracks of users and their respective logins, as well as purchasing associated with users.
# The program tracks inventory levels and generates a report when inventory levels are low, as well as develops purchase orders.

# Meet the team: Project Manager: Misty Mayfield, Front-end Developer: Diego Ansaldo,
# UI/UX Designer: Brionna Morris, Back-end Developer: Wayne Bell. 

# Importing the necessary modules
from tkinter import *
from datetime import datetime
from typing import List, Tuple 

# Creating the product class
class Product:
    def __init__(self, id: str, name: str, description: str, price: float, quantity: int):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Creating the inventory class
class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        # Add product to inventory
        self.products.append(product)

    def remove_product(self, product: Product):
        # Remove product from inventory
        self.products.remove(product)

    def update_product(self, product: Product):
        # Update product information in inventory
        for i in range(len(self.products)):
            if self.products[i].id == product.id:
                self.products[i] = product

# Creating the purchase class
class Purchase:
    def __init__(self):
        self.purchases = []

    def add_purchase(self, product: Product, quantity: int):
        # Add purchase to inventory
        purchase = (product, quantity, datetime.now())
        self.purchases.append(purchase)
        product.quantity += quantity

# Creating the sales class
class Sales:
    def __init__(self):
        self.sales = []

    def add_sale(self, product: Product, quantity: int):
        # Remove sale from inventory
        if product.quantity < quantity:
            raise ValueError("Not enough stock available")
        sale = (product, quantity, datetime.now())
        self.sales.append(sale)
        product.quantity -= quantity

# Creating the barcode scanner class
class BarcodeScanner:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def scan(self, barcode: str) -> Product:
        # Find product in inventory by barcode
        for product in self.inventory.products:
            if product.id == barcode:
                return product
        return None


# Creating the user class and user management class
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class UserManagement:
    def __init__(self):
        self.users = []

    def login(self, username: str, password: str) -> bool:
        # Authenticate user
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def add_user(self, user: User):
        # Add user to system
        self.users.append(user)

    def remove_user(self, username: str):
        # Remove user from system
        for i in range(len(self.users)):
            if self.users[i].username == username:
                del self.users[i]
                break

# Creating the reporting class
class Reporting:
    def __init__(self, inventory: Inventory, purchases: Purchase, sales: Sales):
        self.inventory = inventory
        self.purchases = purchases
        self.sales = sales

    def generate_report(self, start_date: datetime, end_date: datetime) -> Tuple[int, int, int, float]:
        # Generate report based on date range
        num_products = len(self.inventory.products)
        num_purchases = sum(1 for purchase in self.purchases.purchases if start_date <= purchase[2] <= end_date)
        num_sales = sum(1 for sale in self.sales.sales if start_date <= sale[2] <= end_date)
        revenue = sum(sale[0].price * sale[1] for sale in self.sales.sales if start_date <= sale[2] <= end_date)
        return (num_products, num_purchases, num_sales, revenue)

# Creating the inventory management GUI class
class InventoryManagementGUI:
    def __init__(self, inventory: Inventory, purchase: Purchase, sales: Sales, barcode_scanner: BarcodeScanner, user_management: UserManagement, reporting: Reporting):
        self.inventory = inventory
        self.purchase = purchase
        self.sales = sales
        self.barcode_scanner = barcode_scanner
        self.user_management = user_management
        self.reporting = reporting
        self.current_user = None

        # Creating the main window
        self.window = Tk()
        self.window.title("Inventory Management System")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        self.login_frame = Frame(self.window)
        self.login_frame.pack()

        self.login_label = Label(self.login_frame, text="Login")
        self.login_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = Label(self.login_frame, text="Username")
        self.username_label.grid(row=1, column=0, pady=10)

        self.username_entry = Entry(self.login_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=10)

        self.password_label = Label(self.login_frame, text="Password")
        self.password_label.grid(row=2, column=0, pady=10)

        self.password_entry = Entry(self.login_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)

        self.login_button = Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.window.mainloop()

 # Creating the login function
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_management.login(username, password):
            self.current_user = username
            self.login_frame.destroy()
            self.main_menu()

# Creating the main menu function
    def main_menu(self):
        self.main_menu_frame = Frame(self.window)
        self.main_menu_frame.pack()

        self.main_menu_label = Label(self.main_menu_frame, text="Main Menu")
        self.main_menu_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.add_product_button = Button(self.main_menu_frame, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=1, column=0, pady=10)

        self.remove_product_button = Button(self.main_menu_frame, text="Remove Product", command=self.remove_product)
        self.remove_product_button.grid(row=1, column=1, pady=10)

        self.update_product_button = Button(self.main_menu_frame, text="Update Product", command=self.update_product)
        self.update_product_button.grid(row=2, column=0, pady=10)

        self.purchase_product_button = Button(self.main_menu_frame, text="Purchase Product", command=self.purchase_product)
        self.purchase_product_button.grid(row=2, column=1, pady=10)

        self.sell_product_button = Button(self.main_menu_frame, text="Sell Product", command=self.sell_product)
        self.sell_product_button.grid(row=3, column=0, pady=10)

        self.generate_report_button = Button(self.main_menu_frame, text="Generate Report", command=self.generate_report)
        self.generate_report_button.grid(row=3, column=1, pady=10)

        self.logout_button = Button(self.main_menu_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=4, column=0, columnspan=2, pady=10)

# Creating the add product function
    def add_product(self):
        self.add_product_frame = Frame(self.window)
        self.add_product_frame.pack()

        self.add_product_label = Label(self.add_product_frame, text="Add Product")
        self.add_product_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.id_label = Label(self.add_product_frame, text="ID")
        self.id_label.grid(row=1, column=0, pady=10)

        self.id_entry = Entry(self.add_product_frame, width=30)
        self.id_entry.grid(row=1, column=1, pady=10)

        self.name_label = Label(self.add_product_frame, text="Name")
        self.name_label.grid(row=2, column=0, pady=10)

        self.name_entry = Entry(self.add_product_frame, width=30)
        self.name_entry.grid(row=2, column=1, pady=10)

        self.description_label = Label(self.add_product_frame, text="Description")
        self.description_label.grid(row=3, column=0, pady=10)

        self.description_entry = Entry(self.add_product_frame, width=30)
        self.description_entry.grid(row=3, column=1, pady=10)

        self.price_label = Label(self.add_product_frame, text="Price")
        self.price_label.grid(row=4, column=0, pady=10)

        self.price_entry = Entry(self.add_product_frame, width=30)
        self.price_entry.grid(row=4, column=1, pady=10)

        self.quantity_label = Label(self.add_product_frame, text="Quantity")
        self.quantity_label.grid(row=5, column=0, pady=10)

        self.quantity_entry = Entry(self.add_product_frame, width=30)
        self.quantity_entry.grid(row=5, column=1, pady=10)

        self.add_product_button = Button(self.add_product_frame, text="Add Product", command=self.add_product_to_inventory)
        self.add_product_button.grid(row=6, column=0, columnspan=2, pady=10)

# Creating the add product to inventory function
    def add_product_to_inventory(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        if self.inventory_management.add_product(id, name, description, price, quantity):
            self.add_product_frame.destroy()

# Creating the remove product function
    def remove_product(self):
        self.remove_product_frame = Frame(self.window)
        self.remove_product_frame.pack()

        self.remove_product_label = Label(self.remove_product_frame, text="Remove Product")
        self.remove_product_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.id_label = Label(self.remove_product_frame, text="ID")
        self.id_label.grid(row=1, column=0, pady=10)

        self.id_entry = Entry(self.remove_product_frame, width=30)
        self.id_entry.grid(row=1, column=1, pady=10)

        self.remove_product_button = Button(self.remove_product_frame, text="Remove Product", command=self.remove_product_from_inventory)
        self.remove_product_button.grid(row=2, column=0, columnspan=2, pady=10)

# Creating the remove product from inventory function
    def remove_product_from_inventory(self):
        id = self.id_entry.get()
        if self.inventory_management.remove_product(id):
            self.remove_product_frame.destroy()
        

# Creating the update product function
    def update_product(self):
        self.update_product_frame = Frame(self.window)
        self.update_product_frame.pack()

        self.update_product_label = Label(self.update_product_frame, text="Update Product")
        self.update_product_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.id_label = Label(self.update_product_frame, text="ID")
        self.id_label.grid(row=1, column=0, pady=10)

        self.id_entry = Entry(self.update_product_frame, width=30)
        self.id_entry.grid(row=1, column=1, pady=10)

        self.name_label = Label(self.update_product_frame, text="Name")
        self.name_label.grid(row=2, column=0, pady=10)

        self.name_entry = Entry(self.update_product_frame, width=30)
        self.name_entry.grid(row=2, column=1, pady=10)

        self.description_label = Label(self.update_product_frame, text="Description")
        self.description_label.grid(row=3, column=0, pady=10)

        self.description_entry = Entry(self.update_product_frame, width=30)
        self.description_entry.grid(row=3, column=1, pady=10)

        self.price_label = Label(self.update_product_frame, text="Price")
        self.price_label.grid(row=4, column=0, pady=10)

        self.price_entry = Entry(self.update_product_frame, width=30)
        self.price_entry.grid(row=4, column=1, pady=10)

        self.quantity_label = Label(self.update_product_frame, text="Quantity")
        self.quantity_label.grid(row=5, column=0, pady=10)

        self.quantity_entry = Entry(self.update_product_frame, width=30)
        self.quantity_entry.grid(row=5, column=1, pady=10)

        self.update_product_button = Button(self.update_product_frame, text="Update Product", command=self.update_product_in_inventory)
        self.update_product_button.grid(row=6, column=0, columnspan=2, pady=10)

# Creating the update product in inventory function
    def update_product_in_inventory(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        if self.inventory_management.update_product(id, name, description, price, quantity):
            self.update_product_frame.destroy()
      

# Creating the get low stock products function
    def get_low_stock_products(self):
        self.get_low_stock_products_frame = Frame(self.window)
        self.get_low_stock_products_frame.pack()

        self.get_low_stock_products_label = Label(self.get_low_stock_products_frame, text="Get Low Stock Products")
        self.get_low_stock_products_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.threshold_label = Label(self.get_low_stock_products_frame, text="Threshold")
        self.threshold_label.grid(row=1, column=0, pady=10)

        self.threshold_entry = Entry(self.get_low_stock_products_frame, width=30)
        self.threshold_entry.grid(row=1, column=1, pady=10)

        self.get_low_stock_products_button = Button(self.get_low_stock_products_frame, text="Get Low Stock Products", command=self.get_low_stock_products_from_inventory)
        self.get_low_stock_products_button.grid(row=2, column=0, columnspan=2, pady=10)

# Creating the get low stock products from inventory function
    def get_low_stock_products_from_inventory(self):
        threshold = self.threshold_entry.get()
        products = self.inventory_management.get_low_stock_products(threshold)
        if len(products) > 0:
            self.get_low_stock_products_frame.destroy()
            self.display_products(products)
      

# Creating the generate purchase function
    def generate_purchase(self):
        self.generate_purchase_frame = Frame(self.window)
        self.generate_purchase_frame.pack()

        self.generate_purchase_label = Label(self.generate_purchase_frame, text="Generate Purchase")
        self.generate_purchase_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.id_label = Label(self.generate_purchase_frame, text="ID")
        self.id_label.grid(row=1, column=0, pady=10)

        self.id_entry = Entry(self.generate_purchase_frame, width=30)
        self.id_entry.grid(row=1, column=1, pady=10)

        self.quantity_label = Label(self.generate_purchase_frame, text="Quantity")
        self.quantity_label.grid(row=2, column=0, pady=10)

        self.quantity_entry = Entry(self.generate_purchase_frame, width=30)
        self.quantity_entry.grid(row=2, column=1, pady=10)

        self.generate_purchase_button = Button(self.generate_purchase_frame, text="Generate Purchase", command=self.generate_purchase_from_inventory)
        self.generate_purchase_button.grid(row=3, column=0, columnspan=2, pady=10)

# Creating the generate purchase from inventory function
    def generate_purchase_from_inventory(self):
        id = self.id_entry.get()
        quantity = self.quantity_entry.get()
        if self.inventory_management.generate_purchase(id, quantity):
            self.generate_purchase_frame.destroy()

# Creating the display products function 
    def display_products(self, products):
        self.display_products_frame = Frame(self.window)
        self.display_products_frame.pack()

        self.display_products_label = Label(self.display_products_frame, text="Products")
        self.display_products_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.products_listbox = Listbox(self.display_products_frame, width=100)
        self.products_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        for product in products:
            self.products_listbox.insert(END, product)

        self.close_button = Button(self.display_products_frame, text="Close", command=self.close_window)
        self.close_button.grid(row=2, column=0, columnspan=2, pady=10)

# Creating the close window function
    def close_window(self):
        self.display_products_frame.destroy()


# Creating the inventory management class 
    def __str__(self):
        return "ID: " + self.id + ", Name: " + self.name + ", Description: " + self.description + ", Price: " + self.price + ", Quantity: " + self.quantity


# Creating the code needed to connect to the database 
# NOTE: I have not included the database file in this repository nor have I connected the database to a localhoast through mysql


import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="inventory",
    auth_plugin='mysql_native_password'
)

# Check if the connection is successful
if db.is_connected():
    print("Database connection successful!")
else:
    print("Database connection failed.")

# Create a cursor object
cursor = db.cursor()

cursor.execute("CREATE DATABASE inventory")

# Execute a query to create a table for the inventory items
create_table_query = """
CREATE TABLE IF NOT EXISTS inventory_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    supplier_name VARCHAR(255) NOT NULL,
    supplier_contact VARCHAR(255) NOT NULL
);
"""
cursor.execute(create_table_query)

# Insert a new item into the inventory
insert_item_query = """
INSERT INTO inventory_items (name, description, quantity, price, supplier_name, supplier_contact)
VALUES (%s, %s, %s, %s, %s, %s);
"""
item_data = ("Example Item", "This is an example item", 10, 10.99, "Example Supplier", "example@supplier.com")
cursor.execute(insert_item_query, item_data)

# Commit the changes to the database
db.commit()

# Execute a query to retrieve all the inventory items
query = "SELECT * FROM inventory_items"
cursor.execute(query)
results = cursor.fetchall()
for result in results:
    print(result)

# Close the cursor and database connection
cursor.close()
db.close()


# creating the supplier class that retrieves the supplier information from the database
class Supplier:
    def __init__(self, id=None, name=None, contact=None):
        self.id = id
        self.name = name
        self.contact = contact

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_contact(self):
        return self.contact

    def set_contact(self, contact):
        self.contact = contact

    @staticmethod
    def get_all_suppliers():
        # Connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="inventory",
            auth_plugin='mysql_native_password'
        )

        # Create a cursor object
        cursor = db.cursor()

        # Execute a query to retrieve all suppliers
        query = "SELECT id, name, contact FROM suppliers_table"
        cursor.execute(query)

        # Create a list of Supplier objects from the query
        suppliers = []
        results = cursor.fetchall()
        for result in results:
            supplier = Supplier(result[0], result[1], result[2])
            suppliers.append(supplier)

        # Close the cursor and database connection
        cursor.close()
        db.close()

        return suppliers

    def __str__(self):
        return "ID: " + self.id + ", Name: " + self.name + ", Contact: " + self.contact

    