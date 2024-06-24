import fitz


class Invoice:
    def __init__(self, standard_tax_rate=0.2):
        self.standard_tax_rate = standard_tax_rate

    def convert_to_str_and_list_tuple(self, invoice_path: str) -> tuple[str, list]:
        invoice_list = []
        all_text = ""
        doc = fitz.open(invoice_path)
        for page in doc:
            text = page.get_text()
            all_text += text
            page_tables = page.find_tables(
                snap_y_tolerance=2,
                snap_x_tolerance=1,
            )
            for table in page_tables:
                item = table.extract()
                if len(item[0]) > 2 and item[0][0] and item[0][0].startswith("Jobalots"):
                    invoice_list.extend(item)
        return all_text, invoice_list

    def get_date(self, invoice_str: str) -> str:
        invoice_date = invoice_str.split("ORDER DATE : ")[1].split("\n")[0]
        return invoice_date

    def get_invoice_no(self, invoice_str: str) -> str:
        invoice_no = invoice_str.split("INVOICE ")[1].split("\n")[0]
        return invoice_no

    def get_item_price(self, invoice_item: list) -> float | bool:
        price_str = invoice_item[-1]
        try:
            return float(price_str.split("£")[1])
        except TypeError:
            return 0.0

    def get_tax_rate(self, invoice_item: list) -> float:
        for item in reversed(invoice_item):
            if "%" in item:
                return float(item.split("%")[0]) / 100
            return self.standard_tax_rate
