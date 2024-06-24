import os
from paths import MANIFEST_URL_BASE, BASE_DIR
from app.backend.manifest import Manifest
import pytest
from unittest import mock

manifest = Manifest()
MANIFEST_FOLDER_PATH = os.path.join(BASE_DIR, "app", "tests", "data")


@pytest.mark.parametrize(
    "manifest_id, quantity",
    [
        pytest.param("spW73n5369e", 19),
        pytest.param("spIna13cyjJ", 40),
        pytest.param("spSJL31jrL5", 5),
    ],
)
def test_get_items_quantity(manifest_id, quantity):
    manifest_path = os.path.join(MANIFEST_FOLDER_PATH, f"{manifest_id}.csv")
    result = manifest.get_items_quantity(manifest_path)
    expected_result = quantity

    assert result == expected_result


@pytest.mark.parametrize(
    "invoice_item, manifest_id, price",
    [
        pytest.param(1, "spW73n5369e", 0.49),
        pytest.param(3, "spIna13cyjJ", 0.60),
        pytest.param(6, "spSJL31jrL5", 1.04),
    ],
)
def test_get_item_price(invoice_str_and_list, invoice_item, manifest_id, price):
    manifest_path = os.path.join(MANIFEST_FOLDER_PATH, f"{manifest_id}.csv")
    invoice_item = invoice_str_and_list[1][
        invoice_item
    ]  # this manifest is the second item on the invoice
    result = manifest.get_item_price(invoice_item, manifest_path)
    expected_result = price

    assert result == expected_result


@pytest.mark.parametrize(
    "invoice_item, manifest_id, tax_value",
    [
        pytest.param(1, "spW73n5369e", 0.10),
        pytest.param(3, "spIna13cyjJ", 0.12),
        pytest.param(6, "spSJL31jrL5", 0.21),
    ],
)
def test_get_item_tax_value(invoice_str_and_list, invoice_item, manifest_id, tax_value):
    manifest_path = os.path.join(MANIFEST_FOLDER_PATH, f"{manifest_id}.csv")
    invoice_item = invoice_str_and_list[1][invoice_item]
    result = manifest.get_item_tax_value(invoice_item, manifest_path)
    expected_result = tax_value

    assert result == expected_result


@mock.patch("app.backend.manifest.requests.get")
def test_retrieve_from_website_successful(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "some_manifest_data"

    result = manifest.retrieve_from_website("test_manifest")

    assert result == os.path.join(
        BASE_DIR, "app", "input_data", "manifests", "test_manifest.csv"
    )


@mock.patch("app.backend.manifest.requests.get")
def test_retrieve_from_website_not_found(mock_get):
    mock_get.return_value.status_code = 404

    result = manifest.retrieve_from_website("nonexistent_manifest")

    assert result is None


@mock.patch("app.backend.manifest.requests.get")
def test_retrieve_from_website_invalid_content(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html>Invalid content</html>"

    result = manifest.retrieve_from_website("invalid_manifest")

    assert result is None

