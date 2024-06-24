from app.backend.invoice import Invoice
from paths import BASE_DIR
import os
import pytest


invoice = Invoice()
invoice_path = os.path.join(
    BASE_DIR, "app", "tests", "data", "invoice_for_tests_jl278024.pdf"
)


def test_convert_to_str_and_list_tuple(invoice_str_and_list):
    result = invoice.convert_to_str_and_list_tuple(invoice_path)

    assert result == invoice_str_and_list
    assert result[0] == invoice_str_and_list[0]
    assert result[1] == invoice_str_and_list[1]


def test_get_date():
    invoice_str, _ = invoice.convert_to_str_and_list_tuple(invoice_path)
    result = invoice.get_date(invoice_str)
    expected_result = "2024-05-21"

    assert result == expected_result


def test_get_invoice_no():
    invoice_str, _ = invoice.convert_to_str_and_list_tuple(invoice_path)
    result = invoice.get_invoice_no(invoice_str)
    expected_result = "JL278024"

    assert result == expected_result


@pytest.mark.parametrize(
    "position, item_price",
    [
        pytest.param(0, 8.0),
        pytest.param(1, 9.3),
        pytest.param(2, 3.2),
        pytest.param(3, 24.0),
        pytest.param(4, 2.1),
        pytest.param(5, 4.0),
        pytest.param(6, 5.21),
    ]
)
def test_get_item_price(position, item_price):
    _, invoice_list = invoice.convert_to_str_and_list_tuple(invoice_path)
    result = invoice.get_item_price(invoice_list[position])
    expected_result = item_price

    assert result == expected_result

def test_get_tax_rate():
    _, invoice_list = invoice.convert_to_str_and_list_tuple(invoice_path)
    result = invoice.get_tax_rate(invoice_list[0])
    expected_result = 0.2

    assert result == expected_result