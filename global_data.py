from tkinter import *
from tkinter import ttk
root = Tk()
tree = ttk.Treeview(root, columns=("Sensor", "Wartość", "Jednostka", "Timestamp", "Śr.1h", "Śr.12h"), show="headings")
sensor_items = {}
history = {}