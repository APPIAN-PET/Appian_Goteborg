import os
import tkinter as tk
from tkinter import filedialog

def close():
    global l, root, selection
    selection = [l.get(idx) for idx in l.curselection()]
    root.destroy()

def multiple_options(options):
	print('WHAT DO YOU WANT TO CHANGE? SELECT ALL THAT APPLY')
	root = tk.Tk()
    l = tk.Listbox(root, width = 15,selectmode=tk.EXTENDED)
    l.pack()
    [l.insert(tk.END,x) for x in options]
    b = tk.Button(root, text = "OK", command = close).pack()
    root.mainloop()

    return selection

def select_file():
	root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path

print('WHAT DO YOU WANT TO CHANGE? SELECT ALL THAT APPLY')
options = ['Inputs/Outputs','Extraction Atlas','PVC', 'Quantification', 'Appian']




