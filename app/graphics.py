import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from invoice_processor import InvoiceProcessor

# create the root window
root = tkinter.Tk()
root.title("File Dialog")
root.resizable(False, False)
root.geometry("600x600")

invoice_processor = InvoiceProcessor()


def select_files():
    input_file = fd.askopenfilename(
        title="pick input file", initialdir="./", filetypes=(("pdf files", "*.pdf"),)
    )

    output_file = fd.askopenfilename(
        title="pick output file", initialdir="./", filetypes=(("csv files", "*.csv"),)
    )

    showinfo(title="Selected File", message=(input_file, output_file))

    if input_file:
        if not output_file:
            output_file = fd.asksaveasfilename(title="Create output file:", defaultextension=".csv")
            if output_file:
                with open(output_file, 'w') as file:
                    file.write("")
    else:
        showinfo(title="Error", message="You must select input file")
    if input_file and output_file:
        invoice_processor.add_data_to_main_table(input_file, output_file)


# open button
open_button = ttk.Button(
    root,
    text="Open Files",
    command=select_files,
)
open_button.pack(expand=True)


root.mainloop()
