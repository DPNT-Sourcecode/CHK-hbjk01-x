import logging

from .sku_service import SkuService
from .validation_service import ValidationService

logging.getLogger().setLevel(logging.INFO)

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    sku_service = SkuService()
    
    try:
        sku_service.load_from_json_file('skus.json')
    except Exception:
        logging.error("Unable to load SKUs", exc_info=True)
        return -1

    valid_products = ValidationService(sku_service).validate_basket(skus)

    if not valid_products:
        return -1

    



