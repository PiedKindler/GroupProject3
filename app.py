import eel
import GroupProjectWithGUI.web.inventory_system as inventory_system
from GroupProjectWithGUI.web.inventory_system import Reporting


# This needs to be changed to your file path for the folder holding the categories.html file and the other html files.
eel.init("GroupProjectWithGUI\web", allowed_extensions=['.css', '.js', '.html'])


# Function testing out getting info from the other system but commented out since it doesn't work yet.
@eel.expose
def getData():
   print(inventory_system.Reporting.items())

#getData()

eel.start('productinventory.html')