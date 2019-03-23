from solutions.CHK.checkout_solution import checkout
from solutions.CHK.sku_service import SkuService
from solutions.CHK.validation_service import ValidationService
from unittest.mock import patch
from pytest import mark

@patch('validation_service.ValidationService', spec=ValidationService)
@patch('sku_service.SkuService', spec=SkuService)
class CheckoutTestCases():
    def test_checkout_unable_to_load_sku_returns_fail(self, mock_sku_service, mock_validation_service):
        mock_sku_service.load_from_json_file.side_effect = OverflowError()

        output = checkout("stuff")

        assert output == -1

    def test_checkout_invalid_string_returns_fail(self, mock_sku_service, mock_validation_service):
        mock_validation_service.validate_basket.return_value = False

        output = checkout("things")

        assert output == -1