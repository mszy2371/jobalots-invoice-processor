import requests
import fitz  # imports the pymupdf library
import pandas as pd
import os
import csv
import sys

class InvoiceProcessor:
    def __init__(self):
        self.input_manifest_path =  os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "input.csv"
        )
        self.output_manifest_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "manifest.csv"
        )
    
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

    def get_invoice_item_price(self, invoice_item: list) -> float:
        price_str = invoice_item[-1]
        try:
            return float(price_str.split("£")[1])
        except TypeError:
            return 0.0

    def get_manifest_items_quantity(self, manifest_path) -> int:
        total = 0
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

    def retrieve_manifest(self, manifest_id: str) -> str:
        url = f"https://static.bodysocks.net/joblots/manifests/{manifest_id}.csv"
        page = requests.get(url)
        with open(self.input_manifest_path, "w", encoding="utf-8") as f:
            f.write(page.text)
        return self.input_manifest_path

    def convert_manifest(
        self,
        invoice_date: str,
        invoice_no: str,
        invoice_item: list,
        input_csv_path: str,
        manifest_item_price,
    ) -> pd.DataFrame:
        manifest_id = invoice_item[1]
        with open(input_csv_path, "r", encoding="utf-8") as csv_reader, open(
            self.output_manifest_path, "w", encoding="utf-8"
        ) as csv_writer:
            reader = csv.reader(csv_reader)
            writer = csv.writer(csv_writer)
            for index, row in enumerate(reader):
                if index == 0:
                    row.append("Price")
                    row.append("Manifest No")
                    row.append("Invoice No")
                    row.append("Invoice Date")
                    writer.writerow(row)
                elif len(row[0]) < 2:
                    continue
                else:
                    row.append(manifest_item_price)
                    row.append(manifest_id)
                    row.append(invoice_no)
                    row.append(invoice_date)
                    writer.writerow(row)
        df = pd.read_csv(self.output_manifest_path, encoding="utf-8")
        df.drop("Unit Weight (g)", axis=1, inplace=True)
        df.drop("RRP", axis=1, inplace=True)
        df.drop("Total", axis=1, inplace=True)
        return df

    def process_invoice_data(self, invoice_list: str, invoice_no: str, invoice_date: str) -> dict:
        df_combined = pd.DataFrame()
        output_csv_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"output_data/data_for_{invoice_no}_from_{invoice_date}.csv",
        )
        for item in invoice_list:
            manifest_id = item[1]
            manifest_path = self.retrieve_manifest(manifest_id)
            manifest_item_price = self.get_manifest_item_price(item, manifest_path)
            df = self.convert_manifest(
                invoice_date, invoice_no, item, manifest_path, manifest_item_price
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
        if os.path.exists(main_table_path):
            df_main = pd.read_csv(main_table_path, index_col=0)
            if invoice_no in df_main["Invoice No"].values:
                print(f"Data for invoice {invoice_no} already exists in main table.")
                return
            df_main = df_main._append(df, ignore_index=True)
            with open(main_table_path, "w") as f:
                f.write(df_main.to_csv())
        else:
            with open(main_table_path, "w") as f:
                f.write(df.to_csv())


if __name__ == "__main__":
    InvoiceProcessor().add_data_to_main_table("app/input_data/invoice_JL200974.pdf", "app/output_data/main_table.csv")