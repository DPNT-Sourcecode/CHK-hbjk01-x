from lib.solutions.CHK.pricing_service import PricingService
from lib.solutions.CHK.sku_service import SkuService
from unittest.mock import MagicMock
from pytest import mark

# getting a bit like an integration test here
@mark.parametrize("basket_string,expected_output", [
    ("A", 50),
    ("AA", 100),
    ("AAA", 130),
    ("AAAA", 180),
    ("AAAAA", 200),
    ("AAAAAAAA", 330),
    ("ABCDABCD", 215),
    ("EE", 80),
    ("EEB", 80),
    ("EEBB", 110),
    ("EEBBB", 125),
    ("EEBBBBB", 170),
    ("EEEEBB", 160),
    ('BDEEE', 135)
])
def test_get_price(basket_string, expected_output):
    sku_service = SkuService()
    service = PricingService(sku_service)

    sku_service.load_from_json_file('lib/solutions/chk/skus.json')
    
    price = service.get_price(basket_string)

    assert price == expected_output
