from solutions.CHK.validation_service import ValidationService
from pytest import mark
from unittest.mock import MagicMock

@mark.parametrize("basket_string,expected_outcome", [
    ("A", True),
    ("AA", True),
    ("B", False),
    (1337, False),
    (None, False)
])
def test_validate_basket(basket_string, expected_outcome):
    sku_service = MagicMock()
    service = ValidationService(sku_service)

    def fake_get_sku(sku):
        return {
            "sku": "A",
            "price": 50
        } if sku == "A" else None

    sku_service.get_sku.side_effect = fake_get_sku

    outcome = service.validate_basket(basket_string)

    assert outcome == expected_outcome