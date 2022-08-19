import tkinter as tk
import os
import ctypes
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
import utils.generate_tmp as tmp
import utils.tl_substitude as sub

def sce_template():
    sce_types = (
        ('sce files', '*.sce'),
        ('all files', '*.*')
    )
    sce_name = fd.askopenfilename(
        title = 'Open SCE File',
        initialdir = '/',
        filetypes = sce_types
    )
    tmp.sce_to_template(sce_name)
    try:
        showinfo(title = 'Info', message = 'Work Completed!')
    except:
        showerror(title = 'Error', message = 'Please check out source code')

def sce_sub():
    txt_types = (
        ('txt files', '*.txt'),
        ('all files', '*.*')
    )
    txt_f = fd.askopenfilename(
        title = 'Open TXT File',
        initialdir = '/',
        filetypes = txt_types
    )

    sce_types = (
        ('sce files', '*.sce'),
        ('all files', '*.*')
    )
    sce_f= fd.askopenfilename(
        title = 'Open SCE File',
        initialdir = '/',
        filetypes = sce_types
    )

    txt_n = os.path.split(txt_f)[1]
    sce_n = os.path.split(sce_f)[1]
    txt_name = os.path.splitext(txt_n)[0]
    sce_name = os.path.splitext(sce_n)[0]
    if txt_name == sce_name:
        sub.sce_substitude(txt_f, sce_f)
        showinfo(title = 'Info', message = 'Work Completed!')
    else:
        showerror(title = 'Error', message = 'Files should have the same name')

def center_window(w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
root = tk.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)
root.title('SCE Tools')
root.minsize(250, 150)
root.resizable(True, True)
center_window(250, 150)
#root.attributes("-toolwindow", 2)

tmp_button = ttk.Button(
    root,
    text = 'Generate TL Template',
    padding=10,
    command = sce_template
)

substitude_button = ttk.Button(
    root,
    text = 'Substitude tmp to SCE',
    padding=10,
    command = sce_sub
)

tmp_button.pack(expand = True)
substitude_button.pack(expand= True)

root.mainloop()

