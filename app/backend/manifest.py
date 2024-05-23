import requests
import os
import csv
from app.backend.app_logging import logger
from app.backend.invoice import Invoice
from paths import MANIFEST_URL_BASE, BASE_DIR


class Manifest:
    def __init__(self):
        self.invoice = Invoice()
        self.local_manifest_dir = os.path.join(
            BASE_DIR, "app", "input_data", "manifests"
        )

    def get_items_quantity(self, manifest_path) -> int:
        total = 0
        with open(manifest_path, "r", encoding="utf-8") as csv_reader:
            reader = csv.reader(csv_reader)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                else:
                    quantity = int(float(row[4])) if row[4] else 0
                    total += quantity
        return total

    def get_item_price(self, invoice_item: list, manifest_path: str) -> float:
        invoice_item_price = self.invoice.get_item_price(invoice_item)
        manifest_items_quantity = self.get_items_quantity(manifest_path)
        return round((invoice_item_price / manifest_items_quantity), 2)

    def get_item_tax_value(self, invoice_item: list, manifest_path: str) -> float:
        manifest_items_quantity = self.get_items_quantity(manifest_path)
        invoice_item_price = self.invoice.get_item_price(invoice_item)
        tax_rate = self.invoice.get_tax_rate(invoice_item)
        return round((invoice_item_price / manifest_items_quantity * tax_rate), 2)

    def retrieve_from_website(self, manifest_id: str) -> str | None:
        url = os.path.join(MANIFEST_URL_BASE, f"{manifest_id}.csv")
        page = requests.get(url)
        if page.status_code != 200 or page.text.startswith("<html>"):
            logger.warning(f"Manifest {manifest_id} not found online.")
            return None
        if not os.path.exists(self.local_manifest_dir):
            os.makedirs(self.local_manifest_dir)
        saving_dir = os.path.join(self.local_manifest_dir, f"{manifest_id}.csv")
        with open(saving_dir, "w", encoding="utf-8") as f:
            f.write(page.text)
        return saving_dir

    def search_in_local_drive(self, manifest_id: str) -> str | None:
        manifest_path = os.path.join(self.local_manifest_dir, f"{manifest_id}.csv")
        if not os.path.exists(manifest_path):
            logger.warning(f"Manifest {manifest_id} not found locally.")
            return None
        logger.info(f"Local manifest {manifest_id} found.")
        return manifest_path

    def retrieve_manifest(self, manifest_id: str) -> str | None:
        manifest_path = self.search_in_local_drive(manifest_id)
        if not manifest_path:
            manifest_path = self.retrieve_from_website(manifest_id)
        return manifest_path

    def clean_manifest_id(self, manifest_id: str) -> str:
        return manifest_id.replace("\n", "").replace(" ", "")
