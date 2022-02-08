import tkinter as tk
from tkinter import Menu
from tkinter import ttk

# quit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit()

# Create Instance
win = tk.Tk()

# Set Title
win.title("TKinter Demo")

# Create Menu Bar
menuBar = Menu()
win.config(menu=menuBar)

# Add Menu Options
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(labe="New")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=_quit)
menuBar.add_cascade(label="File", menu=fileMenu)

#Tab control with Notebook
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Tab1")
tabControl.pack(expand=1, fill="both") # Pack to make visible

win.mainloop()

