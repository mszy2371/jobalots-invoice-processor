import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from invoice_processor import InvoiceProcessor

# create the root window
root = tkinter.Tk()
root.title('Tkinter File Dialog')
root.resizable(False, False)
root.geometry('600x600')


def select_files():
    filetypes = (
        ('all files', '*.*'),
    )
    l = []
    filenames = fd.askopenfilenames(
        title='Open files',
        initialdir='./',
        filetypes=filetypes)
    

    showinfo(
        title='Selected Files',
        message=filenames
    )
    
    print(filenames)
    return filenames
    
# open button
open_button = ttk.Button(
    root,
    text='Open Files',
    command=select_files,
    
    
)

open_button.pack(expand=True)



root.mainloop()