import requests
import fitz  # imports the pymupdf library
import pandas as pd
import os
import csv
import sys
import logging

logger = logging.getLogger(__name__)

class InvoiceProcessor:
    def __init__(self, standard_tax_rate=0.2):
        self.input_manifest_path =  os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "input.csv"
        )
        self.output_manifest_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "manifest.csv"
        )
        self.standard_tax_rate = standard_tax_rate
    
    def convert_invoice_to_str_and_list_tuple(
        self, invoice_path: str
    ) -> tuple[str, list]:
        invoice_list = []
        all_text = ""
        doc = fitz.open(invoice_path)
        for page in doc:
            text = page.get_text()
            all_text += text
            page_tables = page.find_tables(
                snap_tolerance=2,
            )
            for table in page_tables:
                item = table.extract()
                if len(item) > 2:
                    invoice_list.extend(item)
        return all_text, invoice_list

    def get_invoice_date(self, invoice_str: str) -> str:
        invoice_date = invoice_str.split("ORDER DATE : ")[1].split("\n")[0]
        return invoice_date

    def get_invoice_no(self, invoice_str: str) -> str:
        invoice_no = invoice_str.split("INVOICE ")[1].split("\n")[0]
        return invoice_no

    def get_invoice_item_price(self, invoice_item: list) -> float | bool:
        price_str = invoice_item[-1]
        try:
            return float(price_str.split("£")[1])
        except TypeError:
            return 0.0

    def get_manifest_items_quantity(self, manifest_path) -> int:
        total = 1
        with open(manifest_path, "r", encoding="utf-8") as csv_reader:
            reader = csv.reader(csv_reader)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                else:
                    quantity = int(row[4]) if row[4] else 0
                    total += quantity
        return total

    def get_manifest_item_price(self, invoice_item: list, manifest_path: str) -> float:
        invoice_item_price = self.get_invoice_item_price(invoice_item)
        manifest_items_quantity = self.get_manifest_items_quantity(manifest_path)
        return round((invoice_item_price / manifest_items_quantity), 2)
    
    def get_manifest_item_tax_value(self, invoice_item: list, manifest_path: str) -> float:
        manifest_items_quantity = self.get_manifest_items_quantity(manifest_path)
        invoice_item_price = self.get_invoice_item_price(invoice_item)
        tax_rate = self.set_tax_rate(invoice_item)
        return round((invoice_item_price / manifest_items_quantity * tax_rate), 2)
    
    def set_tax_rate(self, invoice_item: list) -> float:
        for item in reversed(invoice_item):
            if "%" in item:
                return float(item.split("%")[0]) / 100
            return self.standard_tax_rate
        
    def retrieve_manifest_from_website(self, manifest_id: str) -> str | None:
        url = f"https://static.bodysocks.net/joblots/manifests/{manifest_id}.csv"
        page = requests.get(url)
        if page.status_code != 200 or page.text.startswith("<html>"):
            logger.error(f"Manifest {manifest_id} not found online.")
            return None
        with open(self.input_manifest_path, "w", encoding="utf-8") as f:
            f.write(page.text)
        return self.input_manifest_path
    
    def search_manifest_in_local_drive(self, manifest_id: str) -> str | None:
        manifest_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), f"input_data/manifests/{manifest_id}.csv"
        )
        if not os.path.exists(manifest_path):
            logger.error(f"Manifest {manifest_id} not found locally.")
            return None
        print(manifest_path)
        logger.info(f"Local manifest {manifest_id} found.")
        return manifest_path
    
    def retrieve_manifest(self, manifest_id: str) -> str | None:
        manifest_path = self.retrieve_manifest_from_website(manifest_id)
        if not manifest_path:
            manifest_path = self.search_manifest_in_local_drive(manifest_id)
        return manifest_path
    

    def convert_manifest(
        self,
        invoice_date: str,
        invoice_no: str,
        invoice_item: list,
        input_csv_path: str,
        manifest_item_price: float,
        manifest_item_tax_value: float,
    ) -> pd.DataFrame:
        manifest_id = invoice_item[1]
        with open(input_csv_path, "r", encoding="utf-8") as csv_reader, open(
            self.output_manifest_path, "w", encoding="utf-8"
        ) as csv_writer:
            reader = csv.reader(csv_reader)
            writer = csv.writer(csv_writer)
            for index, row in enumerate(reader):
                if index == 0:
                    row.append("Manifest No")
                    row.append("Invoice No")
                    row.append("Invoice Date")
                    row.append("Price per item")
                    row.append("Tax per item")
                    writer.writerow(row)
                elif len(row[0]) < 2:
                    continue
                else:
                    row.append(manifest_id)
                    row.append(invoice_no)
                    row.append(invoice_date)
                    row.append(manifest_item_price)
                    row.append(manifest_item_tax_value)
                    writer.writerow(row)
        df = pd.read_csv(self.output_manifest_path, encoding="utf-8")
        df.drop("Unit Weight (g)", axis=1, inplace=True)
        df.drop("RRP", axis=1, inplace=True)
        df.drop("Total", axis=1, inplace=True)
        df["Price per item + tax"] = round((df["Price per item"] + df["Tax per item"]), 2)
        df["Total tax"] = round((df["Tax per item"] * df["Stock Quantity"]), 2)
        df["Total price netto"] = round((df["Price per item"] * df["Stock Quantity"]), 2)
        return df

    def process_invoice_data(self, invoice_list: str, invoice_no: str, invoice_date: str) -> dict | bool:
        df_combined = pd.DataFrame()
        output_csv_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"output_data/data_for_{invoice_no}_from_{invoice_date}.csv",
        )
        for item in invoice_list:
            manifest_id = item[1]
            manifest_path = self.retrieve_manifest(manifest_id)
            if not manifest_path:
                return False
            manifest_item_price = self.get_manifest_item_price(item, manifest_path)
            manifest_item_tax_value = self.get_manifest_item_tax_value(item, manifest_path)
            df = self.convert_manifest(
                invoice_date, invoice_no, item, manifest_path, manifest_item_price, manifest_item_tax_value
            )
            df_combined = df_combined._append(df, ignore_index=True)
        with open(output_csv_path, "w") as f:
            f.write(df_combined.to_csv())
        if os.path.exists(self.input_manifest_path):
            os.remove(self.input_manifest_path)
        if os.path.exists(self.output_manifest_path):
            os.remove(self.output_manifest_path)
        return df_combined
    
    def add_data_to_main_table(self, invoice_path: str, main_table_path: str):
        invoice_str, invoice_list = self.convert_invoice_to_str_and_list_tuple(invoice_path)
        invoice_date = self.get_invoice_date(invoice_str)
        invoice_no = self.get_invoice_no(invoice_str)
        df = self.process_invoice_data(invoice_list, invoice_no, invoice_date)
        if os.path.exists(main_table_path) and os.path.getsize(main_table_path) > 0:
            df_main = pd.read_csv(main_table_path, index_col=0)
            if invoice_no in df_main["Invoice No"].values:
                logger.info(f"Data for invoice {invoice_no} already exists in main table.")
                return
            if not df_main.empty:
                df_main = df_main._append(df, ignore_index=True)
                with open(main_table_path, "w") as f:
                    f.write(df_main.to_csv())
                    return
        with open(main_table_path, "w") as f:
                f.write(df.to_csv())


processor = InvoiceProcessor()
# invoice_str = processor.convert_invoice_to_str_and_list_tuple("app/input_data/invoice_JL202747.pdf")
# invoice_no = processor.get_invoice_no(invoice_str[0])
# invoice_date = processor.get_invoice_date(invoice_str[0])

# # print(processor.process_invoice_data(invoice_str[1], invoice_no, invoice_date))

# print(processor.retrieve_manifest_from_website("NP-YELLOW928"))
print(processor.retrieve_manifest("LPNWE194529470"))