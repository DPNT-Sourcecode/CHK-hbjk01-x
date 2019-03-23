from lib.solutions.CHK.checkout_solution import checkout
from lib.solutions.CHK.sku_service import SkuService
from lib.solutions.CHK.pricing_service import PricingService
from lib.solutions.CHK.validation_service import ValidationService
from unittest.mock import patch
from pytest import mark

@patch('lib.solutions.CHK.checkout_solution.ValidationService', spec=ValidationService)
@patch('lib.solutions.CHK.checkout_solution.SkuService', spec=SkuService)
def test_checkout_unable_to_load_sku_returns_fail(mock_sku_service, mock_validation_service):
    mock_sku_service.return_value.load_from_json_file.side_effect = OverflowError()

    output = checkout("stuff")

    assert output == -1

@patch('lib.solutions.CHK.checkout_solution.ValidationService', spec=ValidationService)
@patch('lib.solutions.CHK.checkout_solution.SkuService', spec=SkuService)
def test_checkout_invalid_string_returns_fail(mock_sku_service, mock_validation_service):
    mock_validation_service.return_value.validate_basket.return_value = False

    output = checkout("things")

    assert output == -1

@patch('lib.solutions.CHK.checkout_solution.PricingService', spec=PricingService)
@patch('lib.solutions.CHK.checkout_solution.ValidationService', spec=ValidationService)
@patch('lib.solutions.CHK.checkout_solution.SkuService', spec=SkuService)
def test_checkout_valid_skus_returns_price(mock_sku_service, mock_validation_service, mock_pricing_service):
    mock_validation_service.return_value.validate_basket.return_value = True
    mock_pricing_service.return_value.get_price.return_value = 75

    output = checkout("this")

    assert output == 75


