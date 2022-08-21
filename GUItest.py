import tkinter as tk
import ctypes
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
import generate_tmp as tmp
import ass_writer as aw

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

def ass_auto():
    sce_types = (
        ('sce files', '*.sce'),
        ('all files', '*.*')
    )
    sce_f = fd.askopenfilename(
        title = 'Open SCE File',
        initialdir = '/',
        filetypes = sce_types
    )

    vid_types = (
        ('mp4 files', '*.mp4'),
        ('all files', '*.*')
    )
    vid_f= fd.askopenfilename(
        title = 'Open Video File',
        initialdir = '/',
        filetypes = vid_types
    )

    aw.ass_writer(sce_f, vid_f)
    showinfo(title = 'Info', message = 'Work Completed!')

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
    text = 'Run ASS automation',
    padding=10,
    command = ass_auto
)

tmp_button.pack(expand = True)
substitude_button.pack(expand= True)

root.mainloop()

