import pandas as pd
import os
import csv
from app.backend.app_logging import logger
from app.backend.invoice import Invoice
from app.backend.manifest import Manifest
from paths import EMPTY_MANIFEST, MISSING_MANIFESTS_DIR, PROCESSED_DATA_DIR


class DataProcessor:
    def __init__(self):
        self.invoice = Invoice()
        self.manifest = Manifest()

    def convert_data(
        self,
        invoice_date: str,
        invoice_no: str,
        invoice_item: list,
        invoice_item_tax_rate: float,
        input_csv_path: str,
        manifest_item_price: float,
        manifest_item_tax_value: float,
    ) -> pd.DataFrame:
        manifest_id: str = self.manifest.clean_manifest_id(invoice_item[1])
        output_manifest_path = os.path.join(
            self.manifest.local_manifest_dir, f"{manifest_id}-{invoice_no}.csv"
        )
        with open(input_csv_path, "r", encoding="utf-8") as csv_reader, open(
            output_manifest_path, "w", encoding="utf-8"
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
        converted_manifest_dir = os.path.join(
            self.manifest.local_manifest_dir, f"{manifest_id}-{invoice_no}.csv"
        )
        df = pd.read_csv(converted_manifest_dir, encoding="utf-8")
        df.drop("Unit Weight (g)", axis=1, inplace=True)
        df.drop("RRP", axis=1, inplace=True)
        df.drop("Total", axis=1, inplace=True)
        df["Price per item + tax"] = round(
            (df["Price per item"] + df["Tax per item"]), 2
        )
        df["Total price netto"] = round(
            (df["Price per item"] * df["Stock Quantity"]), 2
        )
        df["Total tax"] = round(df["Total price netto"] * invoice_item_tax_rate, 2)
        return df

    def process_invoice_data(
        self, invoice_list: str, invoice_no: str, invoice_date: str
    ) -> tuple[pd.DataFrame, bool]:
        df_combined = pd.DataFrame()
        is_partially_missing = False
        if not os.path.exists(PROCESSED_DATA_DIR):
            os.mkdir(PROCESSED_DATA_DIR)
        output_csv_path = os.path.join(
            PROCESSED_DATA_DIR,
            f"data_for_{invoice_no}_from_{invoice_date}.csv",
        )
        missing_manifests_path = os.path.join(
            MISSING_MANIFESTS_DIR, f"for_{invoice_no}.txt"
        )
        if os.path.exists(missing_manifests_path):
            os.remove(missing_manifests_path)
        for item in invoice_list:
            manifest_id = self.manifest.clean_manifest_id(item[1])
            manifest_path = self.manifest.retrieve_manifest(manifest_id)
            if not manifest_path:
                manifest_path = EMPTY_MANIFEST
                is_partially_missing = True
                with open(missing_manifests_path, "a") as f:
                    f.write(f"{manifest_id}: {item}\n")
            invoice_item_tax_rate = self.invoice.get_tax_rate(item)
            manifest_item_price = self.manifest.get_item_price(item, manifest_path)
            manifest_item_tax_value = self.manifest.get_item_tax_value(
                item, manifest_path
            )
            df = self.convert_data(
                invoice_date,
                invoice_no,
                item,
                invoice_item_tax_rate,
                manifest_path,
                manifest_item_price,
                manifest_item_tax_value,
            )
            if not df.empty:
                df_combined = df_combined._append(df, ignore_index=True)
        with open(output_csv_path, "w") as f:
            f.write(df_combined.to_csv())
        return df_combined, is_partially_missing

    def add_data_to_main_table(
        self, invoice_path: str, main_table_path: str
    ) -> tuple[str, str]:
        invoice_str, invoice_list = self.invoice.convert_to_str_and_list_tuple(
            invoice_path
        )
        invoice_date = self.invoice.get_date(invoice_str)
        invoice_no = self.invoice.get_invoice_no(invoice_str)
        processed_data = self.process_invoice_data(
            invoice_list, invoice_no, invoice_date
        )
        df = processed_data[0]
        if df.empty:
            return invoice_no, "empty"
        if os.path.exists(main_table_path) and os.path.getsize(main_table_path) > 0:
            df_main = pd.read_csv(main_table_path, index_col=0)
            if (
                "Invoice No" in df_main.keys()
                and invoice_no in df_main["Invoice No"].values
            ):
                logger.info(
                    "Data for invoice %s already exists in main table.", invoice_no
                )
                return invoice_no, "invoice exists"
            if not df_main.empty:
                df_main = df_main._append(df, ignore_index=True)
                with open(main_table_path, "w") as f:
                    f.write(df_main.to_csv())
                    return invoice_no, "done"
        with open(main_table_path, "w") as f:
            f.write(df.to_csv())
            if processed_data[1]:
                return invoice_no, "partially done"
            return invoice_no, "done"

    def process_whole_folder(
        self, input_folder: str, output_folder: str, output_file: str
    ) -> None:
        sorted_files = sorted(os.listdir(input_folder))
        output_file = os.path.join(output_folder, output_file)
        for file in sorted_files:
            input_file = os.path.join(input_folder, file)
            if file in os.listdir(input_folder) and file.endswith(".pdf"):
                self.add_data_to_main_table(input_file, output_file)
        logger.info("All files processed.")
        return

