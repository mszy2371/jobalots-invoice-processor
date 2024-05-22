import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from app.backend.processor import DataProcessor
from tkinter import Label
from app.backend.app_logging import logger
import os
from paths import BASE_DIR
from app.utils.messages import select_message





# creating the root window
root = tk.Tk()
root.title("Invoice Processor")
root.resizable(True, True)
root.geometry("800x600")

data_processor = DataProcessor()

def select_message(invoice_no, output_key) -> str:
    outputs = {
        "done": f"{invoice_no} - Done!",
        "invoice exists": f"{invoice_no} - Invoice already exists in table, nothing added to main table",
        "empty": f"{invoice_no} - No data to process, empty file",
        "partially done": f"{invoice_no} - Partially done, some manifests missing, check logs",
    }
    return outputs[output_key]


def select_files():
    try:
        init_dir_input = os.path.join(BASE_DIR, "app", "input_data")
        init_dir_output = os.path.join(BASE_DIR, "app", "output_data")
        input_file = fd.askopenfilename(
            title="choose input file",
            initialdir=init_dir_input,
            filetypes=(("pdf files", "*.pdf"),),
        )
        if not input_file:
            showinfo(
                title="Error", message="You must select an input file for processing"
            )
            return

        output_file = fd.askopenfilename(
            title="choose output file or `Cancel` to create a NEW FILE:",
            initialdir=init_dir_output,
            filetypes=(("csv files", "*.csv"),),
        )
        if not output_file:
            showinfo(
                title="Message",
                message="Output file not selected. Create a new file in next step",
            )

        if input_file:
            if not output_file:
                output_file = fd.asksaveasfilename(
                    title="Create output file:", defaultextension=".csv"
                )
                if output_file:
                    with open(output_file, "w") as file:
                        file.write("")
                else:
                    showinfo(
                        title="Error",
                        message="You must select output file or create a new file. Operation aborted.",
                    )
                    root.destroy()
                    return
        else:
            showinfo(title="Error", message="You must select input file")
        if input_file and output_file:
            processing_info = Label(
                root, text="Processing, please wait...", wraplength=500, anchor="n", justify="center", font=("Arial", 26)
            )
            processing_info.pack(expand=True, ipadx=20, ipady=20)
            root.update_idletasks()
            invoice_no, output = data_processor.add_data_to_main_table(input_file, output_file)
            message = select_message(invoice_no, output)
            processing_info.pack_forget()
            done_info = Label(
                root, text=message, wraplength=500, justify="center", font=("Arial", 26)
            )
            done_info.pack(expand=True, ipadx=20, ipady=20)
            done_info.after(12000, done_info.destroy)
    except Exception as exc:
        showinfo(title="Error", message=exc)
        logger.error(exc.with_traceback(exc.__traceback__))
        return


if __name__ == "__main__":
    open_button = ttk.Button(
        root,
        text="Open Files",
        command=select_files,
    )
    open_button.pack(expand=True, ipadx=20, ipady=20)

    root.mainloop()
    