
def select_message(invoice_no, output_key) -> str:
    outputs = {
        "done": f"{invoice_no} - Done!",
        "invoice exists": f"{invoice_no} - Invoice already exists in table, nothing added to main table",
        "empty": f"{invoice_no} - No data to process, empty file",
        "partially done": f"{invoice_no} - Partially done, some manifests missing, check logs",
    }
    return outputs[output_key]
