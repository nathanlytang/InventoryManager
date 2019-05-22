'''
Inventory Manager
Nathan Tang
19/05/16
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class items:
    def __init__(self, item, ID, price, totAvail, totChecked, description):
        self.item = None
        self.ID = None
        self.price = int
        self.totAvail = object
        self.totChecked = object
        self.description = str
    
class totalAvailable:
    def __init__(self):
        self.totAvail = None

class totalChecked:
    def __init__(self):
        self.totChecked = None

def openFile():
    filedialog.askopenfilename(initialdir="/", filetypes=(("CSV", "*.csv"),("All Files", "*.*")))