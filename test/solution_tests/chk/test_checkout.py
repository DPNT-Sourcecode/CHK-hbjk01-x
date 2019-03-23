from solutions.CHK.checkout_solution import checkout
from solutions.CHK.sku_service import SkuService
from solutions.CHK.pricing_service import PricingService
from solutions.CHK.validation_service import ValidationService
from unittest.mock import patch
from pytest import mark

@patch('solutions.CHK.checkout_solution.ValidationService', spec=ValidationService)
@patch('solutions.CHK.checkout_solution.SkuService', spec=SkuService)
def test_checkout_unable_to_load_sku_returns_fail(mock_sku_service, mock_validation_service):
    mock_sku_service.load_from_json_file.side_effect = OverflowError()

    output = checkout("stuff")

    assert output == -1

@patch('solutions.CHK.checkout_solution.ValidationService', spec=ValidationService)
@patch('solutions.CHK.checkout_solution.SkuService', spec=SkuService)
def test_checkout_invalid_string_returns_fail(mock_sku_service, mock_validation_service):
    mock_validation_service.validate_basket.return_value = False

    output = checkout("things")

    assert output == -1

@patch('solutions.CHK.checkout_solution.PricingService', spec=PricingService)
@patch('solutions.CHK.checkout_solution.ValidationService', spec=ValidationService)
@patch('solutions.CHK.checkout_solution.SkuService', spec=SkuService)
def test_checkout_valid_skus_returns_price(mock_sku_service, mock_validation_service, mock_pricing_service):
    mock_validation_service.validate_basket.return_value = True
    mock_pricing_service.get_price.return_value = 75

    output = checkout("this")

    assert output == 75
