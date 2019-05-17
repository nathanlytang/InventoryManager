'''
Inventory Manager
Nathan Tang
19/05/16
'''

import tkinter as tk
from tkinter import ttk
import csv
import functions

root = tk.Tk()
root.wm_title("Inventory Manager")

addButton = tk.Button(root, text='Add')
editButton = tk.Button(root, text='Edit')
delButton = tk.Button(root, text='Delete')
checkOutButton = tk.Button(root, text='Check Out')
checkInButton = tk.Button(root, text='Check In')

addButton.pack(side=tk.LEFT)
editButton.pack(side=tk.LEFT)
delButton.pack(side=tk.LEFT)
checkOutButton.pack(side=tk.LEFT)
checkInButton.pack(side=tk.LEFT)


root.mainloop()