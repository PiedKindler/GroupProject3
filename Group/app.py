import eel
import webbrowser
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import GroupProjectWithGUI.web.inventory_system as inventory_system
from GroupProjectWithGUI.web.inventory_system import Reporting
from GroupProjectWithGUI.web.inventory_system import InventoryManagementGUI

root = Tk()
w = Label(root, text = "Inventory Program")


# This needs to be changed to your file path for the folder holding the categories.html file and the other html files.
# Starts the connection between GUI and database
eel.init("GroupProjectWithGUI\web", allowed_extensions=['.css', '.js', '.html'])


# Function to run from database when button in login page is clicked
@eel.expose
def getLogin():
   root.attributes("-topmost", True)
   usernm = simpledialog.askstring("Username", "Username:")
   root.attributes("-topmost", True)
   passwd = simpledialog.askstring("Password", "Password:")
   eel.start('main.html',mode='chrome',
                        host='localhost',
                        port=8000, # ensures port is different than the main page runs once login is done
                        block=True)

# Function to run from database when button in inventory needed page is clicked
@eel.expose
def getNeeded():
   print(inventory_system.InventoryManagementGUI.display_products())

# Function to run from database when button in categories page is clicked
#Add products to database
@eel.expose
def getAdd():
   addProd = simpledialog.askstring("Item Name", "Product Name:")
   addAmt = simpledialog.askinteger("Purchase Amount", "Amount to add:")
   return(inventory_system.Inventory.add_product()) 
  
# Function to run from database when button in categories page is clicked
# Subtracts product from database
@eel.expose
def getMinus():
   lessProd = simpledialog.askstring("Item Name", "Product Name:")
   lessAmt = simpledialog.askinteger("Amount Used", "Amount to subtract:")
   return(inventory_system.Inventory.add_product())    

# Function to run from database when button in customer info page is clicked
@eel.expose
def getCompanies():
   print(inventory_system.Supplier.names())   

# Function to run from database when button in product inventory page is clicked      
@eel.expose
def getItems():
   print(inventory_system.Reporting.items())
   print(inventory_system.Reporting.itemDescription())

# Function to run from database when button in sales page is clicked
@eel.expose
def getSales():
   addIn = simpledialog.askstring("Purchase Item", "Product Name:")
   quantity = simpledialog.askinteger("Purchase Amount", "Amount Needed:")
   return(inventory_system.Sales.add_sale())

# Starts the login page on startup
eel.start('login.html', mode='chrome',
                        host='localhost',
                        port=27000, # ensures port is different than the main page runs once login is done
                        block=True)




