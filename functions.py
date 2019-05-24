'''
Inventory Manager
Nathan Tang
19/05/16
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlalchemy
import os

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
    fil = open(filedialog.askopenfilename(initialdir="/", filetypes=(("CSV", "*.csv"),("Database", "*.db"),("All Files", "*.*"))))
    print(fil)
    return fil

def newFile():
    directory = filedialog.askdirectory()
    return directory

def sort(tree, column, descending): # Allows user to sort the data

    data = [(tree.set(child, column), child) for child in tree.get_children('')] # Places values to sort in data

    data.sort(reverse=descending) # Reorders data
    for index, item in enumerate(data):
        tree.move(item[1], '', index)

    tree.heading(column, command=lambda col=column: sort(tree, column, int(not descending)))



def addMenu(tree, engine, connection, metadata, inventory):
    
    testarray=[]

    def getItemArgs(*args):
        itemsStr = stringvar1.get()
        IDStr = stringvar2.get()
        priceStr = stringvar3.get()
        availableStr = stringvar4.get()
        checkedOutStr = stringvar5.get()
        descriptionStr = stringvar6.get()
        if itemsStr and IDStr and priceStr and availableStr and checkedOutStr and descriptionStr:
            ContButton.config(state='normal', command=lambda:testarray.append([itemsStr, IDStr, priceStr, availableStr, checkedOutStr, descriptionStr]))
            print(testarray)
            # return itemsStr, IDStr, priceStr, availableStr, checkedOutStr, descriptionStr
        else:
            ContButton.config(state='disabled')
        
    
    root = tk.Tk()
    root.wm_title('Add A New Item')
    root.focus_force()
    labels=('Item: ', 'ID: ', 'Price: ', 'Available: ', 'Checked Out: ', 'Description: ')
    for i in labels:
        tk.Label(root, text=i, justify=tk.LEFT, anchor='w').grid(row=labels.index(i))

    stringvar1 = tk.StringVar(root)
    stringvar2 = tk.StringVar(root)
    stringvar3 = tk.StringVar(root)
    stringvar4 = tk.StringVar(root)
    stringvar5 = tk.StringVar(root)
    stringvar6 = tk.StringVar(root)

    stringvar1.trace('w', getItemArgs)
    stringvar2.trace('w', getItemArgs)
    stringvar3.trace('w', getItemArgs)
    stringvar4.trace('w', getItemArgs)
    stringvar5.trace('w', getItemArgs)
    stringvar6.trace('w', getItemArgs)

    items = tk.Entry(root, width=40, textvariable=stringvar1)
    ID = tk.Entry(root, width=40, textvariable=stringvar2)
    price = tk.Entry(root, width=40, textvariable=stringvar3)
    available = tk.Entry(root, width=40, textvariable=stringvar4)
    checkedOut = tk.Entry(root, width=40, textvariable=stringvar5)
    description = tk.Entry(root, width=40, textvariable=stringvar6)

    items.grid(row=0, column=1)
    ID.grid(row=1, column=1)
    price.grid(row=2, column=1)
    available.grid(row=3, column=1)
    checkedOut.grid(row=4, column=1)
    description.grid(row=5, column=1)

    ContButton = tk.Button(root, text='Continue', command=lambda: getItemArgs(items, ID, price, available, checkedOut, description))
    ContButton.grid(row=6, column=1)

    

    root.focus_force()

    root.mainloop()



def printTreeview(tree, resultSet): # Updates the treeview with CSV data

    tree.delete(*tree.get_children()) # Delete tree

    # Writes updated tree
    for i in range(len(resultSet)):
        tree.insert("", i, values=(resultSet[i][0],resultSet[i][1],resultSet[i][2],resultSet[i][3],resultSet[i][4],resultSet[i][5]))