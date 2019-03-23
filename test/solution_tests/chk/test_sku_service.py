from solutions.CHK.checkout_solution.sku_service import SkuService
from pytest import mark

@mark.parametrize("sku,expected_price", [
    ("A", 50),
    ("X", None)
])
def test_get_sku(sku, expected_price):
    service = SkuService()
    service.skus = [
        {
            "sku": "A",
            "price": 50
        }
    ]

    response = service.get_sku(sku)

    price = response['price'] if response is not None else None

    assert price == expected_price