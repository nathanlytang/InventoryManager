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

class itemsClass:
    def __init__(self):
        self.item = None
        self.ID = None
        self.price = int
        self.totAvail = totalAvailable()
        self.totChecked = totalChecked()
        self.description = str

    def setItem(self, item):
        self.item = item
        return self.item

    def setID(self, ID):
        self.ID = ID
        return self.ID

    def setPrice(self, price):
        self.price = price
        return self.price

    def setTotAvail(self, totAvail):
        self.totAvail = totAvail

    def setTotChecked(self, totChecked):
        self.totChecked = totChecked

    def setDescription(self, description):
        self.description = description

    def getItem(self):
        return self.item
    
    def getID(self):
        return self.ID
    
    def getPrice(self):
        return self.price

    def getTotAvail(self):
        return self.totAvail

    def getTotChecked(self):
        return self.totChecked

    def getDescription(self):
        return self.description

    
class totalAvailable:
    def __init__(self):
        self.totAvail = int

    def setTotAvail(self, totAvail):
        self.totAvail = totAvail

    def getTotAvail(self):
        return self.totAvail

class totalChecked:
    def __init__(self):
        self.totChecked = int

    def setTotChecked(self, totChecked):
        self.totChecked = totChecked

    def getTotChecked(self):
        return self.totChecked

def openSQL():
    engine = sqlalchemy.create_engine('sqlite:///%s\\inventory.db' % os.getcwd())
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    inventory = sqlalchemy.Table('inventory', metadata, autoload=True, autoload_with=engine)
    print(inventory.columns.keys())
    query = sqlalchemy.select([inventory])
    resultProxy = connection.execute(query)
    resultSet = resultProxy.fetchall()
    print(resultSet)
    return engine, connection, metadata, inventory, query, resultProxy, resultSet

def openFile():
    fil = open(filedialog.askopenfilename(initialdir="/", filetypes=(("Database", "*.db"),("CSV", "*.csv"),("All Files", "*.*"))))
    print(fil)
    return fil

def newFile():
    directory = filedialog.asksaveasfile(defaultextension=".db", filetypes=(("Database", "*.db"),))
    return directory

def sort(tree, column, descending): # Allows user to sort the data

    data = [(tree.set(child, column), child) for child in tree.get_children('')] # Places values to sort in data
    
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][0] = int(data[i][0])
    except:
        data[i] = tuple(data[i])

    data.sort(reverse=descending) # Reorders data
    for index, item in enumerate(data):
        tree.move(item[1], '', index)

    tree.heading(column, command=lambda col=column: sort(tree, column, int(not descending)))



def addMenu(tree): # Add Menu

    engine, connection, metadata, inventory, query, resultProxy, resultSet = openSQL()

    def getItemArgs(*args):  # Get items in entry
        item = stringvar1.get()
        ID = stringvar2.get()
        price = intVar1.get()
        available = intVar2.get()
        checkedOut = intVar3.get()
        description = stringvar3.get()
        if item and ID and price and available and checkedOut and description:
            ContButton.config(state='normal', command=lambda: ContButtonFunc(item, ID, price, available, checkedOut, description))
        else:
            ContButton.config(state='disabled')

    def ContButtonFunc(item, ID, price, available, checkedOut, description):
        
        newItem = itemsClass()
        newItem.setItem(item)
        newItem.setID(ID)
        newItem.setPrice(price)
        newItem.setTotAvail(available)
        newItem.setTotChecked(checkedOut)
        newItem.setDescription(description)

        # Write to tree
        tree.insert("", len(tree.get_children()), values=(newItem.getItem(), newItem.getID(), newItem.getPrice(), newItem.getTotAvail(), newItem.getTotChecked(), newItem.getDescription()))

        # Write to DB
        query = sqlalchemy.insert(inventory)
        values = [{'Item':newItem.getItem(), 'ID':newItem.getID(), 'Price':newItem.getPrice(), 'Available':newItem.getTotAvail(), 'CheckedOut':newItem.getTotChecked(), 'Description':newItem.getDescription()}]
        resultProxy = connection.execute(query, values)
        results = connection.execute(sqlalchemy.select([inventory])).fetchall()
        root.destroy()
    
    
    root = tk.Tk()
    root.wm_title('Add A New Item')
    root.focus_force()
    labels=('Item: ', 'ID: ', 'Price: ', 'Available: ', 'Checked Out: ', 'Description: ')
    for i in labels:
        tk.Label(root, text=i, justify=tk.LEFT, anchor='w').grid(row=labels.index(i))

    stringvar1 = tk.StringVar(root)
    stringvar2 = tk.StringVar(root)
    stringvar3 = tk.StringVar(root)
    intVar1 = tk.IntVar(root)
    intVar2 = tk.IntVar(root)
    intVar3 = tk.IntVar(root)

    stringvar1.trace('w', getItemArgs)
    stringvar2.trace('w', getItemArgs)
    stringvar3.trace('w', getItemArgs)
    intVar1.trace('w', getItemArgs)
    intVar2.trace('w', getItemArgs)
    intVar3.trace('w', getItemArgs)

    item = tk.Entry(root, width=40, textvariable=stringvar1)
    ID = tk.Entry(root, width=40, textvariable=stringvar2)
    price = tk.Entry(root, width=40, textvariable=intVar1)
    available = tk.Entry(root, width=40, textvariable=intVar2)
    checkedOut = tk.Entry(root, width=40, textvariable=intVar3)
    description = tk.Entry(root, width=40, textvariable=stringvar3)

    item.grid(row=0, column=1)
    ID.grid(row=1, column=1)
    price.grid(row=2, column=1)
    available.grid(row=3, column=1)
    checkedOut.grid(row=4, column=1)
    description.grid(row=5, column=1)

    ContButton = tk.Button(root, text='Continue', command=lambda: getItemArgs(item, ID, price, available, checkedOut, description))
    ContButton.grid(row=6, column=1)

    root.focus_force()
    root.mainloop()

def editMenu(tree): # Edit Menu

    engine, connection, metadata, inventory, query, resultProxy, resultSet = openSQL()
    selected_item = tree.selection()[0]
    treeItem = tree.item(selected_item)['values']

    def getItemArgs(*args):  # Get items in entry
        item = stringvar1.get()
        ID = stringvar2.get()
        price = intVar1.get()
        available = intVar2.get()
        checkedOut = intVar3.get()
        description = stringvar3.get()
        if item and ID and price and available and checkedOut and description:
            ContButton.config(state='normal', command=lambda: ContButtonFunc(item, ID, price, available, checkedOut, description))
        else:
            ContButton.config(state='disabled')

    def ContButtonFunc(item, ID, price, available, checkedOut, description):
        
        newItem = itemsClass()
        newItem.setItem(item)
        newItem.setID(ID)
        newItem.setPrice(price)
        newItem.setTotAvail(available)
        newItem.setTotChecked(checkedOut)
        newItem.setDescription(description)

        # Write to tree
        tree.insert("", len(tree.get_children()), values=(newItem.getItem(), newItem.getID(), newItem.getPrice(), newItem.getTotAvail(), newItem.getTotChecked(), newItem.getDescription()))

        # Write to DB
        query = sqlalchemy.insert(inventory)
        values = [{'Item':newItem.getItem(), 'ID':newItem.getID(), 'Price':newItem.getPrice(), 'Available':newItem.getTotAvail(), 'CheckedOut':newItem.getTotChecked(), 'Description':newItem.getDescription()}]
        resultProxy = connection.execute(query, values)
        results = connection.execute(sqlalchemy.select([inventory])).fetchall()
        root.destroy()

    delItem(tree)
    root = tk.Tk()
    root.wm_title('Edit')
    root.focus_force()
    labels=('Item: ', 'ID: ', 'Price: ', 'Available: ', 'Checked Out: ', 'Description: ')
    for i in labels:
        tk.Label(root, text=i, justify=tk.LEFT, anchor='w').grid(row=labels.index(i))

    stringvar1 = tk.StringVar(root)
    stringvar2 = tk.StringVar(root)
    stringvar3 = tk.StringVar(root)
    intVar1 = tk.IntVar(root)
    intVar2 = tk.IntVar(root)
    intVar3 = tk.IntVar(root)

    stringvar1.trace('w', getItemArgs)
    stringvar2.trace('w', getItemArgs)
    stringvar3.trace('w', getItemArgs)
    intVar1.trace('w', getItemArgs)
    intVar2.trace('w', getItemArgs)
    intVar3.trace('w', getItemArgs)

    item = tk.Entry(root, width=40, textvariable=stringvar1)
    ID = tk.Entry(root, width=40, textvariable=stringvar2)
    price = tk.Entry(root, width=40, textvariable=intVar1)
    available = tk.Entry(root, width=40, textvariable=intVar2)
    checkedOut = tk.Entry(root, width=40, textvariable=intVar3)
    description = tk.Entry(root, width=40, textvariable=stringvar3)

    item.insert(tk.END, treeItem[0])
    ID.insert(tk.END, treeItem[1])
    price.insert(tk.END, treeItem[2])
    available.insert(tk.END, treeItem[3])
    checkedOut.insert(tk.END, treeItem[4])
    description.insert(tk.END, treeItem[5])

    item.grid(row=0, column=1)
    ID.grid(row=1, column=1)
    price.grid(row=2, column=1)
    available.grid(row=3, column=1)
    checkedOut.grid(row=4, column=1)
    description.grid(row=5, column=1)

    ContButton = tk.Button(root, text='Continue', command=lambda: getItemArgs(item, ID, price, available, checkedOut, description))
    ContButton.grid(row=6, column=1)

    root.focus_force()
    root.mainloop()


def delItem(tree): # Delete item
    engine, connection, metadata, inventory, query, resultProxy, resultSet = openSQL()
    selected_item = tree.selection()[0] # Deletes selected item from tree and db file
    treeItem = tree.item(selected_item)['values']
    for i in range(len(resultSet)):
        if resultSet[i] == tuple(treeItem):
            connection.execute(inventory.delete().where(inventory.columns.Item == treeItem[0]))
            break
    tree.delete(selected_item)


def checkOut(tree): # Check out an item
    engine, connection, metadata, inventory, query, resultProxy, resultSet = openSQL()
    selected_item = tree.selection()[0]
    treeItem = tree.item(selected_item)['values']
    for i in range(len(resultSet)):
        if resultSet[i] == tuple(treeItem):
            connection.execute(sqlalchemy.update(inventory).values(
                Available = treeItem[3] - 1, CheckedOut = treeItem[4] + 1).where(inventory.columns.Item == treeItem[0]))
            break
    printTreeview(tree)

def checkIn(tree): # Check in an item
    engine, connection, metadata, inventory, query, resultProxy, resultSet = openSQL()
    selected_item = tree.selection()[0]
    treeItem = tree.item(selected_item)['values']
    for i in range(len(resultSet)):
        if resultSet[i] == tuple(treeItem):
            connection.execute(sqlalchemy.update(inventory).values(
                Available = treeItem[3] + 1, CheckedOut = treeItem[4] - 1).where(inventory.columns.Item == treeItem[0]))
            break
    printTreeview(tree)

def printTreeview(tree): # Updates the treeview

    engine, connection, metadata, inventory, query, resultProxy, resultSet = openSQL()

    tree.delete(*tree.get_children()) # Delete tree

    # Writes updated tree
    for i in range(len(resultSet)):
        tree.insert("", i, values=(resultSet[i][0],resultSet[i][1],resultSet[i][2],resultSet[i][3],resultSet[i][4],resultSet[i][5]))