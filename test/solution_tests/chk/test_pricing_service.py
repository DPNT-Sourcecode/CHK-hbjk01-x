from lib.solutions.CHK.pricing_service import PricingService
from unittest.mock import MagicMock
from pytest import mark

@mark.parametrize("basket_string,expected_output", [
    ("A", 50),
    ("AA", 100),
    ("AAA", 130),
    ("AAAA", 180),
    ("AAAAAAAA", 370)
])
def test_get_price(basket_string, expected_output):
    mock_sku_service = MagicMock()
    service = PricingService(mock_sku_service)

    mock_sku_service.get_sku.return_value = {
            "sku": "A",
            "price": 50,
            "offers": [
                {
                    "quantity": 3,
                    "price": 130
                }
            ]
        }

    price = service.get_price(basket_string)

    assert price == expected_output


