import eel
import inventory_system
from inventory_system import Reporting


# This needs to be changed to your file path for the folder holding the categories.html file and the other html files.
eel.init("web", allowed_extensions=['.css', '.html'])


# Function testing out getting info from the other system but commented out since it doesn't work yet.
@eel.expose
def curr_inventory():
   print(inventory_system.Reporting.generate_report())

curr_inventory()

eel.start('categories.html')