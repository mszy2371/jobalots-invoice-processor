import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from invoice_processor import InvoiceProcessor
from tkinter import Label



# create the root window
root = tk.Tk()
root.title("File Dialog")
root.resizable(False, False)
root.geometry("600x400")

invoice_processor = InvoiceProcessor()


def select_files():
    try:
        input_file = fd.askopenfilename(
            title="choose input file", initialdir="./", filetypes=(("pdf files", "*.pdf"),)
        )
        if not input_file:
            showinfo(title="Error", message="You must select an input file for processing")
            return

        output_file = fd.askopenfilename(
            title="choose output file or `Cancel` to create a new file", initialdir="./", filetypes=(("csv files", "*.csv"),)
        )
        if not output_file:
            showinfo(title="Message", message="Output file not selected. Create a new file in next step")
        
        if input_file:
            if not output_file:
                output_file = fd.asksaveasfilename(title="Create output file:", defaultextension=".csv")
                if output_file:
                    with open(output_file, 'w') as file:
                        file.write("")
                else:
                    showinfo(title="Error", message="You must select output file or create a new file. Operation aborted.")
                    root.destroy()
                    return
        else:
            showinfo(title="Error", message="You must select input file")
        if input_file and output_file:
            invoice_processor.add_data_to_main_table(input_file, output_file)
            done_info = Label(root, text="Done!", wraplength=500, justify="center", font=("Arial", 26))
            done_info.pack(expand=True, ipadx=20, ipady=20)
            done_info.after(4000, done_info.destroy)
    except Exception as exc:
        print(exc)
        showinfo(title="Error", message=exc)
        return


open_button = ttk.Button(
    root,
    text="Open Files",
    command=select_files,
)
open_button.pack(expand=True, ipadx=20, ipady=20)


root.mainloop()
