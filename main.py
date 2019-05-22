'''
Inventory Manager
Nathan Tang
19/05/16
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import csv
import functions

root = tk.Tk()
root.wm_title("Inventory Manager")

def openKey(event):
    fil = open(filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=(("CSV", "*.csv"),("All Files", "*.*"))), newline= '')
    print(fil)
    return fil
    

def newKey(event):
    directory = filedialog.askdirectory()
    print(directory)
    return directory

# File Menu

file_menu = tk.Menu(root)
file_submenu = tk.Menu(file_menu, tearoff=False)
file_submenu.add_command(label = 'New         Ctrl+N', command=lambda: filedialog.askdirectory())
file_submenu.add_command(label = 'Open        Ctrl+O', command=lambda: filedialog.askopenfilename(initialdir="/", filetypes=(("CSV", "*.csv"),("All Files", "*.*"))))
file_submenu.add_command(label = 'Exit', command=lambda: root.quit())
file_menu.add_cascade(label = 'File', menu = file_submenu)

openFile = root.bind("<Control-o>", openKey)
directory = root.bind("<Control-n>", newKey)
root.config(menu=file_menu)

# Buttons
buttons = ttk.Frame()
buttons.pack(fill=tk.BOTH)

addButton = tk.Button(root, text='Add', relief=tk.FLAT)
editButton = tk.Button(root, text='Edit', relief=tk.FLAT)
delButton = tk.Button(root, text='Delete', relief=tk.FLAT)
checkOutButton = tk.Button(root, text='Check Out', relief=tk.FLAT)
checkInButton = tk.Button(root, text='Check In', relief = tk.FLAT)

addButton.pack(side=tk.LEFT, ipadx=5, ipady=5, in_=buttons)
editButton.pack(side=tk.LEFT, ipadx=5, ipady=5, in_=buttons)
delButton.pack(side=tk.LEFT, ipadx=5, ipady=5, in_=buttons)
checkOutButton.pack(side=tk.LEFT, ipadx=5, ipady=5, in_=buttons)
checkInButton.pack(side=tk.LEFT, ipadx=5, ipady=5, in_=buttons)

buttons.grid_columnconfigure(0, weight=1)
buttons.grid_rowconfigure(0, weight=1)



# Treeview
container = ttk.Frame()
container.pack(fill='both', expand=True)

treeColumns = ("Item","ID","Price","Available","Checked out","Description")
tree = ttk.Treeview(columns=treeColumns, show="headings")

for column in treeColumns:
    tree.heading(column, text=column, command=lambda c=column: functions.sort(tree, c, 0))

for i in treeColumns:
    tree.column(i, width=130, minwidth=30)

vsb = ttk.Scrollbar(orient="vertical", command=tree.yview) # Vertical scroll bar
hsb = ttk.Scrollbar(orient="horizontal", command=tree.xview) # Horizontal scroll bar

tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

vsb.grid(column=1, row=0, sticky='ns', in_=container)
hsb.grid(column=0, row=1, sticky='ew', in_=container)
tree.grid(column=0, row=0, sticky='nsew', in_=container)

container.grid_columnconfigure(0, weight=1)
container.grid_rowconfigure(0, weight=1)


root.mainloop()